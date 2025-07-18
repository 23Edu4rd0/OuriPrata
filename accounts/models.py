from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Dados de endereço
    cep = models.CharField(max_length=9, blank=True, null=True, help_text="Formato: 12345-678")
    endereco = models.CharField(max_length=200, blank=True, null=True, verbose_name="Logradouro")
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    
    # Campos calculados automaticamente
    eh_divinopolis = models.BooleanField(default=False, verbose_name="É de Divinópolis")
    frete_gratuito = models.BooleanField(default=False, verbose_name="Tem frete grátis")
    
    # Controle
    endereco_completo = models.BooleanField(default=False, verbose_name="Endereço completo")
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    def endereco_formatado(self):
        """Retorna o endereço formatado para exibição"""
        if not self.endereco_completo:
            return "Endereço não informado"
        
        endereco_parts = [
            f"{self.endereco}, {self.numero}",
            self.complemento if self.complemento else None,
            self.bairro,
            f"{self.cidade}/{self.estado}",
            self.cep
        ]
        
        return " - ".join([part for part in endereco_parts if part])
    
    def verificar_divinopolis(self):
        """Verifica se o endereço é de Divinópolis e atualiza as flags"""
        if not self.cidade or not self.estado:
            return False
        
        # Verificar por cidade e estado
        eh_divinopolis = (
            self.cidade.upper().strip() in ['DIVINÓPOLIS', 'DIVINOPOLIS'] and 
            self.estado.upper().strip() == 'MG'
        )
        
        # Verificar também por CEP (faixa 35500-000 a 35599-999)
        if self.cep and self.cep.replace('-', '').replace('.', '').startswith('355'):
            eh_divinopolis = True
        
        # Atualizar flags
        self.eh_divinopolis = eh_divinopolis
        self.frete_gratuito = eh_divinopolis
        
        return eh_divinopolis
    
    def verificar_endereco_completo(self):
        """Verifica se o endereço está completo"""
        campos_obrigatorios = [
            self.cep, self.endereco, self.numero, 
            self.bairro, self.cidade, self.estado
        ]
        
        completo = all(campo and str(campo).strip() for campo in campos_obrigatorios)
        self.endereco_completo = completo
        
        return completo
    
    def save(self, *args, **kwargs):
        """Override do save para verificar automaticamente Divinópolis"""
        self.verificar_endereco_completo()
        if self.endereco_completo:
            self.verificar_divinopolis()
        
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Cria o perfil automaticamente quando um usuário é criado"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Salva o perfil quando o usuário é salvo"""
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
