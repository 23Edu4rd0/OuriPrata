from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings_view, name='settings'),
    path('change-email/', views.change_email, name='change_email'),
    path('change-profile/', views.change_profile, name='change_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('privacy/', views.privacy_policy, name='politica_de_privacidade'),
]
