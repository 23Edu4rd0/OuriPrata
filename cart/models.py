from django.db import models
from django.contrib.auth.models import User
from catalogo.models import Joais

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Joais, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    ring_size = models.CharField(max_length=5, blank=True, null=True, verbose_name="Tamanho do Anel")
    data_adicionado = models.DateTimeField(auto_now_add=True)
    data_atualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'produto', 'ring_size')  # Permite mesmo produto com tamanhos diferentes
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"
    
    def __str__(self):
        size_info = f" (Tam. {self.ring_size})" if self.ring_size else ""
        return f"{self.user.username} - {self.produto.nome}{size_info} ({self.quantidade})"
    
    @property
    def total_item(self):
        """Calcula o total do item (preço * quantidade)"""
        preco = self.produto.preco_promocional if self.produto.em_promocao and self.produto.preco_promocional else self.produto.preco
        return preco * self.quantidade
