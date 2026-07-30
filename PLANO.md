# Plano de Evolução Visual & Funcional — OuriPrata

## Pesquisa (resumo)
Referências: Mejuri, Catbird, Vrai — camadas de white space generoso, fotografia macro,
paleta neutra com metal como acento (não fundo), tipografia serifada fina em títulos,
grids de produto consistentes, filtros simples (metal/preço), microzoom no hover,
selos de confiança/social proof discretos, sem popups agressivos.

O projeto já tem boa base: paleta gold/cream, Cormorant Garamond + Inter, componentes
com bom respiro (navbar, hero, product_card). O trabalho aqui é evolutivo, não uma
reescrita — reforçar o que já funciona e fechar lacunas funcionais.

## Direção de design (já em vigor, reforçar)
- Paleta neutra cream/ink com dourado só em acentos (preço, hover, selos)
- Serifada (Cormorant Garamond) em títulos, sans (Inter) no resto — manter
- Espaçamento generoso, sem grids apertados
- Transições suaves (scale sutil no hover, fade), nada exagerado

## Gaps funcionais identificados
1. Sem wishlist — usuário não consegue "guardar" peças
2. Sem quick view — precisa sair do grid para ver detalhes básicos
3. Sem zoom de imagem na página de produto (só troca de thumbnail)
4. Sem selos de urgência/prova social (novo, mais vendido)
5. Filtro de preço/avaliação existe em `filters_menu.html` mas não está incluído em
   nenhuma página (`all_products.html` não usa o partial) — filtro morto
6. `product_card.html` referencia campos inexistentes no model (`em_promocao`,
   `avaliacao`) — sempre falsy, filtro de avaliação/promoção nunca funciona de verdade

## Ordem de execução
1. **Wishlist client-side** (localStorage) — botão de coração no card e na página de
   produto, contador no navbar, página `/favoritos/` listando os salvos
2. **Badge "Novo"** no card (baseado em `created_at`, já existe no model) e badge
   "Destaque" (baseado em `featured`, já existe) — sem inventar campos novos
3. **Quick view modal** — abre por cima do grid com imagem, nome, preço, botão
   WhatsApp e link "ver detalhes", sem sair da listagem
4. **Zoom de imagem** na página de produto (zoom suave no hover sobre a imagem
   principal, seguindo o cursor)
5. **Conectar `filters_menu.html`** em `all_products.html` (sidebar de filtro por
   preço), removendo o filtro de avaliação/promoção quebrado (sem dado real por trás)
6. Testes manuais (`python manage.py check`, subir servidor, checar grid/carousel/wishlist)
7. Commits pequenos por etapa + `RESUMO.md` final

## Fora de escopo (fica para decisão futura)
- Avaliações reais de clientes (precisaria de model novo + moderação)
- Estoque/"últimas peças" (não há campo de quantidade no model hoje)
- Zoom estilo AR/360° (fora do orçamento de tempo desta rodada)
