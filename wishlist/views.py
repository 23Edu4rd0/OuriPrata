from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Wishlist
from catalogo.models import Joais

@login_required
def wishlist_view(request):
    """Exibe a lista de desejos do usuário"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('produto')
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
@require_POST
def add_to_wishlist(request, produto_id):
    """Adiciona produto à lista de desejos"""
    produto = get_object_or_404(Joais, id=produto_id)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        produto=produto
    )
    
    if created:
        message = f'{produto.nome} foi adicionado à sua lista de desejos!'
        
        # Para requisições AJAX, retornar JSON sem adicionar à sessão
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'status': 'added', 'message': message})
        else:
            messages.success(request, message)
    else:
        message = f'{produto.nome} já está na sua lista de desejos!'
        
        # Para requisições AJAX, retornar JSON sem adicionar à sessão
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'status': 'exists', 'message': message})
        else:
            messages.info(request, message)
            
    return JsonResponse({'status': 'added', 'message': 'Produto adicionado à lista de desejos!'})

@login_required
@require_POST
def remove_from_wishlist(request, produto_id):
    """Remove produto da lista de desejos"""
    produto = get_object_or_404(Joais, id=produto_id)
    
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, produto=produto)
        wishlist_item.delete()
        message = f'{produto.nome} foi removido da sua lista de desejos!'
        
        # Para requisições AJAX, retornar JSON sem adicionar à sessão
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'status': 'removed', 'message': message})
        else:
            messages.success(request, message)
            
    except Wishlist.DoesNotExist:
        error_message = 'Produto não encontrado na sua lista de desejos!'
        
        # Para requisições AJAX, retornar JSON sem adicionar à sessão
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'status': 'not_found', 'message': error_message})
        else:
            messages.error(request, error_message)
    
    return JsonResponse({'status': 'not_found', 'message': 'Produto não encontrado na lista!'})

@login_required
def check_wishlist_status(request, produto_id):
    """Verifica se o produto está na lista de desejos"""
    exists = Wishlist.objects.filter(user=request.user, produto_id=produto_id).exists()
    return JsonResponse({'in_wishlist': exists})
