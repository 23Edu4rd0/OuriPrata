// ===== NAVBAR.JS - Menu Mobile =====

let recalculatePadding = null;

function initMobileMenu() {
  const toggleBtn = document.getElementById("menu-toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  
  toggleBtn?.addEventListener("click", () => {
    if (mobileMenu.style.display === "none" || !mobileMenu.style.display) {
      mobileMenu.style.display = "block";
    } else {
      mobileMenu.style.display = "none";
    }
    
    if (recalculatePadding) {
      setTimeout(recalculatePadding, 100);
    }
  });
}

// ===== INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', function() {
  initMobileMenu();
  
  // Elementos desktop
  const searchInput = document.getElementById('search-input');
  const suggestionsContainer = document.getElementById('search-suggestions');
  const suggestionsList = document.getElementById('suggestions-list');
  
  // Elementos mobile
  const searchInputMobile = document.getElementById('search-input-mobile');
  const suggestionsContainerMobile = document.getElementById('search-suggestions-mobile');
  const suggestionsListMobile = document.getElementById('suggestions-list-mobile');
  
  // Configurar eventos para versão desktop
  if (searchInput && suggestionsContainer && suggestionsList) {
    setupSearchSuggestions(searchInput, suggestionsContainer, suggestionsList, 'desktop');
  }
  
  // Configurar eventos para versão mobile
  if (searchInputMobile && suggestionsContainerMobile && suggestionsListMobile) {
    setupSearchSuggestions(searchInputMobile, suggestionsContainerMobile, suggestionsListMobile, 'mobile');
  }
  
  // Testar suporte à busca por voz
  testVoiceSupportAndShowBtn();
  
  // Expor funções globalmente
  window.clearSearchHistory = clearSearchHistory;
  window.searchCategory = searchCategory;
  window.searchTerm = searchTerm;
  window.applyAdvancedSearch = applyAdvancedSearch;
  window.addToSearchHistory = addToSearchHistory;
  window.startVoiceSearch = startVoiceSearch;
}); 