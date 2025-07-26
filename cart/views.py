from django.views.decorators.csrf import csrf_exempt
from cart.utils import pos_pagamento_usuario

@csrf_exempt
def webhook_cart(request):
    """
    Endpoint para receber notificações do Mercado Pago e processar pós-pagamento.
    """
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            print('Webhook do Mercado Pago recebido (cart):', data)
            mp_id = None
            new_status = None
            if 'data' in data and 'id' in data['data']:
                mp_id = data['data']['id']
            elif 'id' in data:
                mp_id = data['id']
            if 'type' in data and data['type'] == 'payment':
                payment_info = data.get('payment', {})
                new_status = payment_info.get('status')
            if not new_status and 'status' in data:
                new_status = data['status']
            try:
                pedido = pos_pagamento_usuario(mp_id, new_status)
            except Exception as err:
                print(f"Erro no pós-processamento do pedido: {err}")
            return JsonResponse({'status': 'success', 'message': 'Webhook received and order updated'})
        except json.JSONDecodeError:
            print('Erro ao decodificar JSON do webhook')
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f'Erro no webhook: {str(e)}')
            return JsonResponse({'error': 'Internal server error'}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum
from decimal import Decimal
from .models import Cart
from catalogo.models import Joais
import mercadopago
from django.conf import settings

@login_required
def cart_view(request):
    """Exibe o carrinho do usuário"""
    cart_items = Cart.objects.filter(user=request.user).select_related('produto')
    
    # Verificar se o usuário tem perfil completo
    show_checkout = False
    frete_info = None
    
    if cart_items.exists():
        try:
            from accounts.models import UserProfile
            profile = request.user.userprofile
            
            if profile.endereco_completo:
                show_checkout = True
                # Calcular frete para o carrinho
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
                        'valor': 35.00,
                        'tipo': 'Correios',
                        'prazo': '5-10 dias úteis',
                        'gratuito': False,
                        'descricao': 'Frete: R$ 35,00'
                    }
        except:
            # Usuário não tem perfil completo
            frete_info = {
                'valor': 35.00,
                'tipo': 'Correios',
                'prazo': '5-10 dias úteis',
                'gratuito': False,
                'descricao': 'Complete seu perfil para calcular frete'
            }
    
    # Calcular totais
    subtotal = sum(item.total_item for item in cart_items)
    frete_valor = Decimal(str(frete_info['valor'])) if frete_info and not frete_info['gratuito'] else Decimal('0.00')
    total_com_frete = subtotal + frete_valor
    
    # Configurar Mercado Pago apenas se o usuário pode fazer checkout
    preference_id = None
    if cart_items.exists() and show_checkout:
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        
        # Criar itens para o Mercado Pago
        items = []
        for item in cart_items:
            preco = item.produto.preco_promocional if item.produto.em_promocao and item.produto.preco_promocional else item.produto.preco
            items.append({
                "title": item.produto.nome,
                "quantity": item.quantidade,
                "unit_price": float(preco),
                "currency_id": "BRL"
            })
        
        # Adicionar frete como item separado se não for gratuito
        if frete_info and not frete_info['gratuito']:
            items.append({
                "title": f"Frete - {frete_info['tipo']}",
                "quantity": 1,
                "unit_price": float(frete_info['valor']),
                "currency_id": "BRL"
            })
        
        preference_data = {
            "items": items,
            "back_urls": {
                "success": request.build_absolute_uri("/sucesso/"),
                "failure": request.build_absolute_uri("/erro/"),
                "pending": request.build_absolute_uri("/pendente/")
            },
            "payment_methods": {
                "excluded_payment_types": [
                    {"id": "ticket"}
                ]
            }
        }
        
        preference_response = sdk.preference().create(preference_data)
        if preference_response["status"] == 201:
            preference_id = preference_response["response"]["id"]
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'frete_info': frete_info,
        'frete_valor': frete_valor,
        'total': total_com_frete,
        'show_checkout': show_checkout,
        'preference_id': preference_id,
        'mercado_pago_public_key': settings.MERCADO_PAGO_PUBLIC_KEY,
    }
    
    return render(request, 'cart/cart.html', context)

@login_required
@require_POST
def add_to_cart(request, produto_id):
    """Adiciona produto ao carrinho"""
    produto = get_object_or_404(Joais, id=produto_id)
    quantidade = int(request.POST.get('quantidade', 1))
    ring_size = request.POST.get('ring_size', '').strip()
    
    # Verificar se é um produto que precisa de tamanho
    categoria_nome = produto.categoria.nome.lower() if produto.categoria else ""
    precisa_tamanho = any(palavra in categoria_nome for palavra in ['anel', 'anéis', 'alargador', 'alargadores', 'aliança', 'alianças'])
    
    if precisa_tamanho and not ring_size:
        return JsonResponse({
            'status': 'error', 
            'message': 'Por favor, selecione o tamanho do dedo para este produto.'
        })
    
    # Buscar item existente com mesmo produto e tamanho (se aplicável)
    cart_filter = {'user': request.user, 'produto': produto}
    if ring_size:
        cart_filter['ring_size'] = ring_size
    else:
        cart_filter['ring_size__isnull'] = True
    
    try:
        cart_item = Cart.objects.get(**cart_filter)
        cart_item.quantidade += quantidade
        cart_item.save()
        size_info = f" (Tamanho {ring_size})" if ring_size else ""
        message = f'{produto.nome}{size_info} - quantidade atualizada no carrinho!'
        
        # Para requisições AJAX, retornar JSON sem adicionar à sessão
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'status': 'success', 
                'message': message,
                'action': 'updated'
            })
        else:
            messages.success(request, message)
            
    except Cart.DoesNotExist:
        # Criar novo item no carrinho
        cart_item = Cart.objects.create(
            user=request.user,
            produto=produto,
            quantidade=quantidade,
            ring_size=ring_size if ring_size else None
        )
        size_info = f" (Tamanho {ring_size})" if ring_size else ""
        message = f'{produto.nome}{size_info} foi adicionado ao carrinho!'
        
        # Para requisições AJAX, retornar JSON sem adicionar à sessão
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'status': 'success', 
                'message': message,
                'action': 'added'
            })
        else:
            messages.success(request, message)
    
    # Para requisições normais (não AJAX), redirecionar
    return JsonResponse({'status': 'success', 'message': 'Produto adicionado ao carrinho!'})

@login_required
@require_POST
def update_cart(request, produto_id):
    """Atualiza quantidade do produto no carrinho"""
    produto = get_object_or_404(Joais, id=produto_id)
    quantidade = int(request.POST.get('quantidade', 1))
    ring_size = request.POST.get('ring_size', '').strip()
    
    # Buscar item no carrinho considerando o tamanho
    cart_filter = {'user': request.user, 'produto': produto}
    if ring_size:
        cart_filter['ring_size'] = ring_size
    else:
        cart_filter['ring_size__isnull'] = True
    
    try:
        cart_item = Cart.objects.get(**cart_filter)
        if quantidade > 0:
            cart_item.quantidade = quantidade
            cart_item.save()
            return JsonResponse({'status': 'updated', 'message': 'Quantidade atualizada!'})
        else:
            cart_item.delete()
            return JsonResponse({'status': 'removed', 'message': 'Produto removido do carrinho!'})
    except Cart.DoesNotExist:
        return JsonResponse({'status': 'not_found', 'message': 'Produto não encontrado no carrinho!'})

@login_required
@require_POST
def remove_from_cart(request, produto_id):
    """Remove produto do carrinho"""
    produto = get_object_or_404(Joais, id=produto_id)
    ring_size = request.POST.get('ring_size', '').strip()
    
    # Buscar item no carrinho considerando o tamanho
    cart_filter = {'user': request.user, 'produto': produto}
    if ring_size:
        cart_filter['ring_size'] = ring_size
    else:
        cart_filter['ring_size__isnull'] = True
    
    try:
        cart_item = Cart.objects.get(**cart_filter)
        size_info = f" (Tamanho {ring_size})" if ring_size else ""
        cart_item.delete()
        message = f'{produto.nome}{size_info} foi removido do carrinho!'
        
        # Para requisições AJAX, retornar JSON sem adicionar à sessão
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'status': 'removed', 'message': message})
        else:
            messages.success(request, message)
            
    except Cart.DoesNotExist:
        error_message = 'Produto não encontrado no carrinho!'
        
        # Para requisições AJAX, retornar JSON sem adicionar à sessão
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'status': 'not_found', 'message': error_message})
        else:
            messages.error(request, error_message)
    
    return JsonResponse({'status': 'not_found', 'message': 'Produto não encontrado no carrinho!'})

@login_required
def cart_count(request):
    """Retorna a quantidade de itens no carrinho"""
    count = Cart.objects.filter(user=request.user).aggregate(
        total=Sum('quantidade')
    )['total'] or 0
    return JsonResponse({'count': count})

@login_required
def checkout_cart(request):
    """
    View para iniciar o checkout do carrinho - verifica se o usuário tem perfil completo
    """
    # Verificar se há itens no carrinho
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, 'Seu carrinho está vazio.')
        return redirect('cart:cart')
    
    try:
        from accounts.models import UserProfile
        profile = request.user.userprofile
        
        # Verificar se o perfil está completo
        if not profile.endereco_completo:
            # Redirecionar para completar perfil com parâmetro next
            return redirect(f'/accounts/complete-profile/?next=/cart/')
        
        # Perfil completo, processar checkout do carrinho
        return cart_view(request)
        
    except UserProfile.DoesNotExist:
        # Usuário não tem perfil, redirecionar para completar
        return redirect(f'/accounts/complete-profile/?next=/cart/')
