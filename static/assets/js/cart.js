// ===== CART.JS — Carrinho em localStorage =====

const CART_KEY = 'op_cart';

function getCart() {
  try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; }
  catch { return []; }
}

function saveCart(items) {
  localStorage.setItem(CART_KEY, JSON.stringify(items));
  window.dispatchEvent(new CustomEvent('cart:changed', { detail: { items } }));
  _updateCartBadges();
}

function getCartCount() {
  return getCart().reduce((sum, i) => sum + i.quantity, 0);
}

function _updateCartBadges() {
  const n = getCartCount();
  document.querySelectorAll('[data-cart-count]').forEach(el => {
    el.textContent = n;
    el.classList.toggle('hidden', n === 0);
  });
}

function addToCart({ slug, name, price, image, url, variant = null }) {
  const items = getCart();
  const key = variant ? `${slug}__${variant}` : slug;
  const existing = items.find(i => i.key === key);
  if (existing) {
    existing.quantity += 1;
  } else {
    items.push({ key, slug, name, price, image, url, variant, quantity: 1 });
  }
  saveCart(items);
  _showCartToast(name);
}

function removeFromCart(key) {
  saveCart(getCart().filter(i => i.key !== key));
}

function updateQuantity(key, qty) {
  const items = getCart();
  const item = items.find(i => i.key === key);
  if (!item) return;
  if (qty <= 0) { removeFromCart(key); return; }
  item.quantity = qty;
  saveCart(items);
}

function clearCart() {
  saveCart([]);
}

function _showCartToast(name) {
  const wrap = document.getElementById('toastWrap') || (() => {
    const d = document.createElement('div');
    d.id = 'toastWrap';
    d.className = 'fixed top-[80px] right-5 z-[9999] flex flex-col gap-2 max-w-sm';
    document.body.appendChild(d);
    return d;
  })();

  const t = document.createElement('div');
  t.className = 'flex items-center gap-3 px-4 py-3.5 bg-white rounded-xl shadow-soft border-l-4 border-gold-400 text-sm text-ink animate-fade-up';

  // Montado com nós do DOM em vez de innerHTML: o nome da peça vem do banco e
  // com innerHTML um nome contendo HTML seria executado.
  const icon = document.createElement('i');
  icon.className = 'bi bi-bag-check text-gold-500';
  const msg = document.createElement('span');
  const strong = document.createElement('strong');
  strong.textContent = name;
  msg.appendChild(strong);
  msg.appendChild(document.createTextNode(' adicionado ao carrinho'));
  t.append(icon, msg);

  wrap.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// Wire up all [data-add-to-cart] buttons on the page
function _wireAddButtons() {
  document.querySelectorAll('[data-add-to-cart]').forEach(btn => {
    if (btn._cartWired) return;
    btn._cartWired = true;
    btn.addEventListener('click', () => {
      addToCart({
        slug:    btn.dataset.slug,
        name:    btn.dataset.name,
        price:   btn.dataset.price,
        image:   btn.dataset.image || '',
        url:     btn.dataset.url,
        variant: btn.dataset.variant || null,
      });
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  _updateCartBadges();
  _wireAddButtons();
});
