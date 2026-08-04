function renderWishlistPage() {
  const items = getWishlist();
  const grid = document.getElementById('wishlistGrid');
  const empty = document.getElementById('wishlistEmpty');
  const countLabel = document.getElementById('wishlistCountLabel');
  if (!grid) return;

  const n = items.length;
  countLabel.textContent = n === 0 ? '' : `${n} peça${n === 1 ? '' : 's'} salva${n === 1 ? '' : 's'}`;

  if (n === 0) {
    grid.innerHTML = '';
    empty.classList.remove('hidden');
    return;
  }
  empty.classList.add('hidden');

  // Tudo vem do localStorage — escapar antes de virar HTML, inclusive o que
  // entra em atributos (data-*, src, href).
  grid.innerHTML = items.map(item => {
    const nome = escapeHtml(item.name);
    const url = escapeHtml(item.url);
    const imagem = escapeHtml(item.image || '');
    const slug = escapeHtml(item.slug);
    const preco = escapeHtml(item.price || '');
    return `
    <div class="product-item group">
      <div class="relative w-full aspect-square overflow-hidden bg-stone-50 rounded-lg mb-4">
        <a href="${url}" class="block w-full h-full">
          ${item.image
            ? `<img src="${imagem}" alt="${nome}" loading="lazy"
                 class="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105">`
            : `<div class="w-full h-full flex items-center justify-center"><i class="bi bi-gem text-2xl text-ink/15"></i></div>`}
        </a>
        <button type="button" data-wishlist-toggle data-slug="${slug}" data-name="${nome}"
          data-image="${imagem}" data-price="${preco}" data-url="${url}"
          aria-label="Remover dos favoritos"
          class="wishlist-btn is-active absolute top-3 right-3 w-8 h-8 flex items-center justify-center rounded-full bg-white/85 backdrop-blur-sm text-gold-500 hover:text-red-400 transition-colors">
          <i class="bi bi-heart-fill text-sm" aria-hidden="true"></i>
        </button>
      </div>
      <a href="${url}" class="block px-0.5">
        <h3 class="font-serif text-[15px] text-ink font-light leading-snug mb-1.5 group-hover:text-gold-600 transition-colors duration-300">
          ${nome}
        </h3>
        ${item.price
          ? `<span class="text-[12px] text-ink/50 tracking-wider">R$ ${preco}</span>`
          : `<span class="text-[10px] uppercase tracking-widest text-ink/35">Consulte</span>`}
      </a>
    </div>`;
  }).join('');

  grid.querySelectorAll('[data-wishlist-toggle]').forEach(btn => {
    btn.addEventListener('click', () => {
      setTimeout(renderWishlistPage, 50);
    });
  });
}

document.addEventListener('DOMContentLoaded', renderWishlistPage);
window.addEventListener('wishlist:changed', renderWishlistPage);
