from django.urls import path
from pagamentos import views

urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
    path('sucesso/', views.pagamento_sucesso, name='pagamento_sucesso'),
    path('sucesso/<str:produto_slug>/', views.pagamento_sucesso, name='pagamento_sucesso_produto'),
    path('erro/', views.pagamento_erro, name='pagamento_erro'),
    path('falha/<str:produto_slug>/', views.pagamento_erro, name='pagamento_erro_produto'),
    path('pendente/', views.pagamento_pendente, name='pagamento_pendente'),
    path('pendente/<str:produto_slug>/', views.pagamento_pendente, name='pagamento_pendente_produto'),
]
