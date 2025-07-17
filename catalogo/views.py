from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from catalogo.models import Joais, Categorias
import json
import mercadopago
from django.conf import settings

def home(request):
    products = Joais.objects.all()
    # Filtrar apenas as categorias desejadas
    categories = Categorias.objects.filter(nome__in=['Anéis', 'Brincos', 'Pulseiras', 'Colares'])
    return render(request, 'landing_page/home.html', {'products': products, 'categories': categories})

def item_detail(request, slug):
    product = get_object_or_404(Joais, slug=slug)
    product.preco = round(float(product.preco),2)

    # Produtos relacionados: mesma categoria primeiro, depois outros
    related_products = []
    
    # Buscar produtos da mesma categoria (excluindo o produto atual)
    if hasattr(product, 'categoria') and product.categoria:
        same_category = list(Joais.objects.filter(categoria=product.categoria).exclude(id=product.id)[:4])
        related_products.extend(same_category)
    
    # Se não tiver produtos suficientes da mesma categoria, completar com outros
    if len(related_products) < 4:
        additional_needed = 4 - len(related_products)
        other_products = list(Joais.objects.exclude(id=product.id).exclude(id__in=[p.id for p in related_products])[:additional_needed])
        related_products.extend(other_products)

    try:
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        base_url = "http://127.0.0.1:8000"
        preference_data = {
            "items": [
                {
                    "title": product.nome,
                    "quantity": 1,
                    "unit_price": float(product.preco),
                }
            ],
            "back_urls": {
                "success": f"{base_url}/sucesso/",
                "failure": f"{base_url}/erro/",
                "pending": f"{base_url}/pendente/"
            }
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

def products_by_category(request, categoria_slug):
    """
    View para mostrar produtos filtrados por categoria
    """
    # Buscar a categoria pelo slug
    try:
        categoria = get_object_or_404(Categorias, slug=categoria_slug)
    except:
        # Se não encontrar, redirecionar para home
        from django.shortcuts import redirect
        return redirect('home')
    
    # Filtrar produtos da categoria
    products = Joais.objects.filter(categoria=categoria)
    
    # Contar total de produtos
    total_products = products.count()
    
    # Buscar todas as categorias para o filtro lateral
    all_categories = Categorias.objects.all()
    
    return render(request, 'landing_page/products_by_category.html', {
        'products': products,
        'categoria': categoria,
        'total_products': total_products,
        'all_categories': all_categories
    })

def all_products(request):
    """
    View para mostrar todos os produtos do catálogo
    """
    # Buscar todos os produtos
    products = Joais.objects.all()
    
    # Verificar se deve filtrar apenas promoções
    show_only_promotions = request.GET.get('promocoes', '').lower() == 'true'
    
    if show_only_promotions:
        products = products.filter(em_promocao=True)
    
    # Contar total de produtos
    total_products = products.count()
    
    # Buscar todas as categorias para o filtro lateral
    all_categories = Categorias.objects.all()
    
    return render(request, 'landing_page/all_products.html', {
        'products': products,
        'total_products': total_products,
        'all_categories': all_categories,
        'show_only_promotions': show_only_promotions
    })
