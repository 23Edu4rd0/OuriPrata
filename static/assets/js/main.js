document.addEventListener('DOMContentLoaded', () => {
    // 1. Efeito de scroll da Navbar
    const nav = document.getElementById('opNav');
    if (nav) {
        window.addEventListener('scroll', () => {
            nav.classList.toggle('scrolled', window.scrollY > 10);
        }, { passive: true });
    }

    // 2. Mobile drawer (Menu lateral)
    const toggle   = document.getElementById('navToggle');
    const drawer   = document.getElementById('navDrawer');
    const backdrop = document.getElementById('drawerBackdrop');

    function openDrawer()  { drawer?.classList.add('open'); document.body.style.overflow = 'hidden'; }
    function closeDrawer() { drawer?.classList.remove('open'); document.body.style.overflow = ''; }

    toggle?.addEventListener('click', openDrawer);
    backdrop?.addEventListener('click', closeDrawer);

    // 3. Fade-out suave para as mensagens (Toasts)
    document.querySelectorAll('.op-toast').forEach(t => {
        setTimeout(() => {
            t.style.opacity = '0';
            t.style.transform = 'translateY(-10px)';
            setTimeout(() => t.remove(), 300); // Sincronizado com o duration-300 do Tailwind
        }, 4000);
    });
});