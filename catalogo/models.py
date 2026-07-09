from django.db import models
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
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='catalog', blank=True, null=True)

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

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def extra_images(self):
        return self.images.all()


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