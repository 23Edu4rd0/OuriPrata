from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import SignUpForm

def login(request):
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