from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from catalogo.models import Joais
import json
import mercadopago
from django.conf import settings

def home(request):
    products = Joais.objects.all()
    return render(request, 'landing_page/home.html', {'products': products})


def item_detail(request, slug):
    product = get_object_or_404(Joais, slug=slug)

    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title": product.nome,
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(product.preco)
            }
        ],
        "back_urls": {
            "success": "https://example.com/sucesso/",
            "failure": "https://example.com/erro/",
            "pending": "https://example.com/pendente/"
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    print(preference_response)  # <-- Isso mostra a resposta no terminal
    preference = preference_response["response"]
    preference_id = preference.get("id")

    return render(request, 'landing_page/product_detail.html', {
        'product': product,
        'preference_id': preference_id
    })
    
def contact(request):
    return render(request, 'landing_page/contact_us.html')

def about(request):
    return render(request, 'landing_page/about_us.html')

def policy(request):
    return render(request, 'landing_page/privacy_policy.html')

def webrook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print('webrook recebido: ', data)
        return JsonResponse({'status': 'success', 'message': 'Webhook received successfully'})
    return JsonResponse ({'error': 'metodo invalido'}, status=400)
