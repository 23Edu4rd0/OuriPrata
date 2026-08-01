from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Max, Avg, Count, F
from .models import Product, Category, Material, Occasion, Review, Collection, ProductVariant
from accounts.models import BrowsingHistory

SORT_OPTIONS = {
    'recentes': '-created_at',
    'preco_asc': 'price',
    'preco_desc': '-price',
}


def _filter_products(request, products):
    def _to_decimal(value):
        try:
            return Decimal(value.replace(',', '.'))
        except (AttributeError, InvalidOperation):
            return None

    preco_min = _to_decimal(request.GET.get('preco_min', ''))
    preco_max = _to_decimal(request.GET.get('preco_max', ''))
    material_id = request.GET.get('material', '').strip()
    occasion_id = request.GET.get('ocasiao', '').strip()
    gender = request.GET.get('genero', '').strip()
    sort = request.GET.get('ordenar', '').strip()

    if preco_min is not None:
        products = products.filter(price__gte=preco_min)
    if preco_max is not None:
        products = products.filter(price__lte=preco_max)
    if material_id.isdigit():
        products = products.filter(material_id=material_id)
    if occasion_id.isdigit():
        products = products.filter(occasion_id=occasion_id)
    if gender in dict(Product.GENDER_CHOICES):
        products = products.filter(gender=gender)
    if sort in SORT_OPTIONS:
        products = products.order_by(SORT_OPTIONS[sort])

    filter_context = {
        'materials': Material.objects.all(),
        'occasions': Occasion.objects.all(),
        'gender_choices': Product.GENDER_CHOICES,
        'selected_preco_min': request.GET.get('preco_min', ''),
        'selected_preco_max': request.GET.get('preco_max', ''),
        'selected_material': material_id,
        'selected_occasion': occasion_id,
        'selected_gender': gender,
        'selected_sort': sort,
    }
    return products, filter_context


def home(request):
    # 12 itens = 3 "páginas" de 4 no desktop para as setas do carrossel.
    featured_products = Product.objects.filter(featured=True)[:12]
    categories = Category.objects.all()
    new_arrivals = Product.objects.order_by("-created_at")[:12]
    featured_collections = Collection.objects.filter(featured=True).prefetch_related('products')[:4]

    # Promoções: promo_price preenchido e realmente menor que o preço normal.
    # O filtro roda no banco para não carregar o catálogo inteiro em memória.
    promo_products = Product.objects.filter(
        promo_price__isnull=False,
        price__isnull=False,
        promo_price__lt=F('price'),
    ).order_by('-created_at')[:12]

    season_collection = (
        Collection.objects.filter(is_season=True)
        .prefetch_related('products__category')
        .first()
    )
    season_products = list(season_collection.products.all()[:12]) if season_collection else []

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'new_arrivals': new_arrivals,
        'featured_collections': featured_collections,
        'promo_products': promo_products,
        'season_collection': season_collection,
        'season_products': season_products,
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

    reviews = product.reviews.select_related('user').all()
    review_stats = reviews.aggregate(avg=Avg('rating'), total=Count('id'))
    avg_rating = review_stats['avg'] or 0
    review_count = review_stats['total']
    user_review = None

    recently_viewed = []
    if request.user.is_authenticated:
        BrowsingHistory.objects.create(user=request.user, product=product)
        recent_ids = (
            BrowsingHistory.objects
            .filter(user=request.user)
            .exclude(product=product)
            .values('product_id')
            .annotate(last_viewed=Max('viewed_at'))
            .order_by('-last_viewed')
            .values_list('product_id', flat=True)[:4]
        )
        recently_viewed = list(Product.objects.filter(id__in=recent_ids))
        user_review = reviews.filter(user=request.user).first()

    variants = list(product.variants.all())

    context = {
        'product': product,
        'variants': variants,
        'related_products': related_products,
        'recently_viewed': recently_viewed,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'avg_rating_int': int(avg_rating),
        'review_count': review_count,
        'user_review': user_review,
        'rating_range': range(1, 6),
    }
    return render(
        request, 'landing_page/produtos/product_detail.html', context
    )


@login_required
def submit_review(request, slug):
    if request.method != 'POST':
        return JsonResponse({'error': 'method not allowed'}, status=405)

    product = get_object_or_404(Product, slug=slug)
    try:
        rating = int(request.POST.get('rating', 0))
    except ValueError:
        rating = 0

    if rating < 1 or rating > 5:
        return JsonResponse({'error': 'Nota inválida.'}, status=400)

    comment = request.POST.get('comment', '').strip()
    review, created = Review.objects.update_or_create(
        product=product,
        user=request.user,
        defaults={'rating': rating, 'comment': comment},
    )

    stats = product.reviews.aggregate(avg=Avg('rating'), total=Count('id'))
    return JsonResponse({
        'ok': True,
        'created': created,
        'rating': review.rating,
        'comment': review.comment,
        'username': request.user.get_full_name() or request.user.username,
        'date': review.created_at.strftime('%d/%m/%Y'),
        'avg_rating': round(stats['avg'] or 0, 1),
        'review_count': stats['total'],
    })


def wishlist(request):
    return render(request, 'landing_page/produtos/wishlist.html')


def all_products(request):
    products, filter_context = _filter_products(request, Product.objects.all())
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
        **filter_context,
    }
    return render(request, 'landing_page/produtos/all_products.html', context)


def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products, filter_context = _filter_products(
        request, Product.objects.filter(category=category)
    )
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
        **filter_context,
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

    products, filter_context = _filter_products(request, products)
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
        **filter_context,
    }
    return render(
        request, 'landing_page/produtos/search_results.html', context
    )

def cart_page(request):
    return render(request, 'landing_page/carrinho/cart.html')


def collection_list(request):
    collections = Collection.objects.prefetch_related('products').all()
    return render(request, 'landing_page/colecoes/collection_list.html', {
        'collections': collections,
    })


def collection_detail(request, slug):
    collection = get_object_or_404(Collection, slug=slug)
    products, filter_context = _filter_products(
        request, collection.products.all()
    )
    return render(request, 'landing_page/colecoes/collection_detail.html', {
        'collection': collection,
        'products': products,
        'total_products': products.count(),
        **filter_context,
    })


def consulta_personalizada(request):
    materials = Material.objects.all()
    occasions = Occasion.objects.all()
    return render(request, 'landing_page/consulta/consulta.html', {
        'materials': materials,
        'occasions': occasions,
    })


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