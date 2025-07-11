from django.db import models


# Create your models here.

class Joais(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    em_promocao = models.BooleanField(default=False)
    imagem = models.ImageField(upload_to='catalogo', blank=True, null=True)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    ocasiao = models.ForeignKey('Ocasiao', on_delete=models.CASCADE, null=True, blank=True)
    destaque = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name = "Joia"
        verbose_name_plural = "Joias"

    def __str__(self):
        return self.nome
    
class Categorias(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
    
    def __str__(self):
        return self.nome

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