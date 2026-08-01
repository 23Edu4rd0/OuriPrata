/**
 * Carrossel de produtos — controla todos os blocos [data-carousel] da página.
 *
 * No mobile a navegação é o próprio arraste: o trilho é um scroll horizontal
 * nativo com snap, então não há nada para o JS fazer além de acompanhar o
 * estado. As setas existem só no desktop e avançam uma "página" (a largura
 * visível do trilho).
 *
 * A visibilidade das setas fica no CSS: aqui só marcamos data-overflow no
 * elemento raiz e o template decide quando mostrá-las (md+ e com transbordo).
 *
 * A animação é do scroll suave nativo (scroll-smooth no trilho): quem anima é
 * o compositor do navegador, então não trava.
 */
(function () {
  var carousels = document.querySelectorAll('[data-carousel]');
  if (!carousels.length) return;

  carousels.forEach(function (root) {
    var track = root.querySelector('[data-carousel-track]');
    var prev = root.querySelector('[data-carousel-prev]');
    var next = root.querySelector('[data-carousel-next]');
    if (!track || !prev || !next) return;

    // Margem de 1px absorve o arredondamento sub-pixel da largura dos cards,
    // senão a seta "próximo" nunca desabilita no fim do trilho.
    var EPS = 1;

    function maxScroll() {
      return track.scrollWidth - track.clientWidth;
    }

    function update() {
      var max = maxScroll();
      root.dataset.overflow = max > EPS ? 'true' : 'false';
      prev.disabled = track.scrollLeft <= EPS;
      next.disabled = track.scrollLeft >= max - EPS;
    }

    function paginar(direcao) {
      var destino = track.scrollLeft + direcao * track.clientWidth;
      track.scrollTo({ left: Math.max(0, Math.min(destino, maxScroll())) });
    }

    prev.addEventListener('click', function () { paginar(-1); });
    next.addEventListener('click', function () { paginar(1); });

    // Cobre tanto o arraste no celular quanto a paginação pelas setas.
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);

    // As imagens dos cards carregam depois e mudam as medidas do trilho.
    if (window.ResizeObserver) {
      new ResizeObserver(update).observe(track);
    }

    update();
  });
})();
