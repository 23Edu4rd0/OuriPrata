from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cidade', 'estado', 'eh_divinopolis', 'frete_gratuito', 'endereco_completo')
    list_filter = ('eh_divinopolis', 'frete_gratuito', 'endereco_completo', 'estado')
    search_fields = ('user__username', 'user__email', 'cidade', 'cep')
    readonly_fields = ('eh_divinopolis', 'frete_gratuito', 'endereco_completo', 'data_atualizacao')
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Endereço', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
        }),
        ('Informações Calculadas', {
            'fields': ('eh_divinopolis', 'frete_gratuito', 'endereco_completo', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
