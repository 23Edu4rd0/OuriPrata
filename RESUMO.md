# Resumo — Evolução Visual & Funcional OuriPrata

Trabalho executado de forma autônoma conforme `PLANO.md`. Ver histórico de commits
no branch `main` para revisão detalhada, do mais antigo ao mais recente:

1. `feat: add created_at-based "new" badge support to Product model`
2. `feat: add wishlist, quick view, image zoom and working price filter`
3. `fix: use shared product_card partial for new arrivals section`
4. `docs: add PLANO.md ...`

## O que foi feito

### 1. Wishlist (favoritos)
- Botão de coração no card de produto e na página de produto
- Persistência em `localStorage` (`static/assets/js/wishlist.js`), sem precisar de
  login/backend
- Contador no navbar (desktop e drawer mobile)
- Nova página `/favoritos/` que renderiza a lista salva

### 2. Quick View
- Botão "Ver rápido" aparece no hover do card, abre modal (`base.html`) com imagem,
  categoria, nome, preço e link para a página completa — sem sair da grid
  (`static/assets/js/quickview.js`)

### 3. Zoom de imagem na página de produto
- Zoom suave (1.6x) que segue o cursor sobre a imagem principal
  (`product_detail.html`), mantendo a troca de thumbnails já existente

### 4. Selos de novidade/destaque
- Propriedade `Product.is_new` (últimos 14 dias, baseada em `created_at`, já
  existente no model) usada para o selo "Novo"
- Selo "Destaque" reaproveitando o campo `featured` já existente
- Aplicado no card de produto e na página de produto

### 5. Filtro de preço funcional
- O partial `filters_menu.html` existia mas não era usado em nenhuma página —
  agora está incluído como sidebar em `all_products.html` (coleção completa e
  por categoria)
- Removido o filtro de avaliação/promoção: referenciava campos (`avaliacao`,
  `em_promocao`) que não existem no model `Product` e nunca funcionaram de fato
  (sempre retornavam falsy). Preferi remover a filtrar por algo inexistente.

### 6. Correção herdada (já em andamento antes desta sessão)
- A seção de lançamentos da home (`_new_products.html`) foi ajustada para usar
  `new_arrivals` (contexto já enviado por `views.home`) e o mesmo
  `product_card.html` do resto do site — isso também resolve o item do
  `TODO.md` ("Resolver bug que lançamentos não aparece") e faz os lançamentos
  ganharem wishlist/quick view/selos de graça.

## Testes realizados
- `python manage.py check` — sem problemas
- Servidor de desenvolvimento local, smoke test via `curl` em: home, coleção,
  favoritos, detalhe de produto, categoria, busca — todos 200, sem erros/tracebacks
  no log do servidor

## Pendente / decisão do dono do projeto
- **Avaliações reais de clientes**: precisaria de um model novo (`Review`) e
  fluxo de moderação — não implementado nesta rodada
- **Estoque / "últimas peças disponíveis"**: não há campo de quantidade no
  model `Product` hoje; se quiser esse selo de urgência, precisa decidir se
  quer controle de estoque real ou só um campo booleano/manual "peça limitada"
- **AR/360°**: fora do escopo desta rodada (exigiria fornecedor de fotos/3D)
- O `TODO.md` do projeto ainda lista "Melhorar lógica de destaque" e
  "Implementar campo de desconto" — não mexi nesses dois pontos porque exigem
  decisão de produto (regra de destaque automática? desconto percentual ou
  valor fixo? mostrado onde?). Ficam para o próximo ciclo.
