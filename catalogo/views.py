from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from catalogo.models import Joais
import json
import mercadopago
from django.conf import settings

def home(request):
    products = Joais.objects.all()
    return render(request, 'landing_page/home.html', {'products': products})

def login(request):
    return render(request, 'landing_page/login.html')

def sing_up(request):
    return render(request, 'landing_page/sing_up.html')

def item_detail(request, slug):
    product = get_object_or_404(Joais, slug=slug)
    product.preco = round(float(product.preco),2)

    # Produtos relacionados (exemplo: destaque=True, exclui o atual)
    related_products = Joais.objects.filter(destaque=True).exclude(id=product.id)[:4]

    try:
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        base_url = "https://9d8ce638b45f.ngrok-free.app"
        preference_data = {
            "items": [
                {
                    "title": product.nome,
                    "quantity": 1,
                    "unit_price": product.preco,
                }
            ],
            "back_urls": {
                "success": f"{base_url}/sucesso/",
                "failure": f"{base_url}/erro/",
                "pending": f"{base_url}/pendente/"
            },
            "auto_return": "approved"
        }
        preference_response = sdk.preference().create(preference_data)
        if preference_response["status"] == 201:
            preference = preference_response["response"]
            preference_id = preference.get("id")
            return render(request, 'landing_page/product_detail.html', {
                'product': product,
                'preference_id': preference_id,
                'mercado_pago_public_key': settings.MERCADO_PAGO_PUBLIC_KEY,
                'related_products': related_products
            })
        else:
            return render(request, 'landing_page/product_detail.html', {
                'product': product,
                'error': 'Erro ao processar pagamento. Tente novamente.',
                'related_products': related_products
            })
    except Exception as e:
        return render(request, 'landing_page/product_detail.html', {
            'product': product,
            'error': 'Serviço de pagamento temporariamente indisponível.',
            'related_products': related_products
        })
    
def contact(request):
    return render(request, 'landing_page/contact_us.html')

def about(request):
    return render(request, 'landing_page/about_us.html')

def policy(request):
    return render(request, 'landing_page/privacy_policy.html')

def webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('Webhook do Mercado Pago recebido:', data)
            
            # Aqui você pode processar os dados do webhook
            # Por exemplo, atualizar o status do pedido no banco de dados
            
            return JsonResponse({'status': 'success', 'message': 'Webhook received successfully'})
        except json.JSONDecodeError:
            print('Erro ao decodificar JSON do webhook')
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f'Erro no webhook: {str(e)}')
            return JsonResponse({'error': 'Internal server error'}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def pagamento_sucesso(request):
    return render(request, 'landing_page/pagamento_sucesso.html')

def pagamento_erro(request):
    return render(request, 'landing_page/pagamento_erro.html')

def pagamento_pendente(request):
    return render(request, 'landing_page/pagamento_pendente.html')
