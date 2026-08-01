"""
WSGI config for food_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application

from config import environment

# Escolhe dev ou produção a partir de DJANGO_ENV.
environment.configure()

application = get_wsgi_application()
