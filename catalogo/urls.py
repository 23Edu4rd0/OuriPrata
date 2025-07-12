from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<slug:slug>/', views.item_detail, name='product_detail'),
    path('contato/', views.contact, name='contact'),
    path('quem-somos/', views.about, name='about'),  
    path('politica-de-privacidade/', views.policy, name='policy'), 
    path('produto/', views.product, name='product')
]
