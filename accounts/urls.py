from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('settings/', views.settings_view, name='settings'),
    path('change-email/', views.change_email, name='change_email'),
    path('change-profile/', views.change_profile, name='change_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('privacy/', views.privacy_policy, name='politica_de_privacidade'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('api/lookup-cep/', views.lookup_cep, name='lookup_cep'),
]
