from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import os

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
    
    @property
    def average_rating(self):
        """Calcula a média das avaliações do produto"""
        reviews = self.reviews.filter(aprovado=True)
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            return round(total / reviews.count(), 1)
        return 0

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

class Review(models.Model):
    """
    Modelo para avaliações dos produtos pelos clientes
    """
    RATING_CHOICES = [
        (1, '1 - Muito Ruim'),
        (2, '2 - Ruim'),
        (3, '3 - Regular'),
        (4, '4 - Bom'),
        (5, '5 - Excelente'),
    ]
    
    produto = models.ForeignKey(Joais, on_delete=models.CASCADE, related_name='reviews')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Avaliação de 1 a 5 estrelas'
    )
    titulo = models.CharField(max_length=100, blank=True, help_text='Título opcional da avaliação')
    comentario = models.TextField(help_text='Comentário detalhado sobre o produto')
    foto = models.ImageField(
        upload_to='reviews/',
        blank=True,
        null=True,
        help_text='Foto do cliente usando o produto (opcional)'
    )
    recomendado = models.BooleanField(default=True, help_text='Recomenda este produto?')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    aprovado = models.BooleanField(default=False, help_text='Avaliação aprovada pela moderação')
    
    class Meta:
        ordering = ['-data_criacao']
        unique_together = ['produto', 'usuario']  # Um usuário só pode avaliar um produto uma vez
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
    
    def __str__(self):
        return f'{self.usuario.username} - {self.produto.nome} ({self.rating}/5)'
    
    def get_rating_display_stars(self):
        """Retorna HTML para exibir as estrelas"""
        stars = ''
        for i in range(1, 6):
            if i <= self.rating:
                stars += '<i class="bi bi-star-fill text-warning"></i>'
            else:
                stars += '<i class="bi bi-star text-muted"></i>'
        return stars
    
    def get_rating_percentage(self):
        """Retorna a porcentagem do rating (para barras de progresso)"""
        return (self.rating / 5) * 100

class ReviewImage(models.Model):
    """
    Modelo para múltiplas fotos em uma avaliação
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='reviews/imagens/')
    legenda = models.CharField(max_length=200, blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Imagem da Avaliação'
        verbose_name_plural = 'Imagens das Avaliações'
    
    def __str__(self):
        return f'Imagem de {self.review.usuario.username}'