// Quick View — abre modal com detalhes básicos do produto sem sair do grid
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('quickViewModal');
    if (!modal) return;

    const backdrop = document.getElementById('quickViewBackdrop');
    const closeBtn = document.getElementById('quickViewClose');
    const image = document.getElementById('quickViewImage');
    const category = document.getElementById('quickViewCategory');
    const name = document.getElementById('quickViewName');
    const price = document.getElementById('quickViewPrice');
    const link = document.getElementById('quickViewLink');

    function openQuickView(data) {
        image.src = data.image || '';
        image.alt = data.name || '';
        category.textContent = data.category || '';
        category.classList.toggle('hidden', !data.category);
        name.textContent = data.name || '';
        price.textContent = data.price || '';
        link.href = data.url || '#';
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.body.style.overflow = 'hidden';
    }

    function closeQuickView() {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        document.body.style.overflow = '';
    }

    document.body.addEventListener('click', (e) => {
        const trigger = e.target.closest('[data-quick-view]');
        if (!trigger) return;
        e.preventDefault();
        e.stopPropagation();
        openQuickView(trigger.dataset);
    });

    backdrop?.addEventListener('click', closeQuickView);
    closeBtn?.addEventListener('click', closeQuickView);
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeQuickView();
    });
});
