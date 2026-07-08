from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Joia, Categoria

def home(request):
    """
    Página inicial do portfólio
    """
    featured_products = Joia.objects.filter(destaque=True)[:8]
    categories = Categoria.objects.all()
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'landing_page/home.html', context)


def about(request):
    """
    Página 'Quem Somos'
    """
    return render(request, 'landing_page/sobre/about_us.html')


def contact(request):
    """
    Página de contato
    """
    return render(request, 'landing_page/contato/contact_us.html')


def policy(request):
    """
    Página de política de privacidade
    """
    return render(request, 'landing_page/politicas/privacy_policy.html')


def terms(request):
    """
    Página de termos de uso
    """
    return render(request, 'landing_page/politicas/terms_of_use.html')


def item_detail(request, slug):
    """
    Exibe detalhes de uma joia no portfólio
    """
    product = get_object_or_404(Joia, slug=slug)
    related_products = Joia.objects.filter(categoria=product.categoria).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'landing_page/produtos/product_detail.html', context)


def products_by_category(request, categoria_slug):
    """
    Lista produtos filtrados por uma categoria
    """
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    products = Joia.objects.filter(categoria=categoria)
    total_products = products.count()
    all_categories = Categoria.objects.all()
    
    page_title = categoria.nome
    page_subtitle = f"{total_products} joia{'' if total_products == 1 else 's'} encontrada{'' if total_products == 1 else 's'} nesta categoria"
    
    breadcrumbs = [
        {'name': 'Portfólio', 'url': '/catalogo/'},
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
    Mostra todas as joias do portfólio
    """
    products = Joia.objects.all()
    total_products = products.count()
    all_categories = Categoria.objects.all()
    
    page_title = "Portfólio de Joias"
    page_subtitle = f"{total_products} joia{'' if total_products == 1 else 's'} para você se inspirar"
    
    breadcrumbs = [
        {'name': 'Portfólio', 'url': None}
    ]
    
    context = {
        'products': products,
        'total_products': total_products,
        'all_categories': all_categories,
        'current_page': 'catalogo',
        'page_title': page_title,
        'page_subtitle': page_subtitle,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'landing_page/produtos/all_products.html', context)


def search_products(request):
    """
    Pesquisa joias por nome ou descrição com filtros
    """
    query = request.GET.get('q', '').strip()
    categoria_filter = request.GET.get('categoria', '').strip()
    
    products = Joia.objects.all()
    
    if query:
        products = products.filter(
            Q(nome__icontains=query) | 
            Q(descricao__icontains=query)
        ).distinct()
    
    if categoria_filter:
        try:
            categoria = Categoria.objects.get(slug=categoria_filter)
            products = products.filter(categoria=categoria)
        except Categoria.DoesNotExist:
            pass
            
    total_products = products.count()
    all_categories = Categoria.objects.all()
    
    if query:
        page_title = "Resultados da Busca"
        page_subtitle = f"{total_products} joia{'' if total_products == 1 else 's'} encontrada{'' if total_products == 1 else 's'} para \"{query}\""
    else:
        page_title = "Buscar no Portfólio"
        page_subtitle = "Encontre a joia perfeita para você"
        
    breadcrumbs = [
        {'name': 'Busca', 'url': None}
    ]
    
    context = {
        'products': products,
        'total_products': total_products,
        'search_query': query,
        'categoria_filter': categoria_filter,
        'all_categories': all_categories,
        'current_page': 'search',
        'page_title': page_title,
        'page_subtitle': page_subtitle,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'landing_page/produtos/search_results.html', context)


def search_suggestions(request):
    """
    Retorna sugestões de joias via AJAX para a busca rápida
    """
    query = request.GET.get('q', '').strip()
    suggestions = []
    if query and len(query) >= 2:
        products = Joia.objects.filter(
            Q(nome__icontains=query) | 
            Q(descricao__icontains=query)
        ).distinct()[:8]
        for product in products:
            suggestions.append({
                'id': product.id,
                'nome': product.nome,
                'slug': product.slug,
                'imagem': product.imagem.url if product.imagem else None,
            })
    return JsonResponse({
        'suggestions': suggestions,
        'query': query
    })
