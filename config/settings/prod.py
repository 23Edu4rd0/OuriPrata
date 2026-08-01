"""
Ambiente de produção (DJANGO_ENV=production — o padrão dentro do Railway).

As checagens deste módulo falham na subida, de propósito: é melhor o deploy
não iniciar do que o site ficar no ar com a chave de desenvolvimento ou com
DEBUG ligado expondo código-fonte, SQL e variáveis na tela de erro.
"""

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .base import env_bool

DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY', '').strip()
if not SECRET_KEY:
    raise ImproperlyConfigured(
        'SECRET_KEY não definida. Gere uma com '
        '`python -c "import secrets; print(secrets.token_urlsafe(64))"` '
        'e defina no Railway com `railway variables --set SECRET_KEY=...`.'
    )

if not ALLOWED_HOSTS:  # noqa: F405
    raise ImproperlyConfigured(
        'ALLOWED_HOSTS vazia. Defina ALLOWED_HOSTS (domínios separados por '
        'vírgula) ou publique pelo Railway, que injeta RAILWAY_PUBLIC_DOMAIN.'
    )

# Banco: o Postgres do Railway injeta DATABASE_URL ao ser ligado ao serviço.
# conn_max_age reaproveita a conexão entre requisições; conn_health_checks
# descarta a conexão morta depois de um restart do banco em vez de estourar
# erro no primeiro acesso.
_database_url = os.getenv('DATABASE_URL', '').strip()
if not _database_url:
    raise ImproperlyConfigured(
        'DATABASE_URL não definida. Ligue o serviço Postgres ao web no '
        'Railway (railway add --database postgres).'
    )

import dj_database_url  # noqa: E402

DATABASES = {
    'default': dj_database_url.parse(
        _database_url,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# A variante Manifest põe um hash no nome de cada arquivo
# (styles.a1b2c3.css), então uma versão nova nunca é servida do cache antigo
# do navegador. Isso importa para segurança: sem hash, quem já visitou o site
# continuaria com o JavaScript anterior mesmo depois de uma correção.
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# --- Segurança -------------------------------------------------------------

# O Railway termina o TLS no roteador dele e repassa a requisição em http. Sem
# este cabeçalho o Django acharia que a conexão é insegura e redirecionaria em
# laço infinito.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', 'True')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS instrui o navegador a só acessar por https. Começa em 1 hora de
# propósito: se algo der errado com o certificado, o prejuízo expira rápido.
# Suba para 31536000 (1 ano) depois de confirmar que o domínio está estável.
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '3600'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF_TRUSTED_ORIGINS já vem do base.py com o domínio do Railway. Sem ele o
# admin recusaria o POST de login com "CSRF verification failed".
if not CSRF_TRUSTED_ORIGINS:  # noqa: F405
    raise ImproperlyConfigured(
        'CSRF_TRUSTED_ORIGINS vazia. Defina a variável com a origem completa '
        '(https://seu-dominio) ou publique pelo Railway.'
    )
