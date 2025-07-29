// ===== PROMOTION-FILTER.JS - Gerenciamento do filtro de promoções =====
console.log('Promotion filter script loaded');

document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM loaded, checking for promotion parameter...');
  
  // Verificar se tem parâmetro promocoes na URL
  const urlParams = new URLSearchParams(window.location.search);
  const promocoes = urlParams.get('promocoes');
  
  console.log('URL params:', window.location.search);
  console.log('Promocoes param:', promocoes);
  
  // Função para aplicar filtro local de promoção
  function applyPromotionFilter() {
    const checkbox = document.getElementById('promocao');
    const products = document.querySelectorAll('.product-item');
    
    if (!checkbox || !products.length) {
      console.log('Checkbox or products not found');
      return;
    }
    
    console.log('Applying promotion filter...');
    console.log('Checkbox checked:', checkbox.checked);
    console.log('Products found:', products.length);
    
    products.forEach(product => {
      const isPromotion = product.dataset.promotion === 'true';
      console.log('Product:', product.dataset.price, 'Promotion:', isPromotion);
      
      if (checkbox.checked && !isPromotion) {
        product.style.display = 'none';
      } else {
        product.style.display = 'block';
      }
    });
    
    console.log('Promotion filter applied');
  }
  
  // Função para configurar o checkbox
  function setupCheckbox() {
    const checkbox = document.getElementById('promocao');
    if (checkbox) {
      // Remover event listeners existentes para evitar conflitos
      checkbox.removeEventListener('change', handleCheckboxChange);
      
      // Adicionar event listener para manter o estado
      checkbox.addEventListener('change', handleCheckboxChange);
      
      console.log('Checkbox configured successfully');
      return true;
    } else {
      console.log('Checkbox not found, retrying...');
      return false;
    }
  }
  
  // Função para lidar com mudanças no checkbox
  function handleCheckboxChange() {
    const currentUrl = new URL(window.location);
    if (this.checked) {
      currentUrl.searchParams.set('promocoes', 'true');
    } else {
      currentUrl.searchParams.delete('promocoes');
    }
    window.history.pushState({}, '', currentUrl);
    
    // Aplicar filtro local usando a função do filters_menu.html
    if (typeof applyLocalFilters === 'function') {
      applyLocalFilters();
    } else {
      applyPromotionFilter();
    }
  }
  
  if (promocoes && ['true', '1', 'sim', 'yes'].includes(promocoes.toLowerCase())) {
    console.log('Detected promocoes parameter, activating filter...');
    
    // Função para tentar ativar o checkbox
    function tryActivateCheckbox() {
      const checkbox = document.getElementById('promocao');
      if (checkbox) {
        checkbox.checked = true;
        setupCheckbox();
        
        // Aplicar filtro local usando a função do filters_menu.html
        if (typeof applyLocalFilters === 'function') {
          applyLocalFilters();
        } else {
          applyPromotionFilter();
        }
        
        console.log('Promotion filter activated successfully');
        return true;
      } else {
        console.log('Checkbox not found, retrying...');
        return false;
      }
    }
    
    // Tentar imediatamente
    if (!tryActivateCheckbox()) {
      // Se não encontrou, tentar novamente após um delay
      setTimeout(function() {
        if (!tryActivateCheckbox()) {
          // Tentar mais uma vez após outro delay
          setTimeout(tryActivateCheckbox, 500);
        }
      }, 200);
    }
  } else {
    console.log('No promotion parameter detected, setting up checkbox only');
    
    // Apenas configurar o checkbox para mudanças manuais
    if (!setupCheckbox()) {
      setTimeout(setupCheckbox, 200);
    }
  }
}); 