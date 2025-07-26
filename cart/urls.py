from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('checkout/', views.checkout_cart, name='checkout'),
    path('add/<int:produto_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:produto_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:produto_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('count/', views.cart_count, name='cart_count'),
    path('webhook/', views.webhook_cart, name='webhook_cart'),
]
