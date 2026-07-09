from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category


def home(request):
    featured_products = Product.objects.filter(featured=True)[:8]
    categories = Category.objects.all()
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'landing_page/home.html', context)


def about(request):
    return render(request, 'landing_page/sobre/about_us.html')


def contact(request):
    return render(request, 'landing_page/contato/contact_us.html')


def policy(request):
    return render(request, 'landing_page/politicas/privacy_policy.html')


def terms(request):
    return render(request, 'landing_page/politicas/terms_of_use.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(
        request, 'landing_page/produtos/product_detail.html', context
    )


def all_products(request):
    products = Product.objects.all()
    total_products = products.count()
    all_categories = Category.objects.all()

    context = {
        'products': products,
        'total_products': total_products,
        'all_categories': all_categories,
        'current_page': 'catalogo',
        'current_category': None,
        'page_title': 'Full Collection',
        'page_subtitle': f'{total_products} piece{"" if total_products == 1 else "s"} to inspire you',
        'breadcrumbs': [{'name': 'Portfolio', 'url': None}],
    }
    return render(request, 'landing_page/produtos/all_products.html', context)


def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    total_products = products.count()
    all_categories = Category.objects.all()

    context = {
        'products': products,
        'total_products': total_products,
        'all_categories': all_categories,
        'current_page': 'categoria',
        'current_category': category,
        'page_title': category.name,
        'page_subtitle': f'{total_products} piece{"" if total_products == 1 else "s"} found in this category',
        'breadcrumbs': [
            {'name': 'Portfolio', 'url': '/catalogo/'},
            {'name': category.name, 'url': None},
        ],
    }
    return render(request, 'landing_page/produtos/all_products.html', context)


def search_products(request):
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('categoria', '').strip()

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()

    if category_filter:
        try:
            category = Category.objects.get(slug=category_filter)
            products = products.filter(category=category)
        except Category.DoesNotExist:
            pass

    total_products = products.count()
    all_categories = Category.objects.all()

    if query:
        page_title = 'Resultados da Busca'
        page_subtitle = f'{total_products} peça{"" if total_products == 1 else "s"} encontrada{"" if total_products == 1 else "s"} para "{query}"'
    else:
        page_title = 'Buscar no Portfólio'
        page_subtitle = 'Encontre a peça perfeita para você'

    context = {
        'products': products,
        'total_products': total_products,
        'search_query': query,
        'category_filter': category_filter,
        'all_categories': all_categories,
        'current_page': 'search',
        'page_title': page_title,
        'page_subtitle': page_subtitle,
        'breadcrumbs': [{'name': 'Busca', 'url': None}],
    }
    return render(
        request, 'landing_page/produtos/search_results.html', context
    )

def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    suggestions = []
    if query and len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()[:8]
        for product in products:
            suggestions.append({
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'image': product.image.url if product.image else None,
            })
    return JsonResponse({'suggestions': suggestions, 'query': query})