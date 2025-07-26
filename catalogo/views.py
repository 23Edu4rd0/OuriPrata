from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from catalogo.models import Joais, Categorias
from django.db.models import Q

def home(request):
    """
    View para a página inicial do catálogo
    """
    # Buscar todos os produtos para os templates
    products = Joais.objects.all()
    
    # Buscar produtos em promoção
    promotional_products = Joais.objects.filter(em_promocao=True)
    
    # Buscar categorias
    categories = Categorias.objects.all()
    
    context = {
        'products': products,
        'promotional_products': promotional_products,
        'categories': categories,
    }
    return render(request, 'landing_page/home.html', context)

def about(request):
    """
    View para a página 'Quem Somos'
    """
    return render(request, 'landing_page/about.html')

def contact(request):
    """
    View para a página de contato
    """
    return render(request, 'landing_page/contact_us.html')

def policy(request):
    """
    View para a página de política de privacidade
    """
    return render(request, 'landing_page/policy.html')

def item_detail(request, slug):
    """
    View para exibir detalhes de um produto
    """
    from django.conf import settings
    import mercadopago
    
    product = get_object_or_404(Joais, slug=slug)
    
    # Inicializar variáveis do contexto
    show_buy_button = False
    frete_info = None
    preference_id = None
    mercado_pago_public_key = None
    
    # Se usuário está logado, verificar se perfil está completo
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            show_buy_button = user_profile.endereco_completo
            if show_buy_button:
                frete_info = {
                    'gratuito': user_profile.frete_gratuito,
                    'valor': 0 if user_profile.frete_gratuito else 15.00,
                    'prazo': '3 dias úteis' if user_profile.frete_gratuito else '5-7 dias úteis'
                }
                
                # Configurar Mercado Pago
                access_token = settings.MERCADO_PAGO_ACCESS_TOKEN
                public_key = settings.MERCADO_PAGO_PUBLIC_KEY
                
                if access_token and public_key:
                    try:
                        sdk = mercadopago.SDK(access_token)
                        
                        # Calcular valores
                        if product.em_promocao and product.preco_promocional:
                            valor_produto = float(product.preco_promocional)
                        else:
                            valor_produto = float(product.preco)
                        
                        valor_frete = 0 if frete_info['gratuito'] else frete_info['valor']
                        valor_total = valor_produto + valor_frete
                        
                        # Criar preferência
                        preference_data = {
                            "items": [
                                {
                                    "title": product.nome,
                                    "description": product.descricao or "Produto OuriPrata",
                                    "quantity": 1,
                                    "currency_id": "BRL",
                                    "unit_price": valor_total
                                }
                            ],
                            "payer": {
                                "name": request.user.first_name or request.user.username,
                                "surname": request.user.last_name or "",
                                "email": request.user.email,
                            },
                            "back_urls": {
                                "success": request.build_absolute_uri(f"/pagamentos/sucesso/{product.slug}/"),
                                "failure": request.build_absolute_uri(f"/pagamentos/falha/{product.slug}/"),
                                "pending": request.build_absolute_uri(f"/pagamentos/pendente/{product.slug}/")
                            },
                            "auto_return": "approved",
                        }
                        
                        preference_response = sdk.preference().create(preference_data)
                        
                        if preference_response.get("status") == 201:
                            preference_id = preference_response["response"]["id"]
                            mercado_pago_public_key = public_key
                            
                            # Criar pedido
                            from pagamentos.models import Pedido
                            Pedido.objects.create(
                                usuario=request.user,
                                produto=product,
                                quantidade=1,
                                valor_produto=valor_produto,
                                valor_frete=valor_frete,
                                tipo_frete='Grátis' if frete_info['gratuito'] else 'Pago',
                                prazo_frete=frete_info['prazo'],
                                mercado_pago_id=preference_id,
                                status='pending'
                            )
                    except Exception:
                        pass
        except Exception:
            show_buy_button = False
    
    context = {
        'product': product,
        'show_buy_button': show_buy_button,
        'frete_info': frete_info,
        'preference_id': preference_id,
        'mercado_pago_public_key': mercado_pago_public_key,
        'related_products': Joais.objects.filter(categoria=product.categoria).exclude(id=product.id)[:4],
    }
    return render(request, 'landing_page/product_detail.html', context)


@login_required
def meus_pedidos(request):
    from pagamentos.models import Pedido
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data_criacao')
    return render(request, 'landing_page/meus_pedidos.html', {'pedidos': pedidos})


def products_by_category(request, categoria_slug):
    categoria = get_object_or_404(Categorias, slug=categoria_slug)
    products = Joais.objects.filter(categoria=categoria)
    total_products = products.count()
    all_categories = Categorias.objects.all()
    page_title = categoria.nome
    page_subtitle = f"{total_products} produto{'' if total_products == 1 else 's'} encontrado{'' if total_products == 1 else 's'} nesta categoria"
    breadcrumbs = [
        {'name': 'Catálogo', 'url': '/catalogo/'},
        {'name': categoria.nome, 'url': None}
    ]
    context = {
        'products': products,
        'total_products': total_products,
        'all_categories': all_categories,
        'current_page': 'categoria',
        'categoria': categoria,
        'page_title': page_title,
        'page_subtitle': page_subtitle,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'landing_page/product_list.html', context)

def all_products(request):
    """
    View para mostrar todos os produtos do catálogo
    """
    products = Joais.objects.all()
    show_only_promotions = request.GET.get('promocoes', '').lower() == 'true'
    if show_only_promotions:
        products = products.filter(em_promocao=True)
    total_products = products.count()
    all_categories = Categorias.objects.all()
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
    context = {
        'products': products,
        'total_products': total_products,
        'all_categories': all_categories,
        'show_only_promotions': show_only_promotions,
        'current_page': 'catalogo',
        'page_title': page_title,
        'page_subtitle': page_subtitle,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'landing_page/product_list.html', context)

def search_products(request):
    """
    View para pesquisar produtos por nome ou descrição
    """
    query = request.GET.get('q', '').strip()
    products = []
    total_products = 0
    if query:
        products = Joais.objects.filter(
            Q(nome__icontains=query) | 
            Q(descricao__icontains=query)
        ).distinct()
        total_products = products.count()
    all_categories = Categorias.objects.all()
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
    if query and len(query) >= 2:
        products = Joais.objects.filter(
            Q(nome__icontains=query) | 
            Q(descricao__icontains=query)
        ).distinct()[:8]
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
        request.session['next_url'] = request.get_full_path()
        return redirect('login')
    product = get_object_or_404(Joais, slug=product_slug)
    try:
        from accounts.models import UserProfile
        profile = request.user.userprofile
        if not profile.endereco_completo:
            return redirect(f'/accounts/complete-profile/?next={request.get_full_path()}')
        return redirect(f'/catalogo/{product_slug}/')
    except UserProfile.DoesNotExist:
        return redirect(f'/accounts/complete-profile/?next={request.get_full_path()}')
