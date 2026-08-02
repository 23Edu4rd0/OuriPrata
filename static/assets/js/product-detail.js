// --- Seletor de variante ---
(function () {
  const btns = document.querySelectorAll('.variant-btn');
  const cartBtn = document.getElementById('addToCartBtn');
  const stockMsg = document.getElementById('variantStockMsg');
  if (!btns.length) return;

  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      btns.forEach(b => b.classList.remove('border-gold-500', 'text-gold-600', 'bg-gold-50'));
      btn.classList.add('border-gold-500', 'text-gold-600', 'bg-gold-50');

      const variant = btn.dataset.variant;
      const stock = parseInt(btn.dataset.stock, 10);

      if (cartBtn) {
        cartBtn.dataset.variant = variant;
        cartBtn.disabled = false;
        cartBtn.querySelector('i').nextSibling.textContent = ' Adicionar ao carrinho';
      }
      if (stockMsg) {
        if (stock <= 3 && stock > 0) {
          stockMsg.textContent = `Apenas ${stock} unidade${stock > 1 ? 's' : ''} disponível${stock > 1 ? 'is' : ''} neste tamanho.`;
          stockMsg.className = 'text-[11px] text-amber-500 mt-2';
          stockMsg.classList.remove('hidden');
        } else {
          stockMsg.classList.add('hidden');
        }
      }
    });
  });
})();

// --- Galeria de miniaturas ---
const thumbs = document.querySelectorAll('.product-gallery__thumb');
const mainImg = document.getElementById('mainImg');

thumbs.forEach(thumb => {
  thumb.addEventListener('click', () => {
    mainImg.src = thumb.dataset.src;
    thumbs.forEach(t => t.classList.remove('border-ink'));
    thumb.classList.add('border-ink');
  });
});

// --- Zoom por cursor ---
(function () {
  const container = document.getElementById('zoomContainer');
  if (!container || !mainImg) return;
  const ZOOM = 1.6;
  container.addEventListener('mousemove', (e) => {
    const rect = container.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    mainImg.style.transformOrigin = `${x}% ${y}%`;
    mainImg.style.transform = `scale(${ZOOM})`;
  });
  container.addEventListener('mouseleave', () => {
    mainImg.style.transform = 'scale(1)';
    mainImg.style.transformOrigin = 'center';
  });
})();

// --- Lightbox ---
(function () {
  const lightbox = document.getElementById('lightbox');
  const lbImg = document.getElementById('lightboxImg');
  const lbClose = document.getElementById('lightboxClose');
  const lbPrev = document.getElementById('lightboxPrev');
  const lbNext = document.getElementById('lightboxNext');
  if (!lightbox) return;

  const sources = Array.from(thumbs).map(t => t.dataset.src).filter(Boolean);
  let current = 0;

  function openLightbox(src) {
    const norm = src.replace(window.location.origin, '');
    current = sources.findIndex(s => s === norm || s === src);
    if (current < 0) current = 0;
    lbImg.src = sources[current];
    lightbox.classList.remove('hidden');
    lightbox.classList.add('flex');
    document.body.style.overflow = 'hidden';
    const multi = sources.length > 1;
    lbPrev.classList.toggle('hidden', !multi);
    lbNext.classList.toggle('hidden', !multi);
  }

  function closeLightbox() {
    lightbox.classList.add('hidden');
    lightbox.classList.remove('flex');
    document.body.style.overflow = '';
  }

  function showSlide(idx) {
    current = (idx + sources.length) % sources.length;
    lbImg.src = sources[current];
  }

  // click na imagem principal ou no container abre o lightbox
  const zoomContainer = document.getElementById('zoomContainer');
  if (zoomContainer) {
    zoomContainer.addEventListener('click', (e) => {
      e.stopPropagation();
      if (mainImg && mainImg.src) openLightbox(mainImg.src);
    });
  }

  lbClose.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (e) => { if (e.target === lightbox) closeLightbox(); });
  lbPrev.addEventListener('click', (e) => { e.stopPropagation(); showSlide(current - 1); });
  lbNext.addEventListener('click', (e) => { e.stopPropagation(); showSlide(current + 1); });

  document.addEventListener('keydown', (e) => {
    if (lightbox.classList.contains('hidden')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') showSlide(current - 1);
    if (e.key === 'ArrowRight') showSlide(current + 1);
  });
})();

// --- Copiar link ---
(function () {
  const btn = document.getElementById('copyLinkBtn');
  const msg = document.getElementById('copiedMsg');
  if (!btn) return;
  btn.addEventListener('click', () => {
    navigator.clipboard.writeText(window.location.href).then(() => {
      msg.style.opacity = '1';
      setTimeout(() => { msg.style.opacity = '0'; }, 1800);
    });
  });
})();

// --- Descrição expansível ---
(function () {
  const text = document.getElementById('descText');
  const toggle = document.getElementById('descToggle');
  const label = document.getElementById('descToggleLabel');
  const icon = document.getElementById('descToggleIcon');
  if (!text || !toggle) return;

  if (text.scrollHeight > text.offsetHeight + 4) {
    toggle.classList.remove('hidden');
  }

  let expanded = false;
  toggle.addEventListener('click', () => {
    expanded = !expanded;
    text.style.maxHeight = expanded ? text.scrollHeight + 'px' : '96px';
    label.textContent = expanded ? 'Ler menos' : 'Ler mais';
    icon.className = expanded ? 'bi bi-chevron-up text-[9px]' : 'bi bi-chevron-down text-[9px]';
  });
})();

// --- Avaliações ---
(function () {
  const form = document.getElementById('reviewForm');
  if (!form) return;

  const ratingInput = document.getElementById('ratingInput');
  const ratingLabel = document.getElementById('ratingLabel');
  const stars = form.querySelectorAll('.star-pick');
  const submitBtn = form.querySelector('[type="submit"]');
  const formMsg = document.getElementById('reviewFormMsg');

  const LABELS = ['', 'Péssimo', 'Ruim', 'Regular', 'Bom', 'Excelente'];

  function setRating(val) {
    ratingInput.value = val;
    ratingLabel.textContent = val ? LABELS[val] + ` (${val}★)` : 'Selecione uma nota';
    stars.forEach(s => {
      const v = parseInt(s.dataset.value);
      s.className = `star-pick text-2xl transition-colors ${v <= val ? 'text-gold-500' : 'text-ink/15 hover:text-gold-300'}`;
    });
  }

  // Inicializar com a nota existente
  const initial = parseInt(ratingInput.value) || 0;
  if (initial) setRating(initial);

  stars.forEach(s => {
    s.addEventListener('mouseover', () => {
      const v = parseInt(s.dataset.value);
      stars.forEach(st => {
        const sv = parseInt(st.dataset.value);
        st.querySelector('i').className = `bi ${sv <= v ? 'bi-star-fill' : 'bi-star'} pointer-events-none`;
      });
    });
    s.addEventListener('mouseleave', () => {
      const cur = parseInt(ratingInput.value) || 0;
      stars.forEach(st => {
        st.querySelector('i').className = 'bi bi-star-fill pointer-events-none';
      });
      setRating(cur);
    });
    s.addEventListener('click', () => setRating(parseInt(s.dataset.value)));
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const rating = parseInt(ratingInput.value);
    if (!rating) {
      formMsg.textContent = 'Selecione uma nota antes de publicar.';
      return;
    }
    submitBtn.disabled = true;
    submitBtn.textContent = 'Enviando…';
    formMsg.textContent = '';

    const data = new FormData(form);
    try {
      const res = await fetch(form.dataset.url, {
        method: 'POST',
        headers: { 'X-CSRFToken': data.get('csrfmiddlewaretoken') },
        body: data,
      });
      const json = await res.json();
      if (!res.ok) {
        formMsg.textContent = json.error || 'Ocorreu um erro.';
        return;
      }

      // Atualizar resumo numérico
      document.getElementById('avgRatingDisplay').textContent = json.avg_rating.toFixed(1).replace('.', ',');
      document.getElementById('reviewCountDisplay').textContent =
        json.review_count + (json.review_count === 1 ? ' avaliação' : ' avaliações');

      // Remover mensagem "sem avaliações"
      const noMsg = document.getElementById('noReviewsMsg');
      if (noMsg) noMsg.remove();

      // Inserir ou atualizar card da avaliação no topo da lista
      const list = document.getElementById('reviewsList');
      const existingCard = list.querySelector('[data-own-review]');
      const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
      }[c]));
      const username = esc(json.username);
      const comment = esc(json.comment);
      const initial = username ? username[0].toUpperCase() : '?';
      const starsHtml = [1,2,3,4,5].map(i =>
        `<i class="bi ${i <= json.rating ? 'bi-star-fill text-gold-500' : 'bi-star text-ink/15'} text-[11px]"></i>`
      ).join('');
      const commentHtml = comment
        ? `<p class="text-[13px] text-ink/70 leading-relaxed font-light">${comment}</p>`
        : '';
      const cardHtml = `
        <div data-own-review class="flex gap-5 mb-8 pb-8 border-b border-ink/5">
          <div class="shrink-0 w-9 h-9 rounded-full bg-gold-50 border border-gold-200 flex items-center justify-center text-gold-600 text-[13px] font-medium uppercase select-none">${initial}</div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between mb-1.5 gap-4">
              <span class="text-[13px] font-medium text-ink truncate">${username}</span>
              <span class="text-[10px] text-ink/30 shrink-0">${json.date}</span>
            </div>
            <div class="flex items-center gap-0.5 mb-2.5">${starsHtml}</div>
            ${commentHtml}
          </div>
        </div>`;

      if (existingCard) {
        existingCard.outerHTML = cardHtml;
      } else {
        list.insertAdjacentHTML('afterbegin', cardHtml);
      }

      submitBtn.textContent = 'Atualizar';
      formMsg.textContent = json.created ? 'Avaliação publicada!' : 'Avaliação atualizada!';
      setTimeout(() => { formMsg.textContent = ''; }, 3000);
    } catch {
      formMsg.textContent = 'Erro de conexão. Tente novamente.';
    } finally {
      submitBtn.disabled = false;
    }
  });
})();
