# Decisões de front-end

Registro do que não é óbvio olhando os templates. Cada item aqui existe porque
alguém já quebrou (ou quase quebrou) a coisa "arrumando" o que parecia errado.

## Formulário de contato sem `method="post"`

`catalogo/templates/landing_page/contato/contact_us.html`

A ausência do atributo é proposital. Não há view tratando POST — o envio é
feito pelo WhatsApp via JavaScript, mesmo caminho da consulta personalizada.

Com `method="post"` o formulário recarregava a página e a mensagem se perdia em
silêncio: o cliente saía achando que tinha falado com a loja.

## Ordem dos scripts em `base.html`

`escape.js` precisa vir antes de todos os outros — eles dependem da função
`escapeHtml` que ele define. Reordenar quebra o escape de HTML e reabre o XSS
que a correção original fechou.

## Carrossel de produtos

`catalogo/templates/landing_page/partials/_product_carousel.html`

Mostra 4 peças por vez no desktop e 2 no mobile, com a borda da terceira
aparecendo de propósito: é essa borda espiada que sinaliza que dá para
arrastar. Sem ela o trilho parece uma grade estática.

- **Mobile:** só arraste (scroll nativo com snap). As setas não são renderizadas.
- **Desktop:** arraste (rolagem lateral do trackpad) e setas, as duas coisas.

`overscroll-x-contain` impede que o gesto "vaze" para o navegador e dispare o
voltar-página quando o trilho chega ao fim.

O snap é `mandatory` no mobile, onde o dedo solta em qualquer ponto, e
`proximity` no desktop, para não brigar com a posição exata em que as setas
param.

As setas aparecem só em telas md+ e apenas quando o trilho realmente transborda
— o JavaScript marca `data-overflow` no elemento raiz.

## Barra de características (`_trust_bar`)

O conteúdo é incluído duas vezes dentro do mesmo trilho para o loop da animação
não ter emenda visível. As duas cópias precisam ser idênticas, por isso vivem
num partial só (`_trust_bar_items.html`) incluído duas vezes — antes eram dois
blocos copiados à mão que já tinham divergido no espaçamento do mobile
(`gap-10` contra `gap-16`), o que fazia o carrossel dar um solavanco a cada
volta.

A segunda cópia leva `aria-hidden` para o leitor de tela não repetir a lista.

## Coleção da estação (`_season`)

O cabeçalho muda de forma conforme a coleção tenha ou não capa:

- **Com capa:** duas colunas, texto ao lado da imagem.
- **Sem capa:** centralizado — senão sobrariam 7 colunas vazias no desktop.

## Tailwind é compilado localmente

O CSS que vai para produção é o `theme/static/css/dist/styles.css` versionado no
repositório. O build do Railway só instala Python, e o `package.json` do Tailwind
está em `theme/static_src/`, não na raiz — não há Node no container de build.

Ao mexer em classes nos templates, rode `python manage.py tailwind build` e
commite o `styles.css` junto. Esquecer disso deixa o estilo novo fora do ar sem
erro nenhum para denunciar.
