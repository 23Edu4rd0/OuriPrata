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

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'produto', 'rating', 'titulo', 'recomendado', 'aprovado', 'data_criacao']
    list_filter = ['rating', 'recomendado', 'aprovado', 'data_criacao']
    search_fields = ['usuario__username', 'produto__nome', 'titulo', 'comentario']
    list_editable = ['aprovado']
    readonly_fields = ['data_criacao', 'data_atualizacao']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('produto', 'usuario', 'rating', 'titulo', 'comentario')
        }),
        ('Mídia', {
            'fields': ('foto',),
            'classes': ('collapse',)
        }),
        ('Configurações', {
            'fields': ('recomendado', 'aprovado')
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ['review', 'legenda', 'data_upload']
    list_filter = ['data_upload']
    search_fields = ['review__usuario__username', 'legenda']
    readonly_fields = ['data_upload']
