from django.shortcuts import render
from django.http import HttpResponse
from catalogo.models import Joais

def index(request):
    products = Joais.objects.all()
    return render(request, 'landing_page/home.html', {'products': products})

def contact(request):
    return render(request, 'landing_page/contact_us.html')

def items(request):
    products = Joais.objects.all()
    return render(request, 'landing_page/items.html', {'products': products})

    return HttpResponse('<h1>Just testing, never mind.</h1>')

def about(request):
    return render(request, 'landing_page/about_us.html')

def policy(request):
    return render(request, 'landing_page/privacy_policy.html')

def product(request):
    return render(request, 'landing_page/product_detail.html')