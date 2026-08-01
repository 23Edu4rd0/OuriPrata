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
    path('product/<slug:slug>/avaliar/', views.submit_review, name='submit_review'),
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
    path('carrinho/', views.cart_page, name='cart'),
    path('colecoes/', views.collection_list, name='collection_list'),
    path('colecoes/<slug:slug>/', views.collection_detail, name='collection_detail'),
    path('consulta-personalizada/', views.consulta_personalizada, name='consulta_personalizada'),
    # Legacy alias (catálogo → coleção)
    path('catalogo/', views.all_products, name='catalogo'),
]