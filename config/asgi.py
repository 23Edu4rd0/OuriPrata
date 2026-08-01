"""
ASGI config for food_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application

from config import environment

# Escolhe dev ou produção a partir de DJANGO_ENV.
environment.configure()

application = get_asgi_application()
