from django.db import models


# Create your models here.
class Categories(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
    
    def __str__(self):
        return self.nome
    
class Menu_Items(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    imagem = models.ImageField(upload_to='catalogo', blank=True, null=True)
    categoria = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='itens')
    disponivel = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
    
    def __str__(self):
        return self.nome