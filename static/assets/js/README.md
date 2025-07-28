# JavaScript Files - OuriPrata

## Estrutura dos Arquivos JavaScript

Esta pasta contém todos os arquivos JavaScript customizados do projeto OuriPrata, organizados por funcionalidade.

## Arquivos

### `navbar.js` (11KB, 371 linhas)
**Funcionalidades do Navbar e Sistema de Busca**

- **Menu Mobile**: Toggle do menu mobile, geração dinâmica do menu
- **Sistema de Busca Inteligente**: 
  - Sugestões em tempo real
  - Histórico de pesquisas (localStorage)
  - Categorias populares
  - Busca avançada por categoria e preço
- **Busca por Voz**: 
  - Integração com Web Speech API
  - Detecção automática de suporte
  - Tratamento de erros
- **Eventos**: Focus, blur, input, keypress para busca

### `products.js` (15KB, 504 linhas)
**Funcionalidades de Produtos e Interações**

- **Sistema de Alertas**: 
  - Alertas dinâmicos com animações
  - Diferentes tipos (success, danger, warning, info)
  - Auto-remoção após 5 segundos
- **Controle de Quantidade**: Incremento/decremento de produtos
- **Carrinho**: 
  - Adicionar/remover produtos via AJAX
  - Atualização do contador do carrinho
- **Wishlist**: Toggle de favoritos
- **Troca de Imagens**: Galeria de imagens do produto
- **Compartilhamento**: Web Share API com fallback
- **Sistema de Avaliações**:
  - Carregamento dinâmico de reviews
  - Filtros por rating
  - Estatísticas agregadas
  - Formulário de avaliação
  - Estrelas interativas

### `filters.js` (9.8KB, 328 linhas)
**Funcionalidades de Filtros e Listagem**

- **Filtros Desktop**: Aplicação de filtros por categoria, material, ocasião, preço
- **Filtros Mobile**: Modal de filtros para dispositivos móveis
- **Categorias Ativas**: Destaque da categoria selecionada
- **Ordenação**: Ordenação de produtos
- **Paginação**: Navegação entre páginas
- **Infinite Scroll**: Carregamento automático de mais produtos
- **Lazy Loading**: Carregamento sob demanda de imagens
- **Filtros Dinâmicos**: Contadores de filtros aplicados
- **Responsividade**: Adaptação dos filtros para diferentes dispositivos

## Organização

### Estrutura de Pastas
```
static/
├── assets/
│   ├── js/
│   │   ├── navbar.js
│   │   ├── products.js
│   │   ├── filters.js
│   │   └── README.md
│   ├── landing_page/
│   └── joias/
├── bootstrap/
└── custom.css
```

### Dependências
- **Bootstrap 5**: Para componentes UI
- **Web Speech API**: Para busca por voz
- **localStorage**: Para histórico de buscas
- **Fetch API**: Para requisições AJAX

### Boas Práticas Implementadas

✅ **Separação de Responsabilidades**: Cada arquivo tem uma função específica
✅ **Modularização**: Funções reutilizáveis e bem organizadas
✅ **Tratamento de Erros**: Try/catch e validações
✅ **Performance**: Debounce, lazy loading, infinite scroll
✅ **Acessibilidade**: Navegação por teclado e leitores de tela
✅ **Responsividade**: Adaptação para mobile e desktop
✅ **Manutenibilidade**: Código limpo e bem comentado

### Inicialização
Todos os arquivos são carregados no `base.html` e inicializados automaticamente quando o DOM está pronto.

### Compatibilidade
- **Navegadores Modernos**: Chrome, Firefox, Safari, Edge
- **Mobile**: iOS Safari, Chrome Mobile
- **Fallbacks**: Implementados para APIs não suportadas

## Manutenção

### Adicionando Novas Funcionalidades
1. Crie um novo arquivo JS na pasta `assets/js/`
2. Adicione a referência no `base.html`
3. Documente a funcionalidade neste README

### Debugging
- Use `console.log()` para debugging
- Verifique o console do navegador para erros
- Teste em diferentes dispositivos e navegadores

### Performance
- Os arquivos são cacheados pelo navegador
- Considere minificação para produção
- Monitore o tamanho dos arquivos 