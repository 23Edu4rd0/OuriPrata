// ===== SEARCH.JS - Funcionalidade de Busca Rápida =====

document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const suggestionsContainer = document.getElementById('search-suggestions');
  const suggestionsList = document.getElementById('suggestions-list');
  let searchTimeout;

  if (searchInput && suggestionsContainer && suggestionsList) {
    searchInput.addEventListener('input', function() {
      const query = this.value.trim();
      clearTimeout(searchTimeout);
      
      if (query.length >= 2) {
        searchTimeout = setTimeout(() => {
          fetch(`/buscar/sugestoes/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
              if (data.suggestions && data.suggestions.length > 0) {
                suggestionsList.innerHTML = '';
                data.suggestions.forEach(item => {
                  const div = document.createElement('div');
                  div.className = 'p-2 border-bottom suggestion-item';
                  div.style.cursor = 'pointer';
                  
                  const imgHtml = item.imagem 
                    ? `<img src="${item.imagem}" alt="${item.nome}" class="rounded me-2" style="width: 30px; height: 30px; object-fit: cover;">`
                    : `<i class="bi bi-gem text-warning me-2" style="font-size: 1.2rem;"></i>`;
                    
                  div.innerHTML = `
                    <a href="/item/${item.slug}/" class="d-flex align-items-center text-decoration-none text-dark p-1">
                      ${imgHtml}
                      <span class="small fw-semibold">${item.nome}</span>
                    </a>
                  `;
                  suggestionsList.appendChild(div);
                });
                suggestionsContainer.classList.remove('d-none');
              } else {
                suggestionsContainer.classList.add('d-none');
              }
            })
            .catch(() => {
              suggestionsContainer.classList.add('d-none');
            });
        }, 300);
      } else {
        suggestionsContainer.classList.add('d-none');
      }
    });

    // Fechar ao clicar fora
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
        suggestionsContainer.classList.add('d-none');
      }
    });
  }
});