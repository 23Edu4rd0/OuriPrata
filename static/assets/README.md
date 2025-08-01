# Assets - OuriPrata

## Estrutura de Assets do Projeto

Esta pasta contém todos os assets estáticos do projeto OuriPrata, organizados por tipo e funcionalidade.

## Estrutura de Pastas

```
static/assets/
├── css/                    # Arquivos CSS customizados
│   ├── custom.css         # Estilos principais (8.4KB)
│   └── README.md          # Documentação CSS
├── js/                    # Arquivos JavaScript
│   ├── navbar.js          # Funcionalidades do navbar (11KB)
│   ├── products.js        # Funcionalidades de produtos (15KB)
│   ├── filters.js         # Funcionalidades de filtros (9.8KB)
│   └── README.md          # Documentação JavaScript
├── landing_page/          # Assets da landing page
│   ├── logo.png
│   ├── cat.webp
│   └── ...
├── joias/                 # Imagens de produtos
│   ├── aliança.jpg
│   ├── anel_rubi.jpg
│   └── ...
└── README.md              # Este arquivo
```

## Organização por Tipo

### **CSS (`css/`)**
- **custom.css**: Estilos customizados do projeto
- **Funcionalidades**: Animações, responsividade, componentes customizados
- **Tamanho**: 8.4KB, 517 linhas
- **Documentação**: Ver `css/README.md`

### **JavaScript (`js/`)**
- **navbar.js**: Sistema de navegação e busca (11KB)
- **products.js**: Interações com produtos (15KB)
- **filters.js**: Sistema de filtros (9.8KB)
- **Total**: ~36KB de JavaScript customizado
- **Documentação**: Ver `js/README.md`

### **Imagens (`landing_page/` e `joias/`)**
- **Landing Page**: Logo, imagens promocionais, ícones
- **Produtos**: Imagens das joias do catálogo
- **Formatos**: JPG, PNG, WebP
- **Otimização**: Imagens otimizadas para web

## Características Técnicas

### **Performance**
- **Minificação**: Arquivos otimizados para produção
- **Cache**: Headers de cache configurados
- **Compressão**: Gzip habilitado
- **Lazy Loading**: Imagens carregadas sob demanda

### **Organização**
- **Separação por Tipo**: CSS, JS, imagens em pastas específicas
- **Nomenclatura Clara**: Nomes descritivos e consistentes
- **Documentação**: READMEs detalhados para cada pasta
- **Versionamento**: Controle de versão com Git

### **Manutenibilidade**
- **Modularização**: Código organizado por funcionalidade
- **Reutilização**: Componentes reutilizáveis
- **Padrões**: Seguindo boas práticas da indústria
- **Documentação**: Código bem comentado

## Dependências Externas

### **CSS**
- **Bootstrap 5**: Framework CSS base
- **Bootstrap Icons**: Sistema de ícones
- **Google Fonts**: Montserrat (font-family)

### **JavaScript**
- **Bootstrap 5**: Componentes JavaScript
- **Web Speech API**: Busca por voz
- **Fetch API**: Requisições AJAX
- **localStorage**: Armazenamento local

## Fluxo de Desenvolvimento

### **Adicionando Novos Assets**

1. **CSS**:
   - Crie arquivo em `css/`
   - Adicione referência no `base.html`
   - Documente em `css/README.md`

2. **JavaScript**:
   - Crie arquivo em `js/`
   - Adicione referência no `base.html`
   - Documente em `js/README.md`

3. **Imagens**:
   - Otimize a imagem
   - Coloque na pasta apropriada
   - Use formatos modernos (WebP quando possível)

### **Boas Práticas**

✅ **Nomenclatura**: Use nomes descritivos e consistentes
✅ **Otimização**: Comprima imagens e minifique código
✅ **Documentação**: Mantenha READMEs atualizados
✅ **Versionamento**: Commit frequente com mensagens claras
✅ **Testes**: Teste em diferentes dispositivos e navegadores

## Estrutura de Referências

### **Template Base (`base.html`)**
```html
<!-- CSS Customizado -->
<link rel="stylesheet" href="{% static 'assets/css/custom.css' %}">

<!-- JavaScript Customizado -->
<script src="{% static 'assets/js/navbar.js' %}"></script>
<script src="{% static 'assets/js/products.js' %}"></script>
<script src="{% static 'assets/js/filters.js' %}"></script>
```

### **Templates Específicos**
- **Produtos**: Referenciam `products.js`
- **Filtros**: Referenciam `filters.js`
- **Navbar**: Referenciam `navbar.js`

## Monitoramento e Manutenção

### **Tamanho dos Arquivos**
- **CSS Total**: ~8.4KB
- **JS Total**: ~36KB
- **Imagens**: Otimizadas individualmente

### **Performance**
- **First Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **Lighthouse Score**: > 90

### **Compatibilidade**
- **Navegadores**: Chrome, Firefox, Safari, Edge
- **Mobile**: iOS Safari, Chrome Mobile
- **Versões**: Últimas 2 versões principais

## Otimizações Futuras

### **Performance**
- **Critical CSS**: CSS crítico inline
- **Code Splitting**: Carregamento sob demanda
- **Service Worker**: Cache avançado
- **Image Optimization**: WebP e AVIF

### **Desenvolvimento**
- **Build Process**: Webpack/Vite para bundling
- **Hot Reload**: Desenvolvimento mais rápido
- **TypeScript**: Tipagem para JavaScript
- **CSS Modules**: Melhor organização

### **Monitoramento**
- **Analytics**: Rastreamento de performance
- **Error Tracking**: Captura de erros
- **User Feedback**: Métricas de UX

---

**Última Atualização**: Janeiro 2025
**Versão**: 1.0.0
**Mantenedor**: Equipe OuriPrata 

# Organização dos Arquivos CSS e JavaScript

## Estrutura de Arquivos

### CSS
- `navbar.css` - Estilos específicos para a navbar (sticky, mobile)
- `dropdown.css` - Estilos para dropdowns (menu do usuário)
- `review-modal.css` - Estilos para modais de avaliações
- `reviews.css` - Estilos para o sistema de avaliações (responsividade)
- `image-viewer.css` - Estilos para o visualizador de imagens
- `landing.css` - Estilos para a página inicial
- `catalog.css` - Estilos para o catálogo de produtos
- `search-filters.css` - Estilos para filtros de busca
- `utilities.css` - Utilitários CSS gerais
- `components.css` - Componentes CSS diversos

### JavaScript
- `review-system.js` - Lógica completa do sistema de avaliações
- `image-modal.js` - Lógica para o modal de ampliação de imagens

## Funcionalidades

### Navbar
- **Sticky**: Sempre visível no topo
- **Responsivo**: Layout otimizado para mobile
- **Z-index**: Sempre acima de outros elementos

### Dropdown
- **Menu do usuário**: Sempre visível e acessível
- **Mobile**: Adaptação para telas pequenas
- **Posicionamento**: Correto em todos os dispositivos

### Review Modal
- **Review Modal**: Formulário para avaliações
- **Image Preview**: Preview de imagens
- **Botões**: Sempre visíveis e acessíveis

### Sistema de Reviews
- **Responsividade**: Adaptação para mobile e tablet
- **Modal de Review**: Formulário para adicionar/editar avaliações
- **Upload de Imagens**: Preview e upload de imagens
- **Estrelas Interativas**: Sistema de rating com estrelas
- **CRUD Completo**: Criar, ler, atualizar e deletar reviews

### Image Viewer
- **Ampliação**: Clique para ampliar imagens
- **Zoom**: Funcionalidade de zoom 1.5x
- **Responsivo**: Funciona em todos os dispositivos
- **Bordas**: Imagens com bordas para destacar

### Landing Page
- **Página inicial**: Estilos específicos da home
- **Carrossel**: Componentes visuais principais
- **Seções**: Layout responsivo

### Catalog
- **Catálogo**: Estilos para listagem de produtos
- **Cards**: Layout dos cards de produtos
- **Grid**: Sistema de grid responsivo

### Search Filters
- **Filtros**: Interface de filtros de busca
- **Responsivo**: Adaptação para mobile
- **Interativo**: Filtros dinâmicos

## Como Usar

### No Template Base
```html
<!-- CSS essenciais (incluídos automaticamente) -->
<link rel="stylesheet" href="{% static 'assets/css/navbar.css' %}">
<link rel="stylesheet" href="{% static 'assets/css/dropdown.css' %}">
<link rel="stylesheet" href="{% static 'assets/css/review-modal.css' %}">
<link rel="stylesheet" href="{% static 'assets/css/search-filters.css' %}">
<link rel="stylesheet" href="{% static 'assets/css/catalog.css' %}">
<link rel="stylesheet" href="{% static 'assets/css/landing.css' %}">

<!-- CSS específicos (usar block extra_css) -->
{% block extra_css %}
<link rel="stylesheet" href="{% static 'assets/css/reviews.css' %}">
<link rel="stylesheet" href="{% static 'assets/css/image-viewer.css' %}">
{% endblock %}
```

### Chamadas de Função
```javascript
// Abrir modal de review
showReviewForm();

// Ampliar imagem
showImageFullscreen(imageUrl, username);
```

## Benefícios da Organização

1. **Separação de Responsabilidades**: Cada arquivo tem uma função específica
2. **Manutenibilidade**: Fácil de encontrar e modificar código
3. **Performance**: Carregamento otimizado por funcionalidade
4. **Reutilização**: Arquivos podem ser usados em outras páginas
5. **Debugging**: Mais fácil identificar problemas específicos
6. **Escalabilidade**: Fácil adicionar novas funcionalidades
7. **Nomenclatura Clara**: Nomes descritivos e organizados

## Estrutura Final

```
static/assets/css/
├── navbar.css           # Navbar sticky e mobile
├── dropdown.css         # Dropdown menus
├── review-modal.css     # Modais de avaliações
├── reviews.css          # Sistema de reviews
├── image-viewer.css     # Visualizador de imagens
├── landing.css          # Página inicial
├── catalog.css          # Catálogo de produtos
├── search-filters.css   # Filtros de busca
├── utilities.css        # Utilitários gerais
└── components.css       # Componentes diversos
``` 