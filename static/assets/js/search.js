// ===== SEARCH.JS - Funcionalidades de Busca =====

let searchTimeout;
let isRecording = false;

function setupSearchSuggestions(input, container, list, version) {
  const historyElement = version === 'desktop' ? document.getElementById('search-history') : document.getElementById('search-history-mobile');
  const historyListElement = version === 'desktop' ? document.getElementById('history-list') : document.getElementById('history-list-mobile');
  const popularElement = version === 'desktop' ? document.getElementById('popular-categories') : document.getElementById('popular-categories-mobile');
  
  input.addEventListener('focus', function() {
    const query = this.value.trim();
    if (query.length === 0) {
      showHistoryAndCategories(historyElement, historyListElement, popularElement);
    } else if (query.length >= 2) {
      fetchSuggestions(query, container, list);
    }
  });
  
  input.addEventListener('input', function() {
    const query = this.value.trim();
    clearTimeout(searchTimeout);
    
    if (query.length >= 2) {
      searchTimeout = setTimeout(() => {
        fetchSuggestions(query, container, list);
      }, 300);
    } else if (query.length === 0) {
      showHistoryAndCategories(historyElement, historyListElement, popularElement);
    } else {
      hideSuggestions(container);
    }
  });
  
  input.addEventListener('blur', function() {
    setTimeout(() => {
      hideSuggestions(container);
    }, 200);
  });
  
  input.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      const query = this.value.trim();
      if (query.length > 0) {
        addToSearchHistory(query);
        window.location.href = `/buscar/?q=${encodeURIComponent(query)}`;
      }
    }
  });
}

function fetchSuggestions(query, container, list) {
  fetch(`/sugestoes/?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
      if (data.suggestions && data.suggestions.length > 0) {
        displaySuggestions(data.suggestions, list);
        showSuggestions(container);
      } else {
        hideSuggestions(container);
      }
    })
    .catch(error => {
      console.error('Erro ao buscar sugestões:', error);
      hideSuggestions(container);
    });
}

function displaySuggestions(suggestions, list) {
  list.innerHTML = '';
  
  if (suggestions.length === 0) {
    list.innerHTML = `
      <div class="p-3 text-center text-muted">
        <i class="bi bi-search mb-2"></i>
        <div>Nenhum produto encontrado</div>
      </div>
    `;
    return;
  }
  
  suggestions.forEach(suggestion => {
    const item = document.createElement('div');
    item.className = 'suggestion-item p-2 border-bottom';
    item.style.cursor = 'pointer';
    
    if (typeof suggestion === 'string') {
      item.innerHTML = `
        <div class="d-flex align-items-center">
          <i class="bi bi-search me-2 text-muted"></i>
          <span>${suggestion}</span>
        </div>
      `;
      item.addEventListener('click', () => {
        addToSearchHistory(suggestion);
        window.location.href = `/buscar/?q=${encodeURIComponent(suggestion)}`;
      });
    } else {
      const price = suggestion.em_promocao && suggestion.preco_promocional 
        ? `<span class="text-muted text-decoration-line-through small">R$ ${suggestion.preco}</span> <span class="text-success fw-bold">R$ ${suggestion.preco_promocional}</span>`
        : `<span class="fw-bold">R$ ${suggestion.preco}</span>`;
        
      const image = suggestion.imagem 
        ? `<img src="${suggestion.imagem}" alt="${suggestion.nome}" class="rounded" style="width: 40px; height: 40px; object-fit: cover;">`
        : `<div class="bg-light rounded d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;"><i class="bi bi-image text-muted"></i></div>`;
        
      item.innerHTML = `
        <a href="/item/${suggestion.slug}/" class="d-flex align-items-center gap-3 p-3 text-decoration-none text-dark" onclick="addToSearchHistory('${suggestion.nome}')">
          ${image}
          <div class="flex-grow-1">
            <div class="fw-medium mb-1">${suggestion.nome}</div>
            <div class="small">${price}</div>
          </div>
          ${suggestion.em_promocao ? '<span class="badge bg-danger small">Promoção</span>' : ''}
        </a>
      `;
    }
    
    list.appendChild(item);
  });
}

function showSuggestions(container) {
  container.style.display = 'block';
}

function hideSuggestions(container) {
  container.style.display = 'none';
}

function showHistoryAndCategories(historyElement, historyListElement, popularElement) {
  const container = historyElement ? historyElement.parentElement : popularElement ? popularElement.parentElement : null;
  
  if (historyElement && historyListElement) {
    const history = getSearchHistory();
    if (history.length > 0) {
      displaySearchHistory(history, historyListElement);
      historyElement.style.display = 'block';
    } else {
      historyElement.style.display = 'none';
    }
  }
  
  if (popularElement) {
    popularElement.style.display = 'block';
  }
  
  if (container) {
    container.style.display = 'block';
  }
}

function displaySearchHistory(history, list) {
  list.innerHTML = '';
  history.slice(0, 5).forEach(term => {
    const item = document.createElement('div');
    item.className = 'mb-2';
    item.innerHTML = `
      <button class="btn btn-outline-secondary btn-sm w-100 text-start" onclick="searchTerm('${term}')">
        <i class="bi bi-clock-history me-2"></i>
        ${term}
      </button>
    `;
    list.appendChild(item);
  });
  
  if (history.length > 0) {
    const clearBtn = document.createElement('div');
    clearBtn.className = 'mt-2';
    clearBtn.innerHTML = `
      <button class="btn btn-outline-danger btn-sm w-100" onclick="clearSearchHistory()">
        <i class="bi bi-trash me-2"></i>
        Limpar Histórico
      </button>
    `;
    list.appendChild(clearBtn);
  }
}

function getSearchHistory() {
  const history = localStorage.getItem('searchHistory');
  return history ? JSON.parse(history) : [];
}

function addToSearchHistory(term) {
  const history = getSearchHistory();
  const filteredHistory = history.filter(item => item !== term);
  const newHistory = [term, ...filteredHistory].slice(0, 10);
  localStorage.setItem('searchHistory', JSON.stringify(newHistory));
}

function clearSearchHistory(version) {
  localStorage.removeItem('searchHistory');
  if (version === 'mobile') {
    const historyElement = document.getElementById('search-history-mobile');
    const historyListElement = document.getElementById('history-list-mobile');
    if (historyElement) historyElement.style.display = 'none';
    if (historyListElement) historyListElement.innerHTML = '';
  } else {
    const historyElement = document.getElementById('search-history');
    const historyListElement = document.getElementById('history-list');
    if (historyElement) historyElement.style.display = 'none';
    if (historyListElement) historyListElement.innerHTML = '';
  }
}

function searchCategory(category, version) {
  addToSearchHistory(category);
  window.location.href = `/categoria/${category.toLowerCase()}/`;
}

function searchTerm(term) {
  addToSearchHistory(term);
  window.location.href = `/buscar/?q=${encodeURIComponent(term)}`;
}

function applyAdvancedSearch() {
  const category = document.getElementById('search-category')?.value;
  const price = document.getElementById('search-price')?.value;
  
  let url = '/buscar/?';
  const params = [];
  
  if (category) params.push(`categoria=${encodeURIComponent(category)}`);
  if (price) params.push(`preco=${encodeURIComponent(price)}`);
  
  if (params.length > 0) {
    url += params.join('&');
    window.location.href = url;
  }
} 