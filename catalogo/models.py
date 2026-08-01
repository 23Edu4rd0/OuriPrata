from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


def generate_unique_slug(model_class, name, instance_pk=None):
    base_slug = slugify(name)
    slug = base_slug
    counter = 1
    queryset = model_class.objects.filter(slug=slug)
    if instance_pk:
        queryset = queryset.exclude(pk=instance_pk)

    while queryset.exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
        queryset = model_class.objects.filter(slug=slug)
        if instance_pk:
            queryset = queryset.exclude(pk=instance_pk)

    return slug


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.name, self.pk)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('products_by_category', kwargs={'category_slug': self.slug})


class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories'
    )

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.category.name} > {self.name}'


class Material(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
        ordering = ['name']

    def __str__(self):
        return self.name


class Occasion(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Occasion'
        verbose_name_plural = 'Occasions'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_CHOICES = [
        ('feminino', 'Feminino'),
        ('masculino', 'Masculino'),
        ('unissex', 'Unissex'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Informational price (optional)',
    )
    promo_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Preço promocional',
        help_text='Deixe em branco se a peça não está em promoção. Precisa ser menor que o preço normal.',
    )
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='catalog', blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Deixe em branco para estoque ilimitado. Use variantes para controle por tamanho.'
    )
    created_at = models.DateTimeField(auto_now_add=True)


    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='products'
    )
    occasion = models.ForeignKey(
        Occasion,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, blank=True
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-featured', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.name, self.pk)
        super().save(*args, **kwargs)

    def clean(self):
        if self.promo_price is not None:
            if self.price is None:
                raise ValidationError({
                    'promo_price': 'Defina o preço normal antes de cadastrar uma promoção.'
                })
            if self.promo_price >= self.price:
                raise ValidationError({
                    'promo_price': 'O preço promocional precisa ser menor que o preço normal.'
                })

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def extra_images(self):
        return self.images.all()

    @property
    def is_new(self):
        return self.created_at and self.created_at >= timezone.now() - timedelta(days=14)

    @property
    def is_on_sale(self):
        return (
            self.promo_price is not None
            and self.price is not None
            and self.promo_price < self.price
        )

    @property
    def current_price(self):
        """Preço que o cliente paga — o promocional quando há promoção válida."""
        return self.promo_price if self.is_on_sale else self.price

    @property
    def discount_percent(self):
        if not self.is_on_sale:
            return None
        return int(round((1 - self.promo_price / self.price) * 100))

    @property
    def is_out_of_stock(self):
        return self.stock_quantity is not None and self.stock_quantity == 0

    @property
    def is_low_stock(self):
        return self.stock_quantity is not None and 0 < self.stock_quantity <= 3


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='catalog/extra')
    description = models.CharField(max_length=100, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['order']

    def __str__(self):
        return f'Image of {self.product.name} ({self.id})'


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variants'
    )
    size = models.CharField(max_length=30)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size')
        ordering = ['size']
        verbose_name = 'Variante'
        verbose_name_plural = 'Variantes'

    def __str__(self):
        return f'{self.product.name} — {self.size}'


class Collection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='collections/', blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True, related_name='collections')
    featured = models.BooleanField(default=False)
    is_season = models.BooleanField(
        default=False,
        verbose_name='Coleção da estação',
        help_text='Exibe as peças desta coleção em destaque na página inicial. '
                  'Se marcar mais de uma, vale a primeira em ordem alfabética.',
    )
    season_label = models.CharField(
        max_length=60,
        blank=True,
        verbose_name='Rótulo da estação',
        help_text='Ex: "Coleção de Inverno". Se vazio, usa "Coleção da estação".',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Coleção'
        verbose_name_plural = 'Coleções'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Collection, self.name, self.pk)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('collection_detail', kwargs={'slug': self.slug})


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f'{self.user.username} — {self.product.name} ({self.rating}★)'