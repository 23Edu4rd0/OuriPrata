(function () {
  var toggleBtn = document.getElementById('navToggle');
  var closeBtn = document.getElementById('drawerClose');
  var drawer = document.getElementById('navDrawer');
  var backdrop = document.getElementById('drawerBackdrop');

  if (!toggleBtn || !drawer || !backdrop) return;

  function openDrawer() {
    drawer.classList.add('open');
    backdrop.classList.add('open');
    toggleBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    drawer.classList.remove('open');
    backdrop.classList.remove('open');
    toggleBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  toggleBtn.addEventListener('click', function () {
    if (drawer.classList.contains('open')) {
      closeDrawer();
    } else {
      openDrawer();
    }
  });

  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  backdrop.addEventListener('click', closeDrawer);

  // Navegar para outra página fecha o menu — evita que ele reapareça aberto
  // ao voltar pelo histórico (bfcache restaura o DOM como estava).
  drawer.querySelectorAll('a[href]').forEach(function (link) {
    link.addEventListener('click', closeDrawer);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer();
  });

  // Se a largura passar para desktop com o menu aberto, o drawer some mas o
  // scroll do body continuaria travado.
  window.addEventListener('resize', function () {
    if (window.innerWidth >= 768 && drawer.classList.contains('open')) closeDrawer();
  });
})();
