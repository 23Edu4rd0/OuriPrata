from django.conf import settings
import mercadopago
from .models import Pedido


def criar_preferencia_mercado_pago(product, user_profile, request):
    """
    Cria uma preferência do Mercado Pago para um produto
    """
    try:
        # Verificar se as credenciais estão configuradas
        access_token = getattr(settings, 'MERCADO_PAGO_ACCESS_TOKEN', '')
        public_key = getattr(settings, 'MERCADO_PAGO_PUBLIC_KEY', '')
        
        if not access_token or not public_key:
            print("Credenciais do Mercado Pago não encontradas")
            return None
        
        # Inicializar SDK do Mercado Pago
        sdk = mercadopago.SDK(access_token)
        
        # Calcular valores
        if product.em_promocao and product.preco_promocional:
            valor_produto = float(product.preco_promocional)
        else:
            valor_produto = float(product.preco)
        
        valor_frete = 0 if user_profile.frete_gratuito else 15.00
        valor_total = valor_produto + valor_frete
        
        # Criar preferência do Mercado Pago
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
                "phone": {
                    "area_code": "37",
                    "number": "999999999"
                },
                "address": {
                    "street_name": user_profile.endereco or "",
                    "street_number": int(user_profile.numero) if user_profile.numero and user_profile.numero.isdigit() else 0,
                    "zip_code": user_profile.cep.replace('-', '') if user_profile.cep else ""
                }
            },
            "back_urls": {
                "success": request.build_absolute_uri(f"/pagamentos/sucesso/{product.slug}/"),
                "failure": request.build_absolute_uri(f"/pagamentos/falha/{product.slug}/"),
                "pending": request.build_absolute_uri(f"/pagamentos/pendente/{product.slug}/")
            },
            "auto_return": "approved",
            "payment_methods": {
                "excluded_payment_types": [
                    {
                        "id": "ticket"
                    }
                ],
                "installments": 12
            },
            "notification_url": request.build_absolute_uri("/pagamentos/webhook/"),
            "metadata": {
                "produto_id": product.id,
                "usuario_id": request.user.id,
                "frete_gratis": user_profile.frete_gratuito
            }
        }
        
        preference_response = sdk.preference().create(preference_data)
        
        if preference_response["status"] == 201:
            preference_id = preference_response["response"]["id"]
            
            # Criar pedido no banco de dados
            pedido = Pedido.objects.create(
                usuario=request.user,
                produto=product,
                quantidade=1,
                valor_produto=valor_produto,
                valor_frete=valor_frete,
                tipo_frete='Grátis' if user_profile.frete_gratuito else 'Pago',
                prazo_frete='3 dias úteis' if user_profile.frete_gratuito else '5-7 dias úteis',
                mercado_pago_id=preference_id,
                status='pending'
            )
            
            return {
                'preference_id': preference_id,
                'public_key': public_key,
                'pedido_id': pedido.id
            }
        else:
            print(f"Erro ao criar preferência: {preference_response}")
            return None
            
    except Exception as e:
        print(f"Erro ao configurar Mercado Pago: {e}")
        return None
