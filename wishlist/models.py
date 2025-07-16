from django.db import models
from django.contrib.auth.models import User
from catalogo.models import Joais

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Joais, on_delete=models.CASCADE)
    data_adicionado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'produto')
        verbose_name = "Lista de Desejos"
        verbose_name_plural = "Listas de Desejos"
    
    def __str__(self):
        return f"{self.user.username} - {self.produto.nome}"
