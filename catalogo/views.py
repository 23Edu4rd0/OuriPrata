from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    return render(request, 'landing_page/index.html')

def contact(request):
    template = loader.get_template('landing_page/contact.html')
    return HttpResponse(template.render())

def items(request):
    return HttpResponse('<h1>Just testing, never mind.</h1>')

def about(request):
    return render(request, 'landing_page/about.html')

def policy(request):
    return render(request, 'landing_page/private_policy.html')