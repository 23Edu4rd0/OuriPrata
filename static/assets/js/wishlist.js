// Wishlist — localStorage para visitantes anônimos, sincronizado com o servidor quando logado
const WISHLIST_KEY = 'ouriprata_wishlist';

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
}

function isAuthenticated() {
    return document.body.dataset.userAuthenticated === '1';
}

function toggleWishlistOnServer(slug) {
    const url = document.body.dataset.toggleWishlistUrl;
    if (!url) return;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: `slug=${encodeURIComponent(slug)}`,
    }).then(response => {
        if (!response.ok) {
            console.warn('[wishlist] server sync failed', response.status);
        }
    }).catch(err => {
        console.warn('[wishlist] server sync error', err);
    });
}

function getWishlist() {
    try {
        return JSON.parse(localStorage.getItem(WISHLIST_KEY)) || [];
    } catch {
        return [];
    }
}

function saveWishlist(items) {
    localStorage.setItem(WISHLIST_KEY, JSON.stringify(items));
    updateWishlistCount();
}

function isInWishlist(slug) {
    return getWishlist().some(item => item.slug === slug);
}

function toggleWishlist(data) {
    const items = getWishlist();
    const idx = items.findIndex(item => item.slug === data.slug);
    if (idx > -1) {
        items.splice(idx, 1);
    } else {
        items.push(data);
    }
    saveWishlist(items);
    return idx === -1;
}

function updateWishlistCount() {
    const count = getWishlist().length;
    document.querySelectorAll('[data-wishlist-count]').forEach(el => {
        el.textContent = count;
        el.classList.toggle('hidden', count === 0);
    });
}

function syncWishlistButtons() {
    document.querySelectorAll('[data-wishlist-toggle]').forEach(btn => {
        const active = isInWishlist(btn.dataset.slug);
        btn.classList.toggle('is-active', active);
        const icon = btn.querySelector('i');
        if (icon) {
            icon.classList.toggle('bi-heart', !active);
            icon.classList.toggle('bi-heart-fill', active);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    updateWishlistCount();
    syncWishlistButtons();

    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-wishlist-toggle]');
        if (!btn) return;
        e.preventDefault();
        e.stopPropagation();

        const data = {
            slug: btn.dataset.slug,
            name: btn.dataset.name,
            image: btn.dataset.image || '',
            price: btn.dataset.price || '',
            url: btn.dataset.url,
        };
        const added = toggleWishlist(data);
        syncWishlistButtons();

        if (isAuthenticated()) {
            toggleWishlistOnServer(data.slug);
        }

        if (typeof renderWishlistPage === 'function') {
            renderWishlistPage();
        }
    });
});
