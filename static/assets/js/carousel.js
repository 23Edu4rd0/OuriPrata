document.addEventListener("DOMContentLoaded", () => {
  const carousel = document.getElementById("heroCarousel");
  if (!carousel) return;

  const slides = carousel.querySelectorAll(".carousel-slide");
  const dots = carousel.querySelectorAll(".carousel-dot");
  const prevBtn = document.getElementById("carouselPrev");
  const nextBtn = document.getElementById("carouselNext");

  let current = 0;
  let autoplayTimer = null;
  const AUTOPLAY_DELAY = 6000;

  function goToSlide(index) {
    slides[current].classList.remove("opacity-100");
    slides[current].classList.add("opacity-0");
    dots[current].classList.remove("bg-white");
    dots[current].classList.add("bg-white/40");

    current = (index + slides.length) % slides.length;

    slides[current].classList.remove("opacity-0");
    slides[current].classList.add("opacity-100");
    dots[current].classList.remove("bg-white/40");
    dots[current].classList.add("bg-white");
  }

  function nextSlide() { goToSlide(current + 1); }
  function prevSlide() { goToSlide(current - 1); }

  function startAutoplay() {
    stopAutoplay();
    autoplayTimer = setInterval(nextSlide, AUTOPLAY_DELAY);
  }
  function stopAutoplay() {
    if (autoplayTimer) clearInterval(autoplayTimer);
  }

  nextBtn?.addEventListener("click", () => { nextSlide(); startAutoplay(); });
  prevBtn?.addEventListener("click", () => { prevSlide(); startAutoplay(); });

  dots.forEach((dot) => {
    dot.addEventListener("click", () => {
      goToSlide(parseInt(dot.dataset.index, 10));
      startAutoplay();
    });
  });

  // Pausa o autoplay quando o mouse está em cima (desktop)
  carousel.addEventListener("mouseenter", stopAutoplay);
  carousel.addEventListener("mouseleave", startAutoplay);

  startAutoplay();
});