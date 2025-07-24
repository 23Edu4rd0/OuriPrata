from django.db import models
from django.utils.text import slugify

# Create your models here.

class Joais(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(blank=True, null=True)
    descricao = models.TextField(null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    em_promocao = models.BooleanField(default=False)
    imagem = models.ImageField(upload_to='catalogo', blank=True, null=True, help_text="Imagem principal")
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    ocasiao = models.ForeignKey('Ocasiao', on_delete=models.CASCADE, null=True, blank=True)
    categoria = models.ForeignKey('Categorias', on_delete=models.CASCADE, null=True, blank=True)
    destaque = models.BooleanField(default=False)

    def imagens(self):
        return self.imagens_extra.all()

class JoaisImagem(models.Model):
    joia = models.ForeignKey(Joais, on_delete=models.CASCADE, related_name='imagens_extra')
    imagem = models.ImageField(upload_to='catalogo/extra')
    descricao = models.CharField(max_length=100, blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0, help_text="Ordem de exibição")

    class Meta:
        ordering = ['ordem']
        verbose_name = "Imagem da Joia"
        verbose_name_plural = "Imagens da Joia"

    def __str__(self):
        return f"Imagem de {self.joia.nome} ({self.id})"
    
    
    # ...restante da classe Joais já está acima...
    
class Categorias(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(blank=True, null=True)
    imagem = models.ImageField(upload_to='categorias/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nome)
            slug = base_slug
            contador = 1
            while Categorias.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)

class SubCategorias(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, related_name='subcategorias')
    
    class Meta:
        verbose_name = "Subcategoria"
        verbose_name_plural = "Subcategorias"
    
    def __str__(self):
        return self.nome

class Material(models.Model):
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome
    
class Ocasiao(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome