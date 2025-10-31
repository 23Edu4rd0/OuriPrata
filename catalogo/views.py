from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from catalogo.models import Joais, Categorias, Review, ReviewImage
from django.db.models import Q, Avg, Count, F
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
import json
import logging

def home(request):
    """
    View para a página inicial do catálogo
    """
    # Buscar todos os produtos para os templates
    products = Joais.objects.all()
    # Buscar categorias
    categories = Categorias.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'landing_page/home.html', context)

def about(request):
    """
    View para a página 'Quem Somos'
    """
    return render(request, 'landing_page/sobre/about_us.html')

def contact(request):
    """
    View para a página de contato
    """
    return render(request, 'landing_page/contato/contact_us.html')

def policy(request):
    """
    View para a página de política de privacidade
    """
    return render(request, 'landing_page/politicas/privacy_policy.html')

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
    
    # Verificar se o usuário já avaliou este produto
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(produto=product, usuario=request.user).first()
    
    # Buscar todas as reviews do produto
    reviews = Review.objects.filter(produto=product).order_by('-data_criacao')
    
    # Calcular distribuição das avaliações
    rating_distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    total_reviews = reviews.count()
    
    for review in reviews:
        if review.rating in rating_distribution:
            rating_distribution[review.rating] += 1
    
    # Calcular porcentagens para cada rating
    rating_percentages = {}
    for rating in range(1, 6):
        if total_reviews > 0:
            rating_percentages[rating] = (rating_distribution[rating] / total_reviews) * 100
        else:
            rating_percentages[rating] = 0
    
    context = {
        'product': product,
        'show_buy_button': show_buy_button,
        'frete_info': frete_info,
        'preference_id': preference_id,
        'mercado_pago_public_key': mercado_pago_public_key,
        'related_products': Joais.objects.filter(categoria=product.categoria).exclude(id=product.id)[:4],
        'user_review': user_review,
        'reviews': reviews,
        'rating_distribution': rating_distribution,
        'rating_percentages': rating_percentages,
        'total_reviews': total_reviews,
    }
    return render(request, 'landing_page/produtos/product_detail.html', context)


@login_required
def meus_pedidos(request):
    from pagamentos.models import Pedido
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data_criacao')
    return render(request, 'landing_page/pedidos/meus_pedidos.html', {'pedidos': pedidos})


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
    return render(request, 'landing_page/produtos/products_by_category.html', context)

def all_products(request):
    """
    View para mostrar todos os produtos do catálogo
    """
    products = Joais.objects.all()
    promocoes_param = request.GET.get('promocoes', '').lower()
    show_only_promotions = promocoes_param in ['true', '1', 'sim', 'yes']
    
    if show_only_promotions:
        products = products.filter(
            em_promocao=True,
            preco_promocional__isnull=False,
            preco_promocional__gt=0,
            preco_promocional__lt=F('preco')
        )
    
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
        'auto_activate_promotion_filter': show_only_promotions,  # Para ativar o filtro automaticamente
    }
    return render(request, 'landing_page/produtos/all_products.html', context)

def search_products(request):
    """
    View para pesquisar produtos por nome ou descrição com filtros avançados
    """
    query = request.GET.get('q', '').strip()
    categoria_filter = request.GET.get('categoria', '').strip()
    preco_filter = request.GET.get('preco', '').strip()
    
    products = Joais.objects.all()
    total_products = 0
    
    if query:
        # Busca básica por nome ou descrição
        products = products.filter(
            Q(nome__icontains=query) | 
            Q(descricao__icontains=query)
        ).distinct()
    
    # Filtro por categoria
    if categoria_filter:
        try:
            categoria = Categorias.objects.get(slug=categoria_filter)
            products = products.filter(categoria=categoria)
        except Categorias.DoesNotExist:
            pass
    
    # Filtro por preço
    if preco_filter:
        if preco_filter == '0-100':
            products = products.filter(preco__lte=100)
        elif preco_filter == '100-300':
            products = products.filter(preco__gte=100, preco__lte=300)
        elif preco_filter == '300-500':
            products = products.filter(preco__gte=300, preco__lte=500)
        elif preco_filter == '500+':
            products = products.filter(preco__gte=500)
    
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
        'categoria_filter': categoria_filter,
        'preco_filter': preco_filter,
        'all_categories': all_categories,
        'current_page': 'search',
        'page_title': page_title,
        'page_subtitle': page_subtitle,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'landing_page/produtos/search_results.html', context)

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

@login_required
def add_review(request, product_slug):
    """
    View para adicionar uma avaliação a um produto
    """
    if request.method == 'POST':
        product = get_object_or_404(Joais, slug=product_slug)
        
        # Verificar se o usuário já avaliou este produto
        existing_review = Review.objects.filter(produto=product, usuario=request.user).first()
        if existing_review:
            return JsonResponse({
                'status': 'error',
                'message': 'Você já avaliou este produto.'
            })
        
        # Verificar se o usuário está logado
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'Você precisa estar logado para avaliar.'
            })
        
        try:
            rating_raw = request.POST.get('rating', 0)
            title = request.POST.get('title', '').strip()
            comment = request.POST.get('comment', '').strip()
            
            # Tentar converter rating
            try:
                rating = int(rating_raw)
            except (ValueError, TypeError) as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Rating inválido: {rating_raw}. Deve ser um número entre 1 e 5.'
                })
            
            if rating < 1 or rating > 5:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Avaliação deve ser entre 1 e 5 estrelas.'
                })
            
            if not comment:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Comentário é obrigatório.'
                })
            
            # Criar a avaliação
            review = Review.objects.create(
                produto=product,
                usuario=request.user,
                rating=rating,
                titulo=title,
                comentario=comment,
                aprovado=True  # Auto-aprovar para usuários logados
            )
            
            # Processar imagens se fornecidas
            if 'images' in request.FILES:
                for image_file in request.FILES.getlist('images'):
                    if image_file.size <= 5 * 1024 * 1024:  # 5MB limit
                        try:
                            ReviewImage.objects.create(
                                review=review,
                                imagem=image_file
                            )
                        except Exception as e:
                            print(f"Error saving image {image_file.name}: {e}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Avaliação enviada com sucesso!'
            })
            
        except (ValueError, TypeError) as e:
            logging.exception("Erro ao processar avaliação do produto.")
            return JsonResponse({
                'status': 'error',
                'message': 'Dados inválidos fornecidos.'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Método não permitido.'
    })

@login_required
def edit_review(request, review_id):
    """
    View para editar uma avaliação existente
    """
    review = get_object_or_404(Review, id=review_id, usuario=request.user)
    
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating', 0))
            title = request.POST.get('title', '').strip()
            comment = request.POST.get('comment', '').strip()
            
            if rating < 1 or rating > 5:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Avaliação deve ser entre 1 e 5 estrelas.'
                })
            
            if not comment:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Comentário é obrigatório.'
                })
            
            # Atualizar a avaliação
            review.rating = rating
            review.titulo = title
            review.comentario = comment
            review.save()
            
            # Processar imagens se fornecidas
            if 'images' in request.FILES:
                # Remover imagens antigas
                review.imagens.all().delete()
                
                # Adicionar novas imagens
                for image_file in request.FILES.getlist('images'):
                    if image_file.size <= 5 * 1024 * 1024:  # 5MB limit
                        try:
                            ReviewImage.objects.create(
                                review=review,
                                imagem=image_file
                            )
                        except Exception as e:
                            print(f"Error saving image in edit {image_file.name}: {e}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Avaliação atualizada com sucesso!'
            })
            
        except (ValueError, TypeError):
            return JsonResponse({
                'status': 'error',
                'message': 'Dados inválidos fornecidos.'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Método não permitido.'
    })

@login_required
def delete_review(request, review_id):
    """
    View para deletar uma avaliação
    """
    review = get_object_or_404(Review, id=review_id, usuario=request.user)
    
    if request.method == 'POST':
        review.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Avaliação removida com sucesso!'
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Método não permitido.'
    })

def get_product_reviews(request, product_slug):
    """
    View para obter avaliações de um produto via AJAX
    """
    product = get_object_or_404(Joais, slug=product_slug)
    rating_filter = request.GET.get('rating', '')
    page = request.GET.get('page', 1)
    
    # Filtrar avaliações aprovadas
    reviews = Review.objects.filter(produto=product, aprovado=True)
    
    # Aplicar filtro de rating se especificado
    if rating_filter and rating_filter.isdigit():
        rating = int(rating_filter)
        if 1 <= rating <= 5:
            reviews = reviews.filter(rating=rating)
    
    # Paginação
    paginator = Paginator(reviews, 5)  # 5 avaliações por página
    reviews_page = paginator.get_page(page)
    
    # Calcular estatísticas
    total_reviews = reviews.count()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    rating_distribution = reviews.values('rating').annotate(count=Count('rating')).order_by('rating')
    
    # Converter para lista de dicionários para JSON
    reviews_data = []
    for review in reviews_page:
        reviews_data.append({
            'id': review.id,
            'usuario': review.usuario.username,
            'rating': review.rating,
            'titulo': review.titulo,
            'comentario': review.comentario,
            'foto_url': review.foto.url if review.foto else None,
            'recomendado': review.recomendado,
            'data_criacao': review.data_criacao.strftime('%d/%m/%Y'),
            'can_edit': request.user == review.usuario,
        })
    
    return JsonResponse({
        'reviews': reviews_data,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 1),
        'rating_distribution': list(rating_distribution),
        'has_next': reviews_page.has_next(),
        'has_previous': reviews_page.has_previous(),
        'current_page': reviews_page.number,
        'total_pages': reviews_page.paginator.num_pages,
    })
