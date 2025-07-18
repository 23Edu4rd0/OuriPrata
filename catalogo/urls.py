from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.all_products, name='catalogo'),
    path('buscar/', views.search_products, name='search_products'),
    path('buscar/sugestoes/', views.search_suggestions, name='search_suggestions'),
    path('item/<slug:slug>/', views.item_detail, name='product_detail'),
    path('checkout/<slug:product_slug>/', views.checkout, name='checkout'),
    path('categoria/<slug:categoria_slug>/', views.products_by_category, name='products_by_category'),
    path('contato/', views.contact, name='contact'),
    path('quem-somos/', views.about, name='about'),  
    path('politica-de-privacidade/', views.policy, name='policy'),
    path('produto/<slug:slug>/', views.item_detail, name='item_detail'), 
    path('webhook/', views.webhook, name='webhook'),
    # URLs de callback do Mercado Pago
    path('sucesso/', views.pagamento_sucesso, name='pagamento_sucesso'),
    path('erro/', views.pagamento_erro, name='pagamento_erro'),
    path('pendente/', views.pagamento_pendente, name='pagamento_pendente'),
]
