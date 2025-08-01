// Sistema de Avaliações - OuriPrata
// Arquivo: static/assets/js/review-system.js

console.log('Review system loaded successfully!');

// Função global para atualizar visual das estrelas
function updateStars(selectedRating) {
  const stars = document.querySelectorAll('.star-btn');
  stars.forEach((star) => {
    const value = parseInt(star.dataset.value);
    if (selectedRating > 0 && value <= selectedRating) {
      star.classList.add('selected');
      star.style.color = '#ffc107';
    } else {
      star.classList.remove('selected');
      star.style.color = '#dee2e6';
    }
  });
}

// Configurar estrelas de rating
function setupSimpleStars() {
  const stars = document.querySelectorAll('.star-btn');
  const ratingInput = document.getElementById('rating-input');
  
  if (!ratingInput) {
    console.error('Rating input not found');
    return;
  }
  
  // Definir rating padrão como 0 (todas cinzas)
  ratingInput.value = 0;
  updateStars(0);
  
  // Adicionar event listeners para cada estrela
  stars.forEach((star) => {
    star.addEventListener('click', function() {
      const rating = parseInt(this.dataset.value);
      ratingInput.value = rating;
      updateStars(rating);
    });
  });
}

// Mostrar modal de avaliação
function showReviewForm() {
  console.log('showReviewForm called!');
  console.log('Opening review modal...');
  const modal = document.getElementById('reviewModal');
  
  if (modal) {
    // Forçar o modal a aparecer
    modal.style.display = 'block';
    modal.style.zIndex = '9999';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    
    // Resetar formulário
    const form = document.getElementById('reviewForm');
    form.reset();
    
    // Limpar preview de imagens existentes
    const existingPreviews = document.querySelectorAll('.mb-3');
    existingPreviews.forEach(preview => {
      const label = preview.querySelector('label');
      if (label && label.textContent.includes('Imagens Atuais')) {
        preview.remove();
      }
    });
    
    // Resetar botão de submit
    const submitBtn = document.getElementById('submit-review-btn');
    submitBtn.textContent = 'Enviar Avaliação';
    submitBtn.onclick = submitReview;
    submitBtn.disabled = false;
    
    setupSimpleStars();
    
    // Fechar ao clicar fora
    modal.addEventListener('click', function(e) {
      if (e.target === modal) {
        closeReviewModal();
      }
    });
    
  } else {
    console.error('Modal not found!');
  }
}

// Fechar modal de avaliação
function closeReviewModal() {
  const modal = document.getElementById('reviewModal');
  if (modal) {
    modal.style.display = 'none';
    
    // Limpar preview de imagens existentes
    const existingPreviews = document.querySelectorAll('.mb-3');
    existingPreviews.forEach(preview => {
      const label = preview.querySelector('label');
      if (label && label.textContent.includes('Imagens Atuais')) {
        preview.remove();
      }
    });
    
    // Resetar formulário
    const form = document.getElementById('reviewForm');
    if (form) {
      form.reset();
    }
    
    // Resetar botão
    const submitBtn = document.getElementById('submit-review-btn');
    if (submitBtn) {
      submitBtn.textContent = 'Enviar Avaliação';
      submitBtn.onclick = submitReview;
      submitBtn.disabled = false;
    }
  }
}

// Enviar nova avaliação
function submitReview() {
  console.log('Submitting review...');
  const form = document.getElementById('reviewForm');
  
  if (!form) {
    console.error('Review form not found');
    alert('Erro: formulário não encontrado');
    return;
  }
  
  const formData = new FormData(form);
  
  // Validar campos obrigatórios
  const comment = formData.get('comment');
  const rating = formData.get('rating');
  
  if (!comment.trim()) {
    showAlert('warning', 'Por favor, escreva um comentário.');
    return;
  }
  
  if (!rating || rating == '0') {
    showAlert('warning', 'Por favor, selecione uma avaliação.');
    return;
  }
  
  // Mostrar loading no botão
  const submitBtn = document.getElementById('submit-review-btn');
  if (!submitBtn) {
    console.error('Submit button not found');
    alert('Erro: botão de envio não encontrado');
    return;
  }
  
  const originalText = submitBtn.textContent;
  submitBtn.textContent = 'Enviando...';
  submitBtn.disabled = true;
  
  // Pegar o slug do produto da URL atual
  const currentPath = window.location.pathname;
  const productSlug = currentPath.split('/').filter(part => part)[1]; // /item/alianca/ -> alianca
  
  // Verificar se o CSRF token está presente
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
  if (!csrfToken) {
    console.error('CSRF token not found');
    showAlert('danger', 'Erro de segurança. Recarregue a página.');
    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
    return;
  }
  
  // Garantir que o CSRF token está no FormData
  formData.append('csrfmiddlewaretoken', csrfToken.value);
  
  // Enviar avaliação
  fetch(`/avaliar/${productSlug}/`, {
    method: 'POST',
    body: formData
  })
  .then(response => {
    console.log('Response status:', response.status);
    console.log('Response headers:', response.headers);
    return response.json();
  })
  .then(data => {
    console.log('Response data:', data);
    if (data.status === 'success') {
      showAlert('success', 'Avaliação enviada com sucesso!');
      closeReviewModal();
      
      // Recarregar a página para mostrar a avaliação
      setTimeout(() => {
        window.location.reload();
      }, 1500);
    } else {
      showAlert('danger', data.message || 'Erro ao enviar avaliação.');
      // Restaurar botão
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  })
  .catch(error => {
    console.error('Erro:', error);
    showAlert('danger', 'Erro de conexão. Tente novamente.');
    // Restaurar botão
    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
  });
}

// Editar avaliação existente
function editReview() {
  console.log('editReview called!');
  console.log('editReview function called');
  
  // Verificar se há dados da avaliação do usuário
  if (!window.userReviewId) {
    console.error('No user review data found');
    return;
  }
  
  // Mostrar o modal
  const modal = document.getElementById('reviewModal');
  if (modal) {
    modal.style.display = 'block';
    modal.style.zIndex = '9999';
  } else {
    console.error('Modal not found in editReview');
    return;
  }
  
  // Preencher o formulário com os dados da avaliação atual
  const form = document.getElementById('reviewForm');
  const ratingInput = document.getElementById('rating-input');
  const commentInput = document.getElementById('comment');
  const imagesInput = document.getElementById('images');
  
  if (ratingInput && commentInput) {
    // Preencher com os dados da avaliação existente
    ratingInput.value = window.userReviewRating || 0;
    commentInput.value = window.userReviewComment || '';
    
    // Atualizar as estrelas visualmente
    updateStars(window.userReviewRating || 0);
    
    // Mostrar imagens existentes se houver
    if (window.userReviewImages && window.userReviewImages.length > 0) {
      const imagePreviewContainer = document.createElement('div');
      imagePreviewContainer.className = 'mb-3';
      imagePreviewContainer.innerHTML = '<label class="form-label fw-semibold">Imagens Atuais:</label><div class="d-flex gap-2 flex-wrap"></div>';
      
      const imageContainer = imagePreviewContainer.querySelector('.d-flex');
      window.userReviewImages.forEach(imageUrl => {
        const imgDiv = document.createElement('div');
        imgDiv.className = 'position-relative';
        imgDiv.innerHTML = `
          <img src="${imageUrl}" alt="Imagem da avaliação" style="width: 80px; height: 80px; object-fit: cover; border-radius: 4px;">
          <small class="text-muted d-block mt-1">Imagem atual</small>
        `;
        imageContainer.appendChild(imgDiv);
      });
      
      // Inserir antes do campo de imagens
      const imagesField = document.querySelector('label[for="images"]').parentElement;
      imagesField.parentElement.insertBefore(imagePreviewContainer, imagesField);
    }
    
    // Mudar o texto do botão de submit
    const submitBtn = document.getElementById('submit-review-btn');
    submitBtn.textContent = 'Atualizar Avaliação';
    submitBtn.onclick = updateReview;
  }
  
}

// Atualizar avaliação existente
function updateReview() {
  console.log('Updating review...');
  const form = document.getElementById('reviewForm');
  const formData = new FormData(form);
  
  // Validar campos obrigatórios
  const comment = formData.get('comment');
  const rating = formData.get('rating');
  
  if (!comment.trim()) {
    showAlert('warning', 'Por favor, escreva um comentário.');
    return;
  }
  
  if (!rating || rating == '0') {
    showAlert('warning', 'Por favor, selecione uma avaliação.');
    return;
  }
  
  // Verificar se há dados da avaliação do usuário
  if (!window.userReviewId) {
    showAlert('danger', 'Erro: dados da avaliação não encontrados.');
    return;
  }
  
  // Verificar se o CSRF token está presente
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
  if (!csrfToken) {
    console.error('CSRF token not found');
    showAlert('danger', 'Erro de segurança. Recarregue a página.');
    return;
  }
  
  // Garantir que o CSRF token está no FormData
  formData.append('csrfmiddlewaretoken', csrfToken.value);
  
  // Mostrar loading no botão
  const submitBtn = document.getElementById('submit-review-btn');
  const originalText = submitBtn.textContent;
  submitBtn.textContent = 'Atualizando...';
  submitBtn.disabled = true;
  
  // Enviar atualização
  fetch(`/editar-avaliacao/${window.userReviewId}/`, {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      showAlert('success', 'Avaliação atualizada com sucesso!');
      closeReviewModal();
      
      // Recarregar a página para mostrar a avaliação atualizada
      setTimeout(() => {
        window.location.reload();
      }, 1500);
    } else {
      showAlert('danger', data.message || 'Erro ao atualizar avaliação.');
      // Restaurar botão
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  })
  .catch(error => {
    console.error('Erro:', error);
    showAlert('danger', 'Erro de conexão. Tente novamente.');
    // Restaurar botão
    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
  });
}

// Deletar avaliação
function deleteReview() {
  if (!window.userReviewId) {
    showAlert('danger', 'Erro: dados da avaliação não encontrados.');
    return;
  }
  
  if (confirm('Tem certeza que deseja apagar sua avaliação?')) {
    fetch(`/deletar-avaliacao/${window.userReviewId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        showAlert('success', 'Avaliação apagada com sucesso!');
        setTimeout(() => {
          window.location.reload();
        }, 1500);
      } else {
        showAlert('danger', data.message || 'Erro ao apagar avaliação.');
      }
    })
    .catch(error => {
      console.error('Erro:', error);
      showAlert('danger', 'Erro de conexão. Tente novamente.');
    });
  }
}

// Função para mostrar alertas
function showAlert(type, message) {
  console.log(`Alert [${type}]:`, message);
  
  // Criar elemento de alerta
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
  alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;
  
  // Adicionar ao body
  document.body.appendChild(alertDiv);
  
  // Remover automaticamente após 5 segundos
  setTimeout(() => {
    if (alertDiv.parentNode) {
      alertDiv.parentNode.removeChild(alertDiv);
    }
  }, 5000);
  
  // Fallback para alert() se o elemento não aparecer
  setTimeout(() => {
    if (!document.body.contains(alertDiv)) {
      alert(`${type.toUpperCase()}: ${message}`);
    }
  }, 100);
}

// Função para mostrar preview das imagens selecionadas
function setupImagePreview() {
  // Função removida - preview desabilitado
  return;
}

// Inicializar sistema quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
  console.log('Review system initialized');
  
  // Configurar estrelas se existirem
  if (document.querySelectorAll('.star-btn').length > 0) {
    setupSimpleStars();
  }
}); 