from django.contrib import admin

from .models import (
    Category,
    Collection,
    Material,
    Occasion,
    Product,
    ProductImage,
    ProductVariant,
    Review,
    Subcategory,
)

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Material)
admin.site.register(Occasion)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'description', 'order')
    fk_name = 'product'


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('size', 'stock')


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    can_delete = True


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductVariantInline, ReviewInline]
    list_display = (
        'name', 'price', 'promo_price', 'em_promocao',
        'stock_quantity', 'featured', 'category', 'material',
    )
    list_editable = ('promo_price',)
    search_fields = ('name', 'description')
    list_filter = ('category', 'material', 'featured')
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Em promoção', boolean=True)
    def em_promocao(self, obj):
        return obj.is_on_sale


admin.site.register(Product, ProductAdmin)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured', 'is_season', 'season_label')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('products',)
    list_filter = ('featured', 'is_season')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at',)
