from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import SignUpForm
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login realizado com sucesso.')
                return redirect('home')
            else:
                messages.error(request, 'E-mail ou senha inválidos.')
        except User.DoesNotExist:
            messages.error(request, 'E-mail não encontrado.')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            password = form.cleaned_data['password1']
            user_obj = User.objects.get(email=user.email)
            user_auth = authenticate(request, username=user_obj.username, password=password)
            if user_auth is not None:
                auth_login(request, user_auth)
                messages.success(request, f'Conta criada com sucesso para {user.email}. Você está logado agora.')
                return redirect('home')
        else:
            messages.error(request, 'Erro ao criar conta. Por favor, verifique os dados e tente novamente.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect('home')

def privacy_policy(request):
    return render(request, 'accounts/privacy_policy.html')

@login_required
def settings_view(request):
    return render(request, 'accounts/settings.html')

@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        password = request.POST.get('password')
        
        if not authenticate(username=request.user.username, password=password):
            messages.error(request, 'Senha incorreta.')
            return redirect('accounts:settings')
        
        if User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            messages.error(request, 'Este e-mail já está em uso por outro usuário.')
            return redirect('accounts:settings')
        
        request.user.email = new_email
        request.user.save()
        
        messages.success(request, 'E-mail alterado com sucesso!')
        return redirect('accounts:settings')
    
    return redirect('accounts:settings')

@login_required
def change_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()
        
        messages.success(request, 'Informações do perfil atualizadas com sucesso!')
        return redirect('accounts:settings')
    
    return redirect('accounts:settings')

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_delete = request.POST.get('confirm_delete')
        
        if not authenticate(username=request.user.username, password=password):
            messages.error(request, 'Senha incorreta.')
            return redirect('accounts:settings')
        
        if confirm_delete != 'EXCLUIR':
            messages.error(request, 'Por favor, digite "EXCLUIR" para confirmar.')
            return redirect('accounts:settings')
        
        username = request.user.username
        request.user.delete()
        
        messages.success(request, f'Sua conta foi excluída com sucesso.')
        return redirect('home')
    
    return redirect('accounts:settings')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not authenticate(username=request.user.username, password=current_password):
            messages.error(request, 'Senha atual incorreta.')
            return redirect('accounts:settings')
        
        if new_password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('accounts:settings')
        
        if len(new_password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return redirect('accounts:settings')
        
        request.user.set_password(new_password)
        request.user.save()
        
        auth_login(request, request.user)
        
        messages.success(request, 'Senha alterada com sucesso!')
        return redirect('accounts:settings')
    
    return redirect('accounts:settings')

@login_required
def complete_profile(request):
    """View para completar o perfil do usuário com endereço"""
    # Pegar ou criar o perfil
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Endereço salvo com sucesso!')
            
            # Verificar se veio de um checkout
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            return redirect('accounts:settings')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'accounts/complete_profile.html', {
        'form': form,
        'profile': profile
    })

@login_required
def check_profile_complete(request):
    """Verifica se o perfil está completo e redireciona se necessário"""
    try:
        profile = request.user.userprofile
        if not profile.endereco_completo:
            return redirect('complete_profile')
    except UserProfile.DoesNotExist:
        return redirect('complete_profile')
    
    return None  # Perfil está completo

def lookup_cep(request):
    """API para buscar dados do CEP via ViaCEP"""
    if request.method == 'GET':
        cep = request.GET.get('cep', '').replace('-', '').replace('.', '').replace(' ', '')
        
        if len(cep) != 8 or not cep.isdigit():
            return JsonResponse({'error': 'CEP inválido'}, status=400)
        
        try:
            response = requests.get(f'https://viacep.com.br/ws/{cep}/json/', timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'erro' in data:
                    return JsonResponse({'error': 'CEP não encontrado'}, status=404)
                
                # Verificar se é Divinópolis
                eh_divinopolis = (
                    data.get('localidade', '').upper() == 'DIVINÓPOLIS' and 
                    data.get('uf', '').upper() == 'MG'
                )
                
                return JsonResponse({
                    'endereco': data.get('logradouro', ''),
                    'bairro': data.get('bairro', ''),
                    'cidade': data.get('localidade', ''),
                    'estado': data.get('uf', ''),
                    'cep': f"{cep[:5]}-{cep[5:]}",
                    'eh_divinopolis': eh_divinopolis,
                    'frete_gratuito': eh_divinopolis
                })
            else:
                return JsonResponse({'error': 'Erro ao consultar CEP'}, status=500)
                
        except requests.RequestException:
            return JsonResponse({'error': 'Erro de conexão'}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def profile_view(request):
    """Exibe o perfil do usuário"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    
    # Calcular informações de frete
    frete_info = None
    if profile and profile.endereco_completo:
        if profile.eh_divinopolis:
            frete_info = {
                'tipo': 'Frete GRÁTIS',
                'descricao': 'Entrega local gratuita em Divinópolis',
                'prazo': '1-2 dias úteis',
                'valor': 0.00
            }
        else:
            frete_info = {
                'tipo': 'Correios',
                'descricao': 'Entrega via Correios',
                'prazo': '5-10 dias úteis',
                'valor': 35.00
            }
    
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'frete_info': frete_info
    })

@login_required
def edit_profile(request):
    """Permite ao usuário editar seu perfil/endereço"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            
            # Verificar se é Divinópolis
            cep_limpo = profile.cep.replace('-', '').replace(' ', '') if profile.cep else ''
            cidade_upper = profile.cidade.upper() if profile.cidade else ''
            estado_upper = profile.estado.upper() if profile.estado else ''
            
            profile.eh_divinopolis = (
                cep_limpo.startswith('355') or 
                (cidade_upper in ['DIVINÓPOLIS', 'DIVINOPOLIS'] and estado_upper == 'MG')
            )
            
            profile.save()
            messages.success(request, 'Endereço atualizado com sucesso!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'profile': profile
    })