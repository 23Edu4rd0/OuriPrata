// ===== PRODUCTS.JS - Funcionalidades de Produtos =====

// ===== SISTEMA DE ALERTAS =====
function showAlert(type, message) {
  // Mapear tipos para classes Bootstrap e cores
  const alertConfig = {
    'success': {
      class: 'alert-success',
      icon: 'bi-check-circle-fill',
      color: '#198754',
      bgColor: 'rgba(25, 135, 84, 0.1)',
      borderColor: '#198754'
    },
    'danger': {
      class: 'alert-danger', 
      icon: 'bi-exclamation-triangle-fill',
      color: '#dc3545',
      bgColor: 'rgba(220, 53, 69, 0.1)',
      borderColor: '#dc3545'
    },
    'warning': {
      class: 'alert-warning',
      icon: 'bi-exclamation-circle-fill', 
      color: '#fd7e14',
      bgColor: 'rgba(253, 126, 20, 0.1)',
      borderColor: '#fd7e14'
    },
    'info': {
      class: 'alert-info',
      icon: 'bi-info-circle-fill',
      color: '#0dcaf0',
      bgColor: 'rgba(13, 202, 240, 0.1)', 
      borderColor: '#0dcaf0'
    }
  };

  const config = alertConfig[type] || alertConfig['info'];
  
  // Criar container de alertas se não existir
  let alertContainer = document.getElementById('alert-container');
  if (!alertContainer) {
    alertContainer = document.createElement('div');
    alertContainer.id = 'alert-container';
    alertContainer.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9998;
      max-width: 400px;
      width: auto;
      pointer-events: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
    `;
    
    // Responsividade para mobile
    if (window.innerWidth <= 576) {
      alertContainer.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        left: 10px;
        z-index: 9998;
        max-width: none;
        width: auto;
        pointer-events: none;
        display: flex;
        flex-direction: column;
        gap: 8px;
      `;
    }
    
    document.body.appendChild(alertContainer);
  }
  
  // Criar o alerta
  const alertId = 'alert-' + Date.now();
  const alert = document.createElement('div');
  alert.id = alertId;
  alert.style.cssText = `
    background: ${config.bgColor};
    border: 1px solid ${config.borderColor};
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    backdrop-filter: blur(10px);
    border-left: 4px solid ${config.color};
    pointer-events: auto;
    transform: translateX(100%);
    opacity: 0;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    font-family: 'Montserrat', sans-serif;
    position: relative;
    overflow: hidden;
    min-width: 300px;
    max-width: 100%;
    width: 100%;
  `;
  
  alert.innerHTML = `
    <div class="d-flex align-items-start">
      <div class="me-3" style="color: ${config.color}; font-size: 1.2rem;">
        <i class="${config.icon}"></i>
      </div>
      <div class="flex-grow-1">
        <div style="color: ${config.color}; font-weight: 600; margin-bottom: 4px;">
          ${type.charAt(0).toUpperCase() + type.slice(1)}
        </div>
        <div style="color: #333; font-size: 0.9rem; line-height: 1.4;">
          ${message}
        </div>
      </div>
      <button type="button" class="btn-close ms-2" onclick="removeAlert('${alertId}')" 
              style="font-size: 0.8rem; opacity: 0.6; border: none; background: none; color: ${config.color};">
        <i class="bi bi-x"></i>
      </button>
    </div>
  `;
  
  alertContainer.appendChild(alert);
  
  // Animar entrada
  setTimeout(() => {
    alert.style.transform = 'translateX(0)';
    alert.style.opacity = '1';
  }, 10);
  
  // Auto-remover após 5 segundos
  setTimeout(() => {
    removeAlert(alertId);
  }, 5000);
}

function removeAlert(alertId) {
  const alert = document.getElementById(alertId);
  if (alert) {
    alert.style.transform = 'translateX(100%)';
    alert.style.opacity = '0';
    setTimeout(() => {
      if (alert.parentNode) {
        alert.parentNode.removeChild(alert);
      }
    }, 400);
  }
}

// ===== CONTROLE DE QUANTIDADE =====
function updateQuantity(productId, change) {
  const quantityElement = document.getElementById(`quantity-${productId}`);
  const currentQuantity = parseInt(quantityElement.textContent);
  const newQuantity = Math.max(1, currentQuantity + change);
  
  quantityElement.textContent = newQuantity;
  
  // Atualizar preço total se existir
  const priceElement = document.getElementById(`price-${productId}`);
  const totalElement = document.getElementById(`total-${productId}`);
  if (priceElement && totalElement) {
    const price = parseFloat(priceElement.dataset.price);
    const total = price * newQuantity;
    totalElement.textContent = `R$ ${total.toFixed(2)}`;
  }
}

// ===== CARRINHO =====
function addToCart(productId, quantity = 1) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
  fetch('/cart/add/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({
      product_id: productId,
      quantity: quantity
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      showAlert('success', 'Produto adicionado ao carrinho!');
      updateCartCount(data.cart_count);
    } else {
      showAlert('danger', data.message || 'Erro ao adicionar produto.');
    }
  })
  .catch(error => {
    console.error('Erro:', error);
    showAlert('danger', 'Erro ao adicionar produto ao carrinho.');
  });
}

function removeFromCart(productId) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
  fetch('/cart/remove/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({
      product_id: productId
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      showAlert('success', 'Produto removido do carrinho!');
      updateCartCount(data.cart_count);
      // Remover elemento do DOM se estiver na página do carrinho
      const cartItem = document.getElementById(`cart-item-${productId}`);
      if (cartItem) {
        cartItem.remove();
      }
    } else {
      showAlert('danger', data.message || 'Erro ao remover produto.');
    }
  })
  .catch(error => {
    console.error('Erro:', error);
    showAlert('danger', 'Erro ao remover produto do carrinho.');
  });
}

function updateCartCount(count) {
  const cartCountElements = document.querySelectorAll('.cart-count');
  cartCountElements.forEach(element => {
    element.textContent = count;
  });
}

// ===== WISHLIST =====
function toggleWishlist(productId) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const wishlistBtn = document.getElementById(`wishlist-btn-${productId}`);
  
  fetch('/wishlist/toggle/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({
      product_id: productId
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      if (data.in_wishlist) {
        wishlistBtn.innerHTML = '<i class="bi bi-heart-fill text-danger"></i>';
        showAlert('success', 'Produto adicionado aos favoritos!');
      } else {
        wishlistBtn.innerHTML = '<i class="bi bi-heart"></i>';
        showAlert('warning', 'Produto removido dos favoritos.');
      }
    } else {
      showAlert('danger', data.message || 'Erro ao atualizar favoritos.');
    }
  })
  .catch(error => {
    console.error('Erro:', error);
    showAlert('danger', 'Erro ao atualizar favoritos.');
  });
}

// ===== TROCA DE IMAGENS =====
function changeImage(productId, imageUrl) {
  const mainImage = document.getElementById(`product-image-${productId}`);
  if (mainImage) {
    mainImage.src = imageUrl;
  }
}

// ===== COMPARTILHAMENTO =====
function shareProduct(productName, productUrl) {
  if (navigator.share) {
    navigator.share({
      title: productName,
      url: productUrl
    });
  } else {
    // Fallback para copiar URL
    navigator.clipboard.writeText(productUrl).then(() => {
      showAlert('success', 'Link copiado para a área de transferência!');
    });
  }
}

// ===== SISTEMA DE AVALIAÇÕES =====
function loadReviews(productSlug, page = 1, ratingFilter = null) {
  let url = `/reviews/${productSlug}/?page=${page}`;
  if (ratingFilter) url += `&rating=${ratingFilter}`;
  
  fetch(url)
    .then(response => response.json())
    .then(data => {
      updateReviewStats(data.stats);
      renderReviews(data.reviews);
      updatePagination(data.has_next, data.has_previous);
    })
    .catch(error => {
      console.error('Erro ao carregar avaliações:', error);
      showAlert('danger', 'Erro ao carregar avaliações.');
    });
}

function updateReviewStats(stats) {
  const avgRating = document.getElementById('avg-rating');
  const totalReviews = document.getElementById('total-reviews');
  const ratingBars = document.getElementById('rating-bars');
  
  if (avgRating) avgRating.textContent = stats.avg_rating?.toFixed(1) || '0.0';
  if (totalReviews) totalReviews.textContent = stats.total_reviews || 0;
  
  if (ratingBars) {
    const total = stats.total_reviews || 1;
    ratingBars.innerHTML = `
      <div class="rating-bar mb-2">
        <span>5 estrelas</span>
        <div class="progress" style="height: 8px;">
          <div class="progress-bar bg-warning" style="width: ${(stats.five_star / total) * 100}%"></div>
        </div>
        <span>${stats.five_star || 0}</span>
      </div>
      <div class="rating-bar mb-2">
        <span>4 estrelas</span>
        <div class="progress" style="height: 8px;">
          <div class="progress-bar bg-warning" style="width: ${(stats.four_star / total) * 100}%"></div>
        </div>
        <span>${stats.four_star || 0}</span>
      </div>
      <div class="rating-bar mb-2">
        <span>3 estrelas</span>
        <div class="progress" style="height: 8px;">
          <div class="progress-bar bg-warning" style="width: ${(stats.three_star / total) * 100}%"></div>
        </div>
        <span>${stats.three_star || 0}</span>
      </div>
      <div class="rating-bar mb-2">
        <span>2 estrelas</span>
        <div class="progress" style="height: 8px;">
          <div class="progress-bar bg-warning" style="width: ${(stats.two_star / total) * 100}%"></div>
        </div>
        <span>${stats.two_star || 0}</span>
      </div>
      <div class="rating-bar mb-2">
        <span>1 estrela</span>
        <div class="progress" style="height: 8px;">
          <div class="progress-bar bg-warning" style="width: ${(stats.one_star / total) * 100}%"></div>
        </div>
        <span>${stats.one_star || 0}</span>
      </div>
    `;
  }
}

function renderReviews(reviews) {
  const container = document.getElementById('reviews-container');
  if (!container) return;
  
  container.innerHTML = '';
  
  reviews.forEach(review => {
    const reviewElement = document.createElement('div');
    reviewElement.className = 'review-card border rounded p-3 mb-3';
    reviewElement.innerHTML = `
      <div class="d-flex justify-content-between align-items-start mb-2">
        <div>
          <h6 class="mb-1">${review.titulo || 'Avaliação'}</h6>
          <div class="stars-container">
            ${generateStars(review.rating)}
          </div>
        </div>
        <small class="text-muted">${new Date(review.data_criacao).toLocaleDateString('pt-BR')}</small>
      </div>
      <p class="mb-2">${review.comentario}</p>
      ${review.foto ? `<img src="${review.foto}" class="img-fluid rounded mb-2" style="max-width: 200px;">` : ''}
      <div class="d-flex justify-content-between align-items-center">
        <small class="text-muted">Por: ${review.usuario}</small>
        ${review.recomendado ? '<span class="badge bg-success">Recomenda</span>' : ''}
      </div>
    `;
    container.appendChild(reviewElement);
  });
}

function generateStars(rating) {
  let stars = '';
  for (let i = 1; i <= 5; i++) {
    if (i <= rating) {
      stars += '<i class="bi bi-star-fill text-warning"></i>';
    } else {
      stars += '<i class="bi bi-star text-muted"></i>';
    }
  }
  return stars;
}

function updatePagination(hasNext, hasPrevious) {
  const prevBtn = document.getElementById('prev-page');
  const nextBtn = document.getElementById('next-page');
  
  if (prevBtn) prevBtn.disabled = !hasPrevious;
  if (nextBtn) nextBtn.disabled = !hasNext;
}

function setupRatingStars() {
  const stars = document.querySelectorAll('.star-rating .bi');
  const ratingInput = document.getElementById('rating-input');
  
  stars.forEach((star, index) => {
    star.addEventListener('click', () => {
      const rating = index + 1;
      ratingInput.value = rating;
      
      // Atualizar visual das estrelas
      stars.forEach((s, i) => {
        if (i < rating) {
          s.classList.remove('bi-star');
          s.classList.add('bi-star-fill', 'text-warning');
        } else {
          s.classList.remove('bi-star-fill', 'text-warning');
          s.classList.add('bi-star');
        }
      });
    });
  });
}

function setupReviewForm() {
  const form = document.getElementById('review-form');
  if (!form) return;
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(form);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(form.action, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        showAlert('success', 'Avaliação enviada com sucesso!');
        // Recarregar avaliações
        const productSlug = form.dataset.productSlug;
        loadReviews(productSlug);
        // Fechar modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('reviewModal'));
        if (modal) modal.hide();
      } else {
        showAlert('danger', data.message || 'Erro ao enviar avaliação.');
      }
    })
    .catch(error => {
      console.error('Erro:', error);
      showAlert('danger', 'Erro ao enviar avaliação.');
    });
  });
}

// ===== INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', function() {
  // Configurar estrelas de avaliação se existirem
  const ratingStars = document.querySelector('.star-rating');
  if (ratingStars) {
    setupRatingStars();
  }
  
  // Configurar formulário de avaliação se existir
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    setupReviewForm();
  }
  
  // Carregar avaliações se estiver na página de produto
  const productSlug = document.querySelector('[data-product-slug]')?.dataset.productSlug;
  if (productSlug) {
    loadReviews(productSlug);
  }
  
  // Expor funções globalmente
  window.showAlert = showAlert;
  window.removeAlert = removeAlert;
  window.updateQuantity = updateQuantity;
  window.addToCart = addToCart;
  window.removeFromCart = removeFromCart;
  window.toggleWishlist = toggleWishlist;
  window.changeImage = changeImage;
  window.shareProduct = shareProduct;
  window.loadReviews = loadReviews;
}); 