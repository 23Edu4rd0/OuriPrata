from django.contrib import admin
from .models import Categoria, SubCategoria, Material, Ocasiao, Joia, JoiaImagem

admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Material)
admin.site.register(Ocasiao)

class JoiaImagemInline(admin.StackedInline):
    model = JoiaImagem
    extra = 1
    fields = ('imagem', 'descricao', 'ordem')
    fk_name = 'joia'

class JoiaAdmin(admin.ModelAdmin):
    inlines = [JoiaImagemInline]
    list_display = ('nome', 'preco', 'destaque', 'categoria', 'material')
    search_fields = ('nome', 'descricao')
    list_filter = ('categoria', 'material', 'destaque')
    prepopulated_fields = {'slug': ('nome',)}

admin.site.register(Joia, JoiaAdmin)
