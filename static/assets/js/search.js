// ===== SEARCH.JS — Busca com sugestões AJAX =====

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('navSearch');
  const suggestionsBox = document.getElementById('searchSuggestions');
  let timeout;

  if (!searchInput || !suggestionsBox) return;

  searchInput.addEventListener('input', function () {
    const query = this.value.trim();
    clearTimeout(timeout);

    if (query.length < 2) {
      suggestionsBox.innerHTML = '';
      suggestionsBox.classList.add('hidden');
      return;
    }

    timeout = setTimeout(() => {
      fetch(`/buscar/sugestoes/?q=${encodeURIComponent(query)}`)
        .then(r => r.json())
        .then(data => {
          const items = data.suggestions || [];
          if (!items.length) {
            suggestionsBox.classList.add('hidden');
            return;
          }

          suggestionsBox.innerHTML = items.map(p => `
            <a href="/product/${p.slug}/"
              class="flex items-center gap-3 px-4 py-3 hover:bg-cream-50 transition-colors group">
              <div class="w-10 h-10 rounded-lg overflow-hidden bg-stone-100 shrink-0">
                ${p.image
                  ? `<img src="${p.image}" alt="${p.name}" class="w-full h-full object-cover">`
                  : `<div class="w-full h-full flex items-center justify-center"><i class="bi bi-gem text-xs text-ink/25"></i></div>`}
              </div>
              <span class="text-[13px] text-ink font-light group-hover:text-gold-600 transition-colors truncate">
                ${p.name}
              </span>
            </a>
          `).join('');

          // Separator + "ver todos"
          suggestionsBox.innerHTML += `
            <a href="/buscar/?q=${encodeURIComponent(query)}"
              class="flex items-center justify-between px-4 py-3 border-t border-ink/5 text-[10px] uppercase tracking-[0.2em] text-ink/40 hover:text-gold-500 transition-colors">
              Ver todos os resultados
              <i class="bi bi-arrow-right text-xs"></i>
            </a>`;

          suggestionsBox.classList.remove('hidden');
        })
        .catch(() => suggestionsBox.classList.add('hidden'));
    }, 280);
  });

  // Close on outside click
  document.addEventListener('click', e => {
    if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
      suggestionsBox.classList.add('hidden');
    }
  });

  // Close on Escape
  searchInput.addEventListener('keydown', e => {
    if (e.key === 'Escape') suggestionsBox.classList.add('hidden');
  });
});
