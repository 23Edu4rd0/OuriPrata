from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('add/<int:produto_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:produto_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('check/<int:produto_id>/', views.check_wishlist_status, name='check_wishlist_status'),
]
