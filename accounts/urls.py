from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('sing_up/', views.sing_up, name='sing_up'),
]
