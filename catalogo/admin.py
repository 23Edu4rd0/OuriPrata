from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Categorias)
admin.site.register(SubCategorias)
admin.site.register(Material)
admin.site.register(Ocasiao)
from .models import JoaisImagem

class JoaisImagemInline(admin.StackedInline):
    model = JoaisImagem
    extra = 1
    fields = ('imagem', 'descricao', 'ordem')
    fk_name = 'joia'

class JoaisAdmin(admin.ModelAdmin):
    inlines = [JoaisImagemInline]
    list_display = ('nome', 'preco', 'em_promocao', 'destaque')
    search_fields = ('nome',)

admin.site.register(Joais, JoaisAdmin)
