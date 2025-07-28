# CSS Files - OuriPrata

## Estrutura dos Arquivos CSS

Esta pasta contém todos os arquivos CSS customizados do projeto OuriPrata, organizados por funcionalidade.

## Arquivos

### `custom.css` (8.4KB, 517 linhas)
**Estilos Customizados do Projeto**

#### **Animações**
- **Pulse**: Animação para botões de busca por voz
- **Loading**: Spinner de carregamento
- **Transições**: Efeitos suaves em hover e interações

#### **Sistema de Busca**
- **Sugestões**: Estilos para dropdown de sugestões
- **Histórico**: Botões de histórico de buscas
- **Categorias Populares**: Estilos para categorias em destaque
- **Busca Avançada**: Formulários de filtros avançados
- **Botões de Voz**: Estilos para busca por voz

#### **Filtros Mobile**
- **Modal de Filtros**: Design responsivo para dispositivos móveis
- **Botão FAB**: Floating Action Button para abrir filtros
- **Categorias Grid**: Layout em grid para categorias
- **Switches**: Toggles customizados para opções
- **Inputs de Preço**: Campos de preço responsivos
- **Botões de Ação**: Aplicar e limpar filtros

#### **Sistema de Avaliações**
- **Seção de Reviews**: Layout para seção de avaliações
- **Barras de Rating**: Visualização de distribuição de estrelas
- **Cards de Review**: Estilos para cards de avaliações
- **Estrelas Interativas**: Sistema de rating com estrelas
- **Formulário de Avaliação**: Estilos para formulário

#### **Cards de Produtos**
- **Hover Effects**: Animações em hover
- **Badges**: Promoções e ratings
- **Imagens**: Responsividade e object-fit
- **Preços**: Destaque para preços e promoções
- **Botões**: Estilos para ações de produtos

#### **Filtros Desktop**
- **Sidebar**: Layout da barra lateral de filtros
- **Checkboxes**: Estilos customizados para checkboxes
- **Ranges de Preço**: Campos de preço mínimo/máximo
- **Botões de Filtro**: Aplicar e limpar filtros
- **Categorias Ativas**: Destaque para categoria selecionada

#### **Responsividade**
- **Mobile First**: Design adaptado para dispositivos móveis
- **Breakpoints**: Media queries para diferentes tamanhos
- **Flexibilidade**: Layouts flexíveis e adaptáveis

## Organização

### Estrutura de Pastas
```
static/
├── assets/
│   ├── css/
│   │   ├── custom.css
│   │   └── README.md
│   ├── js/
│   │   ├── navbar.js
│   │   ├── products.js
│   │   ├── filters.js
│   │   └── README.md
│   ├── landing_page/
│   └── joias/
├── bootstrap/
└── bootstrap.min.css
```

### Dependências
- **Bootstrap 5**: Framework CSS base
- **Bootstrap Icons**: Ícones do sistema
- **Google Fonts**: Montserrat (font-family)

### Boas Práticas Implementadas

✅ **Mobile First**: Design responsivo com mobile first
✅ **BEM Methodology**: Nomenclatura consistente
✅ **CSS Variables**: Uso de variáveis CSS quando possível
✅ **Performance**: Otimização de seletores
✅ **Acessibilidade**: Contraste adequado e navegação por teclado
✅ **Manutenibilidade**: Código bem organizado e comentado
✅ **Compatibilidade**: Suporte a navegadores modernos

### Especificidade CSS
- **Bootstrap Override**: Sobrescritas específicas do Bootstrap
- **Custom Classes**: Classes customizadas para funcionalidades específicas
- **Media Queries**: Responsividade bem definida

### Cores do Sistema
```css
/* Cores principais */
--primary: #ffc107;      /* Amarelo/Bronze */
--success: #198754;       /* Verde */
--danger: #dc3545;        /* Vermelho */
--warning: #fd7e14;       /* Laranja */
--info: #0dcaf0;          /* Azul claro */
--dark: #232323;          /* Preto suave */
```

### Breakpoints
```css
/* Mobile */
@media (max-width: 576px) { }

/* Tablet */
@media (min-width: 577px) and (max-width: 768px) { }

/* Desktop */
@media (min-width: 769px) { }
```

## Manutenção

### Adicionando Novos Estilos
1. Crie um novo arquivo CSS na pasta `assets/css/`
2. Adicione a referência no `base.html`
3. Documente os estilos neste README
4. Mantenha a organização por seções

### Debugging
- Use DevTools do navegador para inspecionar estilos
- Verifique especificidade CSS
- Teste em diferentes dispositivos e navegadores
- Valide CSS com ferramentas online

### Performance
- Os arquivos CSS são cacheados pelo navegador
- Considere minificação para produção
- Monitore o tamanho dos arquivos
- Use CSS crítico para above-the-fold

### Compatibilidade
- **Navegadores Modernos**: Chrome, Firefox, Safari, Edge
- **Mobile**: iOS Safari, Chrome Mobile
- **Fallbacks**: Implementados para propriedades não suportadas

## Estrutura de Comentários

```css
/* ===== SEÇÃO ===== */
/* Descrição da seção */

/* Subsessão */
.elemento {
  /* Propriedade com comentário */
  propriedade: valor;
}
```

## Otimizações Futuras

- **CSS Modules**: Para melhor organização
- **PostCSS**: Para processamento avançado
- **CSS-in-JS**: Para componentes dinâmicos
- **Critical CSS**: Para performance
- **CSS Grid**: Para layouts mais complexos 