from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'accounts/login.html')

def sing_up(request):
    return render(request, 'accounts/sing_up.html')