from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('colecao/', views.all_products, name='all_products'),
    path('buscar/', views.search_products, name='search_products'),
    path('buscar/sugestoes/', views.search_suggestions, name='search_suggestions'),
    path('item/<slug:slug>/', views.item_detail, name='product_detail'),
    path('categoria/<slug:categoria_slug>/', views.products_by_category, name='products_by_category'),
    path('contato/', views.contact, name='contact_us'),
    path('sobre/', views.about, name='about_us'),
    path('politica-de-privacidade/', views.policy, name='politica_privacidade'),
    path('termos-de-uso/', views.terms, name='termos_uso'),
    # Alias legado (catálogo → coleção)
    path('catalogo/', views.all_products, name='catalogo'),
]
