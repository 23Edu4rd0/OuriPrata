from django.contrib import admin
from .models import Wishlist

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'produto', 'data_adicionado']
    list_filter = ['data_adicionado']
    search_fields = ['user__username', 'produto__nome']
    readonly_fields = ['data_adicionado']
