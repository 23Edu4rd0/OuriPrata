"""
Configurações comuns aos dois ambientes.

Nada aqui decide se o site está em desenvolvimento ou em produção: o que muda
entre os dois fica em dev.py e prod.py, que importam este arquivo. Assim uma
configuração de segurança não depende de alguém lembrar de mudar uma variável
— o ambiente errado simplesmente não carrega o módulo errado.

Qual módulo é usado vem de DJANGO_ENV (veja config/environment.py).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# O .env é conveniência de desenvolvimento. Em produção as variáveis vêm do
# painel do Railway; override=False garante que um .env que acabe indo parar no
# container não sobrescreva o que o servidor definiu.
load_dotenv(BASE_DIR / '.env', override=False)


def env_list(nome):
    """Lê uma variável com valores separados por vírgula."""
    return [
        item.strip() for item in os.getenv(nome, '').split(',') if item.strip()
    ]


def env_bool(nome, padrao='False'):
    return os.getenv(nome, padrao).strip().lower() in {'true', '1', 'yes'}


# O Railway expõe o domínio gerado para o serviço nesta variável.
RAILWAY_PUBLIC_DOMAIN = os.getenv('RAILWAY_PUBLIC_DOMAIN', '').strip()

# Definidos em dev.py / prod.py.
DEBUG = False
SECRET_KEY = None

ALLOWED_HOSTS = env_list('ALLOWED_HOSTS')
if RAILWAY_PUBLIC_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)

# Application definition

INSTALLED_APPS = [
    'catalogo.apps.CatalogoConfig',
    'accounts.apps.AccountsConfig',
    'theme',
    'jazzmin',
    'tailwind',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

TAILWIND_APP_NAME = 'theme'

JAZZMIN_SETTINGS = {
    'theme': 'cyborg',
    'site_title': 'Administração do OuriPrata',
    'site_header': 'OuriPrata Admin',
    'welcome_sign': 'Bem-vindo ao Painel do OuriPrata',
    'copyright': 'OuriPrata © 2025',
    'show_sidebar': True,
    'navigation_expanded': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
#
# O banco fica a cargo de cada ambiente: dev.py cai no SQLite quando não há
# DATABASE_URL, prod.py exige a variável.

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Media files
#
# Em produção MEDIA_ROOT precisa apontar para o volume persistente do Railway,
# senão as fotos enviadas pelo admin somem no próximo deploy (o disco do
# container é descartável).

MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv('MEDIA_ROOT', BASE_DIR / 'media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'home'

CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS')
if RAILWAY_PUBLIC_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RAILWAY_PUBLIC_DOMAIN}')

# Logging: o Railway captura o stdout/stderr do container, então basta escrever
# no console para os logs aparecerem no painel.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'padrao': {
            'format': '[{levelname}] {asctime} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'padrao',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
