from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import SignUpForm
from django.contrib.auth.decorators import login_required

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
            return redirect('settings')
        
        if User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            messages.error(request, 'Este e-mail já está em uso por outro usuário.')
            return redirect('settings')
        
        request.user.email = new_email
        request.user.save()
        
        messages.success(request, 'E-mail alterado com sucesso!')
        return redirect('settings')
    
    return redirect('settings')

@login_required
def change_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()
        
        messages.success(request, 'Informações do perfil atualizadas com sucesso!')
        return redirect('settings')
    
    return redirect('settings')

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_delete = request.POST.get('confirm_delete')
        
        if not authenticate(username=request.user.username, password=password):
            messages.error(request, 'Senha incorreta.')
            return redirect('settings')
        
        if confirm_delete != 'EXCLUIR':
            messages.error(request, 'Por favor, digite "EXCLUIR" para confirmar.')
            return redirect('settings')
        
        username = request.user.username
        request.user.delete()
        
        messages.success(request, f'Sua conta foi excluída com sucesso.')
        return redirect('home')
    
    return redirect('settings')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not authenticate(username=request.user.username, password=current_password):
            messages.error(request, 'Senha atual incorreta.')
            return redirect('settings')
        
        if new_password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('settings')
        
        if len(new_password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return redirect('settings')
        
        request.user.set_password(new_password)
        request.user.save()
        
        auth_login(request, request.user)
        
        messages.success(request, 'Senha alterada com sucesso!')
        return redirect('settings')
    
    return redirect('settings')