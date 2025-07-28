// ===== NAVBAR FIX - JavaScript para garantir visibilidade =====

document.addEventListener('DOMContentLoaded', function() {
  // Garantir que o conteúdo seja visível
  function ensureContentVisibility() {
    // Garantir que o main seja visível
    const main = document.querySelector('main');
    if (main) {
      main.style.display = 'block';
      main.style.visibility = 'visible';
      main.style.opacity = '1';
      main.style.zIndex = '1';
    }
    
    // Garantir que o header da lista seja visível
    const productListHeader = document.querySelector('.product-list-header');
    if (productListHeader) {
      productListHeader.style.display = 'block';
      productListHeader.style.visibility = 'visible';
      productListHeader.style.opacity = '1';
      productListHeader.style.zIndex = '1';
    }
    
    // Garantir que o carrossel seja visível
    const carousel = document.querySelector('.carousel');
    if (carousel) {
      carousel.style.display = 'block';
      carousel.style.visibility = 'visible';
      carousel.style.opacity = '1';
      carousel.style.zIndex = '1';
    }
    
    // Garantir que todos os containers sejam visíveis
    const containers = document.querySelectorAll('.container, .container-fluid');
    containers.forEach(container => {
      container.style.display = 'block';
      container.style.visibility = 'visible';
      container.style.opacity = '1';
      container.style.zIndex = '1';
    });
    
    // Garantir que todas as seções sejam visíveis
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
      section.style.display = 'block';
      section.style.visibility = 'visible';
      section.style.opacity = '1';
      section.style.zIndex = '1';
    });
  }
  
  // Executar imediatamente
  ensureContentVisibility();
  
  // Executar após um pequeno delay para garantir que tudo carregou
  setTimeout(ensureContentVisibility, 100);
  
  // Executar quando a janela mudar de tamanho
  window.addEventListener('resize', ensureContentVisibility);
  
  // Executar quando o DOM mudar
  const observer = new MutationObserver(ensureContentVisibility);
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
}); 