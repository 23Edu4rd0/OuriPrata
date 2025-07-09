from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'landing_page/index.html')

def contact(request):
    return render(request, 'landing_page/contact.html')

def items(request):
    return HttpResponse('<h1>Just testing, never mind.</h1>')

def about(request):
    return render(request, 'landing_page/about.html')

def policy(request):
    return render(request, 'landing_page/private_policy.html')

def product(request):
    return render(request, 'landing_page/product.html')