from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'produto', 'quantidade', 'total_item', 'data_adicionado']
    list_filter = ['data_adicionado', 'data_atualizado']
    search_fields = ['user__username', 'produto__nome']
    readonly_fields = ['data_adicionado', 'data_atualizado']
    
    def total_item(self, obj):
        return f"R$ {obj.total_item}"
    total_item.short_description = 'Total do Item'
