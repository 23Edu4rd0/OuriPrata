from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('item/', views.items, name='item'),
    path('contato/', views.contact, name='contact'),
    path('quem-somos/', views.about, name='about'),  # Nova rota
]
