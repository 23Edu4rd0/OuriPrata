from django import forms
from .models import UserProfile
import requests

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado']
        widgets = {
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345-678',
                'maxlength': '9',
                'id': 'cep'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, Avenida, etc.',
                'id': 'endereco'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número',
                'id': 'numero'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apto, casa, etc. (opcional)',
                'id': 'complemento'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bairro',
                'id': 'bairro'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade',
                'id': 'cidade'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UF',
                'maxlength': '2',
                'id': 'estado'
            }),
        }
        labels = {
            'cep': 'CEP',
            'endereco': 'Endereço',
            'numero': 'Número',
            'complemento': 'Complemento',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'Estado (UF)',
        }
    
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            # Remove formatação
            cep = cep.replace('-', '').replace('.', '').replace(' ', '')
            
            # Valida formato
            if len(cep) != 8 or not cep.isdigit():
                raise forms.ValidationError('CEP deve ter 8 dígitos.')
            
            # Formata corretamente
            cep = f"{cep[:5]}-{cep[5:]}"
            
            return cep
        return cep
    
    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        if estado:
            return estado.upper().strip()
        return estado
    
    def clean_cidade(self):
        cidade = self.cleaned_data.get('cidade')
        if cidade:
            return cidade.title().strip()
        return cidade

class CepLookupForm(forms.Form):
    """Formulário simples para busca de CEP"""
    cep = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345-678',
            'id': 'cep-lookup'
        }),
        label='CEP'
    )
