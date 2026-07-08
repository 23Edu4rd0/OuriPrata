// ===== SEARCH.JS - Funcionalidade de Busca Rápida com novo Design System =====

document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('navSearch');
  const suggestionsContainer = document.getElementById('searchSuggestions');
  let searchTimeout;

  if (searchInput && suggestionsContainer) {
    searchInput.addEventListener('input', function() {
      const query = this.value.trim();
      clearTimeout(searchTimeout);
      
      if (query.length >= 2) {
        searchTimeout = setTimeout(() => {
          fetch(`/buscar/sugestoes/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
              if (data.suggestions && data.suggestions.length > 0) {
                suggestionsContainer.innerHTML = '';
                data.suggestions.forEach(item => {
                  const a = document.createElement('a');
                  a.href = `/item/${item.slug}/`;
                  a.className = 'search-suggestion-item';
                  
                  const imgHtml = item.imagem 
                    ? `<img src="${item.imagem}" alt="${item.nome}" class="search-suggestion-img">`
                    : `<div class="search-suggestion-img d-flex align-items-center justify-content-center bg-light"><i class="bi bi-gem text-gold"></i></div>`;
                    
                  a.innerHTML = `
                    ${imgHtml}
                    <span style="font-weight: 500;">${item.nome}</span>
                  `;
                  suggestionsContainer.appendChild(a);
                });
                suggestionsContainer.classList.add('show');
              } else {
                suggestionsContainer.classList.remove('show');
              }
            })
            .catch(() => {
              suggestionsContainer.classList.remove('show');
            });
        }, 300);
      } else {
        suggestionsContainer.classList.remove('show');
      }
    });

    // Fechar ao clicar fora
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
        suggestionsContainer.classList.remove('show');
      }
    });
  }
});