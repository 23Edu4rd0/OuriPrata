document.addEventListener('DOMContentLoaded', () => {
    // 1. Efeito de scroll da Navbar
    const nav = document.getElementById('opNav');
    if (nav) {
        window.addEventListener('scroll', () => {
            nav.classList.toggle('scrolled', window.scrollY > 10);
        }, { passive: true });
    }

    // 2. O menu lateral mobile é controlado por navbar.js

    // 3. Fade-out suave para as mensagens (Toasts)
    document.querySelectorAll('.op-toast').forEach(t => {
        setTimeout(() => {
            t.style.opacity = '0';
            t.style.transform = 'translateY(-10px)';
            setTimeout(() => t.remove(), 300); // Sincronizado com o duration-300 do Tailwind
        }, 4000);
    });
});