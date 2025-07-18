from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from catalogo.models import Joais, Categorias
from django.db.models import Q
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

    # Verificar se o usuário está logado e tem perfil completo para mostrar o botão de compra
    show_buy_button = False
    frete_info = {
        'valor': 35.00,
        'tipo': 'Correios',
        'prazo': '5-10 dias úteis',
        'gratuito': False,
        'descricao': '(Frete será calculado após login)'
    }
    
    if request.user.is_authenticated:
        try:
            from accounts.models import UserProfile
            profile = request.user.userprofile
            
            if profile.endereco_completo:
                show_buy_button = True
                # Calcular informações de frete
                if profile.eh_divinopolis:
                    frete_info = {
                        'valor': 0.00,
                        'tipo': 'Entrega local gratuita',
                        'prazo': '1-2 dias úteis',
                        'gratuito': True,
                        'descricao': 'Frete GRÁTIS - Divinópolis'
                    }
                else:
                    frete_info = {
                        'valor': 35.00,  # Valor realista para frete
                        'tipo': 'Correios',
                        'prazo': '5-10 dias úteis',
                        'gratuito': False,
                        'descricao': 'Frete: R$ 35,00'
                    }
        except:
            # Se não tem perfil, não mostra botão de compra
            pass

    # Só processar pagamento se for POST e usuário tiver perfil completo
    if request.method == 'POST' and show_buy_button:
        try:
            sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
            base_url = "http://127.0.0.1:8000"
            
            # Calcular preço final (produto + frete)
            preco_final = float(product.preco_promocional if product.em_promocao and product.preco_promocional else product.preco)
            if frete_info and not frete_info['gratuito']:
                preco_final += frete_info['valor']
            
            preference_data = {
                "items": [
                    {
                        "title": product.nome,
                        "quantity": 1,
                        "unit_price": preco_final,
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
                    'related_products': related_products,
                    'show_buy_button': show_buy_button,
                    'frete_info': frete_info
                })
            else:
                return render(request, 'landing_page/product_detail.html', {
                    'product': product,
                    'error': 'Erro ao processar pagamento. Tente novamente.',
                    'related_products': related_products,
                    'show_buy_button': show_buy_button,
                    'frete_info': frete_info
                })
        except Exception as e:
            return render(request, 'landing_page/product_detail.html', {
                'product': product,
                'error': 'Serviço de pagamento temporariamente indisponível.',
                'related_products': related_products,
                'show_buy_button': show_buy_button,
                'frete_info': frete_info
            })
    
    # GET request ou usuário sem perfil completo
    return render(request, 'landing_page/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'show_buy_button': show_buy_button,
        'frete_info': frete_info
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
    
    # Configurar dados para os partials
    page_title = categoria.nome
    page_subtitle = f"{total_products} produto{'' if total_products == 1 else 's'} encontrado{'' if total_products == 1 else 's'} nesta categoria"
    breadcrumbs = [
        {'name': 'Catálogo', 'url': '/catalogo/'},
        {'name': categoria.nome, 'url': None}
    ]
    
    return render(request, 'landing_page/products_by_category.html', {
        'products': products,
        'categoria': categoria,
        'current_categoria': categoria,
        'total_products': total_products,
        'all_categories': all_categories,
        'current_page': 'categoria',
        'page_title': page_title,
        'page_subtitle': page_subtitle,
        'breadcrumbs': breadcrumbs,
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
    
    # Configurar dados para os partials
    if show_only_promotions:
        page_title = "Produtos em Promoção"
        page_subtitle = f"{total_products} produto{'' if total_products == 1 else 's'} em oferta especial"
        breadcrumbs = [
            {'name': 'Catálogo', 'url': '/catalogo/'},
            {'name': 'Promoções', 'url': None}
        ]
    else:
        page_title = "Catálogo Completo"
        page_subtitle = f"{total_products} produto{'' if total_products == 1 else 's'} disponíve{'l' if total_products == 1 else 'is'}"
        breadcrumbs = [
            {'name': 'Catálogo', 'url': None}
        ]
    
    return render(request, 'landing_page/all_products.html', {
        'products': products,
        'total_products': total_products,
        'all_categories': all_categories,
        'show_only_promotions': show_only_promotions,
        'current_page': 'catalogo',
        'page_title': page_title,
        'page_subtitle': page_subtitle,
        'breadcrumbs': breadcrumbs,
    })

def search_products(request):
    """
    View para pesquisar produtos por nome ou descrição
    """
    query = request.GET.get('q', '').strip()
    products = []
    total_products = 0
    
    if query:
        # Buscar produtos que contenham o termo no nome ou descrição
        products = Joais.objects.filter(
            Q(nome__icontains=query) | 
            Q(descricao__icontains=query)
        ).distinct()
        total_products = products.count()
    
    # Buscar todas as categorias para o filtro lateral
    all_categories = Categorias.objects.all()
    
    # Configurar dados para os partials
    if query:
        page_title = "Resultados da Pesquisa"
        page_subtitle = f"{total_products} produto{'' if total_products == 1 else 's'} encontrado{'' if total_products == 1 else 's'} para \"{query}\""
    else:
        page_title = "Pesquisar Produtos"
        page_subtitle = "Digite algo para pesquisar nossos produtos"
    
    breadcrumbs = [
        {'name': 'Pesquisa', 'url': None}
    ]
    
    context = {
        'products': products,
        'total_products': total_products,
        'search_query': query,
        'all_categories': all_categories,
        'current_page': 'search',
        'page_title': page_title,
        'page_subtitle': page_subtitle,
        'breadcrumbs': breadcrumbs,
    }
    
    return render(request, 'landing_page/search_results.html', context)

def search_suggestions(request):
    """
    View para retornar sugestões de produtos via AJAX
    """
    query = request.GET.get('q', '').strip()
    suggestions = []
    
    if query and len(query) >= 2:  # Só buscar se tiver pelo menos 2 caracteres
        # Buscar produtos que contenham o termo no nome ou descrição
        products = Joais.objects.filter(
            Q(nome__icontains=query) | 
            Q(descricao__icontains=query)
        ).distinct()[:8]  # Limitar a 8 sugestões
        
        for product in products:
            suggestions.append({
                'id': product.id,
                'nome': product.nome,
                'preco': str(product.preco),
                'preco_promocional': str(product.preco_promocional) if product.preco_promocional else None,
                'em_promocao': product.em_promocao,
                'slug': product.slug,
                'imagem': product.imagem.url if product.imagem else None,
            })
    
    return JsonResponse({
        'suggestions': suggestions,
        'query': query
    })

def checkout(request, product_slug):
    """
    View para iniciar o checkout - verifica se o usuário tem perfil completo
    """
    if not request.user.is_authenticated:
        # Salvar a URL de destino e redirecionar para login
        request.session['next_url'] = request.get_full_path()
        return redirect('login')
    
    # Verificar se o produto existe
    product = get_object_or_404(Joais, slug=product_slug)
    
    try:
        from accounts.models import UserProfile
        profile = request.user.userprofile
        
        # Verificar se o perfil está completo
        if not profile.endereco_completo:
            # Redirecionar para completar perfil com parâmetro next
            return redirect(f'/accounts/complete-profile/?next={request.get_full_path()}')
        
        # Perfil completo, processar checkout
        return item_detail(request, product_slug)
        
    except UserProfile.DoesNotExist:
        # Usuário não tem perfil, redirecionar para completar
        return redirect(f'/accounts/complete-profile/?next={request.get_full_path()}')
