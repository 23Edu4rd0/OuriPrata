from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('colecao/', views.all_products, name='all_products'),
    path('buscar/', views.search_products, name='search_products'),
    path(
        'buscar/sugestoes/',
        views.search_suggestions,
        name='search_suggestions',
    ),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('favoritos/', views.wishlist, name='wishlist'),
    path(
        'categoria/<slug:category_slug>/',
        views.products_by_category,
        name='products_by_category',
    ),
    path('contato/', views.contact, name='contact_us'),
    path('sobre/', views.about, name='about_us'),
    path(
        'politica-de-privacidade/', views.policy, name='politica_privacidade'
    ),
    path('termos-de-uso/', views.terms, name='termos_uso'),
    # Legacy alias (catálogo → coleção)
    path('catalogo/', views.all_products, name='catalogo'),
]