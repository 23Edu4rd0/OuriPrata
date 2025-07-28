// ===== MOBILE-FILTERS.JS - Filtros Mobile =====

function openFilterModal() {
  console.log('Abrindo modal...');
  const modal = document.getElementById('filterModal');
  console.log('Modal encontrado:', modal);
  if (modal) {
    // Forçar visibilidade imediata para debug
    modal.style.opacity = '1';
    modal.style.visibility = 'visible';
    modal.style.pointerEvents = 'auto';
    // Adicionar classe show para animação
    modal.classList.add('show');
    console.log('Classe show adicionada');
    document.body.style.overflow = 'hidden';
    // Esconde botão de filtro
    const filterBtn = document.querySelector('.mobile-filter-btn');
    if (filterBtn) filterBtn.classList.add('hide');
  } else {
    console.error('Modal não encontrado!');
  }
}

function closeFilterModal() {
  const modal = document.getElementById('filterModal');
  if (modal) {
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
    // Mostra botão de filtro
    const filterBtn = document.querySelector('.mobile-filter-btn');
    if (filterBtn) filterBtn.classList.remove('hide');
  }
}

function toggleMobileSwitch(element) {
  element.classList.toggle('active');
}

function applyMobileFilters() {
  const isPromoActive = document.getElementById('mobilePromoSwitch').classList.contains('active');
  const minPrice = parseFloat(document.getElementById('mobilePrecoMin').value) || 0;
  const maxPrice = parseFloat(document.getElementById('mobilePrecoMax').value) || Infinity;
  
  // Aqui você pode implementar a lógica de filtro
  console.log('Filtros aplicados:', { isPromoActive, minPrice, maxPrice });
  
  // Fechar modal após aplicar
  closeFilterModal();
}

function clearMobileFilters() {
  document.getElementById('mobilePromoSwitch').classList.remove('active');
  document.getElementById('mobilePrecoMin').value = '';
  document.getElementById('mobilePrecoMax').value = '';
}

// ===== INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', function() {
  // Fechar modal ao clicar fora
  const filterModal = document.getElementById('filterModal');
  if (filterModal) {
    filterModal.addEventListener('click', function(e) {
      if (e.target === this) {
        closeFilterModal();
      }
    });
  }
}); 