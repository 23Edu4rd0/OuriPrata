from django.urls import path
from . import views
from pagamentos import views as pagamentos_views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.all_products, name='catalogo'),  # Lista todos os produtos
    path('buscar/', views.search_products, name='search_products'),
    path('buscar/sugestoes/', views.search_suggestions, name='search_suggestions'),
    path('item/<slug:slug>/', views.item_detail, name='product_detail'),
    path('categoria/<slug:categoria_slug>/', views.products_by_category, name='products_by_category'),  # Lista produtos por categoria
    path('contato/', views.contact, name='contact'),
    path('quem-somos/', views.about, name='about'),  
    path('politica-de-privacidade/', views.policy, name='policy'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('sucesso/', pagamentos_views.pagamento_sucesso, name='pagamento_sucesso'),
    path('erro/', pagamentos_views.pagamento_erro, name='pagamento_erro'),
    path('pendente/', pagamentos_views.pagamento_pendente, name='pagamento_pendente'),
]
