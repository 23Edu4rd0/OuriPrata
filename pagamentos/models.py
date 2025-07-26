from django.db import models
from django.conf import settings
from catalogo.models import Joais

# Modelo para registrar pedidos
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produto = models.ForeignKey('catalogo.Joais', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    valor_produto = models.DecimalField(max_digits=10, decimal_places=2)
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_frete = models.CharField(max_length=50)
    prazo_frete = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    mercado_pago_id = models.CharField(max_length=100, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def valor_total(self):
        return self.valor_produto + self.valor_frete

    def __str__(self):
        return f"Pedido #{self.id} - {self.produto.nome} ({self.get_status_display()})"
from django.db import models

# Create your models here.
