from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<slug:slug>/', views.item_detail, name='product_detail'),
    path('contato/', views.contact, name='contact'),
    path('quem-somos/', views.about, name='about'),  
    path('politica-de-privacidade/', views.policy, name='policy'),
    path('produto/<slug:slug>/', views.item_detail, name='item_detail'), 
    path('webrook/', views.webrook, name='webrook')
]
