"""
Ambiente de desenvolvimento (DJANGO_ENV=dev, o padrão fora do Railway).

Prioriza conveniência: erros detalhados na tela, auto-reload do navegador,
SQLite sem precisar subir um Postgres, e nenhum redirecionamento para https —
que travaria o runserver em laço.
"""

import os

from .base import *  # noqa: F403
from .base import BASE_DIR, env_bool

DEBUG = env_bool('DEBUG', 'True')

# Em desenvolvimento a chave não protege nada real, então tem um padrão para o
# projeto rodar logo depois do clone. Em produção não existe padrão (prod.py).
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-desenvolvimento-nao-use-em-producao',
)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', 'testserver']

INTERNAL_IPS = ['127.0.0.1']

# django_browser_reload injeta um script de auto-reload em cada página; é
# ferramenta de desenvolvimento e não entra em produção.
INSTALLED_APPS += ['django_browser_reload']  # noqa: F405

# Entra logo depois do SecurityMiddleware, que o Django recomenda manter no
# topo: assim os cabeçalhos de segurança valem para todas as respostas e o
# ambiente de desenvolvimento não mascara problemas de ordem.
MIDDLEWARE = MIDDLEWARE[:]  # noqa: F405
MIDDLEWARE.insert(
    MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1,
    'django_browser_reload.middleware.BrowserReloadMiddleware',
)

# SQLite por padrão. Definindo DATABASE_URL dá para apontar para um Postgres
# local (ou para o do Railway, via `railway run`) sem mexer no código.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

_database_url = os.getenv('DATABASE_URL', '').strip()
if _database_url:
    import dj_database_url

    DATABASES['default'] = dj_database_url.parse(_database_url)

# Storage simples: a variante Manifest exigiria rodar collectstatic a cada
# alteração de CSS, e quebra a página com erro se um arquivo não estiver no
# manifesto.
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

CSRF_TRUSTED_ORIGINS += [  # noqa: F405
    'http://localhost',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
]

# E-mails de recuperação de senha e afins aparecem no terminal em vez de
# exigirem um servidor SMTP configurado.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
