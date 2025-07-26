from .models import Cart


def limpar_carrinho_usuario(usuario):
    """
    Remove todos os itens do carrinho do usuário.
    """
    Cart.objects.filter(user=usuario).delete()

def pos_pagamento_usuario(mp_id, new_status):
    """
    Executa toda lógica pós-pagamento para o usuário (atualiza pedido, limpa carrinho, etc).
    mp_id: id do pagamento Mercado Pago
    new_status: status recebido do Mercado Pago
    """
    from pagamentos.models import Pedido
    status_map = {
        'approved': 'approved',
        'pending': 'pending',
        'rejected': 'rejected',
    }
    pedido = Pedido.objects.filter(mercado_pago_id=mp_id).first()
    if pedido and new_status:
        pedido.status = status_map.get(new_status, 'pending')
        pedido.save()
        if pedido.status in ['approved', 'pending']:
            limpar_carrinho_usuario(pedido.usuario)
        return pedido
    return None
