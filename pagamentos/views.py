import json
from django.http import JsonResponse
from django.shortcuts import render
from pagamentos.models import Pedido
from django.conf import settings
import mercadopago

def webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('Webhook do Mercado Pago recebido:', data)
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
            status_map = {
                'approved': 'approved',
                'pending': 'pending',
                'rejected': 'rejected',
            }
            pedido = None
            if mp_id:
                pedido = Pedido.objects.filter(mercado_pago_id=mp_id).first()
            if pedido and new_status:
                pedido.status = status_map.get(new_status, 'pending')
                pedido.save()
                if pedido.status in ['approved', 'pending']:
                    try:
                        from cart.models import CartItem
                        CartItem.objects.filter(user=pedido.usuario).delete()
                    except Exception as err:
                        print(f"Erro ao remover itens do carrinho: {err}")
            return JsonResponse({'status': 'success', 'message': 'Webhook received and order updated'})
        except json.JSONDecodeError:
            print('Erro ao decodificar JSON do webhook')
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f'Erro no webhook: {str(e)}')
            return JsonResponse({'error': 'Internal server error'}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def pagamento_sucesso(request, produto_slug=None):
    context = {}
    if produto_slug:
        from catalogo.models import Joais
        try:
            produto = Joais.objects.get(slug=produto_slug)
            context['produto'] = produto
        except Joais.DoesNotExist:
            pass
    return render(request, 'pagamentos/pagamento_sucesso.html', context)

def pagamento_erro(request, produto_slug=None):
    context = {}
    if produto_slug:
        from catalogo.models import Joais
        try:
            produto = Joais.objects.get(slug=produto_slug)
            context['produto'] = produto
        except Joais.DoesNotExist:
            pass
    return render(request, 'pagamentos/pagamento_erro.html', context)

def pagamento_pendente(request, produto_slug=None):
    context = {}
    if produto_slug:
        from catalogo.models import Joais
        try:
            produto = Joais.objects.get(slug=produto_slug)
            context['produto'] = produto
        except Joais.DoesNotExist:
            pass
    # Passar contexto do pedido se necessário
    if 'product' in request.GET:
        context['product'] = request.GET.get('product')
    if 'frete_info' in request.GET:
        context['frete_info'] = request.GET.get('frete_info')
    return render(request, 'pagamentos/pagamento_pendente.html', context)
from django.shortcuts import render

# Create your views here.
