from django.urls import path

from . import views

urlpatterns = [
    path('entrar/', views.AccountLoginView.as_view(), name='login'),
    path('sair/', views.AccountLogoutView.as_view(), name='logout'),
    path('cadastro/', views.signup, name='signup'),
    path('perfil/', views.profile, name='profile'),
    path('favoritos/alternar/', views.toggle_wishlist, name='toggle_wishlist'),
]
