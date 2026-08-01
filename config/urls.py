import re

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalogo.urls')),
    path('conta/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__reload__/', include('django_browser_reload.urls')),
    ]
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
