// ===== FILTERS.JS - Funcionalidades de Filtros e Listagem =====

// ===== FILTROS DESKTOP =====
function applyFilters() {
  const selectedCategories = Array.from(document.querySelectorAll('input[name="categoria"]:checked'))
    .map(cb => cb.value);
  
  const selectedMaterials = Array.from(document.querySelectorAll('input[name="material"]:checked'))
    .map(cb => cb.value);
  
  const selectedOcasioes = Array.from(document.querySelectorAll('input[name="ocasiao"]:checked'))
    .map(cb => cb.value);
  
  const priceMin = document.getElementById('preco-min')?.value;
  const priceMax = document.getElementById('preco-max')?.value;
  const onlyPromotions = document.getElementById('apenas-promocoes')?.checked;
  const ratingFilter = document.querySelector('input[name="rating"]:checked')?.value;
  
  // Construir URL com parâmetros
  const params = new URLSearchParams();
  
  if (selectedCategories.length > 0) {
    params.append('categoria', selectedCategories.join(','));
  }
  
  if (selectedMaterials.length > 0) {
    params.append('material', selectedMaterials.join(','));
  }
  
  if (selectedOcasioes.length > 0) {
    params.append('ocasiao', selectedOcasioes.join(','));
  }
  
  if (priceMin) params.append('preco_min', priceMin);
  if (priceMax) params.append('preco_max', priceMax);
  if (onlyPromotions) params.append('promocao', 'true');
  if (ratingFilter) params.append('rating', ratingFilter);
  
  // Redirecionar com filtros
  const currentUrl = new URL(window.location);
  currentUrl.search = params.toString();
  window.location.href = currentUrl.toString();
}

function clearFilters() {
  // Limpar checkboxes
  document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
    cb.checked = false;
  });
  
  // Limpar inputs de preço
  const priceInputs = document.querySelectorAll('input[type="number"]');
  priceInputs.forEach(input => {
    input.value = '';
  });
  
  // Limpar filtro de rating
  const ratingInputs = document.querySelectorAll('input[name="rating"]');
  ratingInputs.forEach(input => {
    input.checked = false;
  });
  
  // Aplicar filtros limpos
  applyFilters();
}

// ===== FILTROS MOBILE =====
function openFilterModal() {
  const modal = document.getElementById('filterModal');
  if (modal) {
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    // Esconder botões de filtro
    const filterBtns = document.querySelectorAll('.mobile-filter-btn, .mobile-filter-top-btn');
    filterBtns.forEach(btn => btn.classList.add('hide'));
  }
}

function closeFilterModal() {
  const modal = document.getElementById('filterModal');
  if (modal) {
    const bsModal = bootstrap.Modal.getInstance(modal);
    if (bsModal) {
      bsModal.hide();
    }
    
    // Mostrar botões de filtro
    const filterBtns = document.querySelectorAll('.mobile-filter-btn, .mobile-filter-top-btn');
    filterBtns.forEach(btn => btn.classList.remove('hide'));
  }
}

function toggleMobileSwitch(switchId) {
  const switchElement = document.getElementById(switchId);
  if (switchElement) {
    switchElement.checked = !switchElement.checked;
  }
}

function applyMobileFilters() {
  const selectedCategories = Array.from(document.querySelectorAll('#filterModal input[name="categoria"]:checked'))
    .map(cb => cb.value);
  
  const selectedMaterials = Array.from(document.querySelectorAll('#filterModal input[name="material"]:checked'))
    .map(cb => cb.value);
  
  const selectedOcasioes = Array.from(document.querySelectorAll('#filterModal input[name="ocasiao"]:checked'))
    .map(cb => cb.value);
  
  const priceMin = document.getElementById('mobile-preco-min')?.value;
  const priceMax = document.getElementById('mobile-preco-max')?.value;
  const onlyPromotions = document.getElementById('mobile-apenas-promocoes')?.checked;
  const ratingFilter = document.querySelector('#filterModal input[name="rating"]:checked')?.value;
  
  // Construir URL com parâmetros
  const params = new URLSearchParams();
  
  if (selectedCategories.length > 0) {
    params.append('categoria', selectedCategories.join(','));
  }
  
  if (selectedMaterials.length > 0) {
    params.append('material', selectedMaterials.join(','));
  }
  
  if (selectedOcasioes.length > 0) {
    params.append('ocasiao', selectedOcasioes.join(','));
  }
  
  if (priceMin) params.append('preco_min', priceMin);
  if (priceMax) params.append('preco_max', priceMax);
  if (onlyPromotions) params.append('promocao', 'true');
  if (ratingFilter) params.append('rating', ratingFilter);
  
  // Fechar modal
  closeFilterModal();
  
  // Redirecionar com filtros
  const currentUrl = new URL(window.location);
  currentUrl.search = params.toString();
  window.location.href = currentUrl.toString();
}

function clearMobileFilters() {
  // Limpar checkboxes no modal
  document.querySelectorAll('#filterModal input[type="checkbox"]').forEach(cb => {
    cb.checked = false;
  });
  
  // Limpar inputs de preço no modal
  const priceInputs = document.querySelectorAll('#filterModal input[type="number"]');
  priceInputs.forEach(input => {
    input.value = '';
  });
  
  // Limpar filtro de rating no modal
  const ratingInputs = document.querySelectorAll('#filterModal input[name="rating"]');
  ratingInputs.forEach(input => {
    input.checked = false;
  });
  
  // Aplicar filtros limpos
  applyMobileFilters();
}

// ===== CATEGORIAS ATIVAS =====
function highlightActiveCategory() {
  const currentPath = window.location.pathname;
  const categoryButtons = document.querySelectorAll('.category-btn');
  
  categoryButtons.forEach(btn => {
    btn.classList.remove('active');
    const href = btn.getAttribute('href');
    
    if (href && currentPath.includes(href)) {
      btn.classList.add('active');
    }
  });
}

// ===== ORDENAÇÃO =====
function sortProducts(sortBy) {
  const currentUrl = new URL(window.location);
  currentUrl.searchParams.set('ordenar', sortBy);
  window.location.href = currentUrl.toString();
}

// ===== PAGINAÇÃO =====
function goToPage(page) {
  const currentUrl = new URL(window.location);
  currentUrl.searchParams.set('pagina', page);
  window.location.href = currentUrl.toString();
}

// ===== INFINITE SCROLL =====
let isLoading = false;
let currentPage = 1;

function setupInfiniteScroll() {
  const productGrid = document.querySelector('.product-grid');
  if (!productGrid) return;
  
  window.addEventListener('scroll', () => {
    if (isLoading) return;
    
    const scrollTop = window.pageYOffset;
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    
    if (scrollTop + windowHeight >= documentHeight - 100) {
      loadMoreProducts();
    }
  });
}

function loadMoreProducts() {
  if (isLoading) return;
  
  isLoading = true;
  currentPage++;
  
  const currentUrl = new URL(window.location);
  currentUrl.searchParams.set('pagina', currentPage);
  
  fetch(currentUrl.toString())
    .then(response => response.text())
    .then(html => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const newProducts = doc.querySelectorAll('.product-item');
      
      const productGrid = document.querySelector('.product-grid');
      newProducts.forEach(product => {
        productGrid.appendChild(product.cloneNode(true));
      });
      
      isLoading = false;
    })
    .catch(error => {
      console.error('Erro ao carregar mais produtos:', error);
      isLoading = false;
    });
}

// ===== LAZY LOADING =====
function setupLazyLoading() {
  const images = document.querySelectorAll('img[data-src]');
  
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        observer.unobserve(img);
      }
    });
  });
  
  images.forEach(img => imageObserver.observe(img));
}

// ===== FILTROS DINÂMICOS =====
function updateFilterCounts() {
  const filterGroups = document.querySelectorAll('.filter-group');
  
  filterGroups.forEach(group => {
    const checkboxes = group.querySelectorAll('input[type="checkbox"]');
    const countElement = group.querySelector('.filter-count');
    
    if (countElement) {
      const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
      countElement.textContent = `(${checkedCount})`;
    }
  });
}

// ===== RESPONSIVIDADE DOS FILTROS =====
function setupResponsiveFilters() {
  const filterToggle = document.querySelector('.filter-toggle');
  const filterSidebar = document.querySelector('.filters-sidebar');
  
  if (filterToggle && filterSidebar) {
    filterToggle.addEventListener('click', () => {
      filterSidebar.classList.toggle('show');
    });
  }
  
  // Fechar filtros ao clicar fora
  document.addEventListener('click', (e) => {
    if (!filterSidebar?.contains(e.target) && !filterToggle?.contains(e.target)) {
      filterSidebar?.classList.remove('show');
    }
  });
}

// ===== INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', function() {
  // Destacar categoria ativa
  highlightActiveCategory();
  
  // Configurar filtros responsivos
  setupResponsiveFilters();
  
  // Configurar lazy loading
  setupLazyLoading();
  
  // Configurar infinite scroll se habilitado
  const infiniteScrollEnabled = document.querySelector('[data-infinite-scroll]');
  if (infiniteScrollEnabled) {
    setupInfiniteScroll();
  }
  
  // Atualizar contadores de filtros
  updateFilterCounts();
  
  // Expor funções globalmente
  window.applyFilters = applyFilters;
  window.clearFilters = clearFilters;
  window.openFilterModal = openFilterModal;
  window.closeFilterModal = closeFilterModal;
  window.toggleMobileSwitch = toggleMobileSwitch;
  window.applyMobileFilters = applyMobileFilters;
  window.clearMobileFilters = clearMobileFilters;
  window.sortProducts = sortProducts;
  window.goToPage = goToPage;
}); 