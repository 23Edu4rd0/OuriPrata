import re

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalogo.urls')),
    path('conta/', include('accounts.urls')),
]

# Só o settings de desenvolvimento instala o django_browser_reload; incluir a
# rota sem o app derrubaria a produção no import.
if 'django_browser_reload' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('__reload__/', include('django_browser_reload.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
else:
    # As fotos das peças são enviadas pelo admin em tempo de execução, então
    # não passam pelo collectstatic e o whitenoise não as enxerga. O helper
    # static() acima devolve lista vazia quando DEBUG=False, o que deixaria o
    # catálogo sem imagem nenhuma em produção.
    #
    # Servir pelo próprio Django não é o mais rápido, mas dá conta do volume de
    # um catálogo pequeno. Se o tráfego crescer, o caminho é mover as imagens
    # para armazenamento de objetos (S3, Cloudflare R2) e apontar MEDIA_URL
    # para lá — só esta rota sai.
    # O prefixo sai de MEDIA_URL em vez de ficar fixo, para a rota não sair do
    # ar caso a configuração mude.
    _prefixo_media = re.escape(settings.MEDIA_URL.lstrip('/'))
    urlpatterns += [
        re_path(
            rf'^{_prefixo_media}(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT},
        ),
    ]
