from django.contrib import admin
from .models import Category, Subcategory, Material, Occasion, Product, ProductImage

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Material)
admin.site.register(Occasion)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'description', 'order')
    fk_name = 'product'


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'price', 'featured', 'category', 'material')
    search_fields = ('name', 'description')
    list_filter = ('category', 'material', 'featured')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)