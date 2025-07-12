from django.shortcuts import render, get_object_or_404
from catalogo.models import Joais

def home(request):
    products = Joais.objects.all()
    return render(request, 'landing_page/home.html', {'products': products})

def item_detail(request, slug):
    product = get_object_or_404(Joais, slug=slug)  
    return render(request, 'landing_page/product_detail.html', {'product': product})

def contact(request):
    return render(request, 'landing_page/contact_us.html')

def about(request):
    return render(request, 'landing_page/about_us.html')

def policy(request):
    return render(request, 'landing_page/privacy_policy.html')

def product(request):
    return render(request, 'landing_page/product_detail.html')
