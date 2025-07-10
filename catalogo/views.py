from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'landing_page/home.html')

def contact(request):
    return render(request, 'landing_page/contact_us.html')

def items(request):
    return HttpResponse('<h1>Just testing, never mind.</h1>')

def about(request):
    return render(request, 'landing_page/about_us.html')

def policy(request):
    return render(request, 'landing_page/privacy_policy.html')

def product(request):
    return render(request, 'landing_page/product_detail.html')