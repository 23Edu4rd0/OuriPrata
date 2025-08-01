// Modal de Imagem - JavaScript

function showImageFullscreen(imageUrl, username) {
  // Criar um overlay simples
  const overlay = document.createElement('div');
  overlay.className = 'image-modal-overlay';
  
  // Criar a imagem
  const img = document.createElement('img');
  img.src = imageUrl;
  img.className = 'image-modal-img';
  
  // Adicionar título
  const title = document.createElement('div');
  title.className = 'image-modal-title';
  title.textContent = `Imagem de ${username}`;
  
  // Adicionar botão de fechar
  const closeBtn = document.createElement('div');
  closeBtn.className = 'image-modal-close';
  closeBtn.innerHTML = '×';
  
  // Adicionar instrução de zoom
  const zoomHint = document.createElement('div');
  zoomHint.className = 'image-modal-hint';
  zoomHint.innerHTML = '🔍 Clique na imagem para dar zoom';
  
  // Variável para controlar zoom
  let isZoomed = false;
  
  // Função de zoom
  function toggleZoom() {
    if (isZoomed) {
      img.classList.remove('zoomed');
      overlay.classList.remove('zoomed');
      isZoomed = false;
    } else {
      img.classList.add('zoomed');
      overlay.classList.add('zoomed');
      isZoomed = true;
    }
  }
  
  // Adicionar elementos ao overlay
  overlay.appendChild(img);
  overlay.appendChild(title);
  overlay.appendChild(closeBtn);
  overlay.appendChild(zoomHint);
  
  // Adicionar ao body
  document.body.appendChild(overlay);
  
  // Eventos de clique
  img.onclick = function(e) {
    e.stopPropagation();
    toggleZoom();
  };
  
  // Fechar ao clicar fora
  overlay.onclick = function(e) {
    if (e.target === overlay) {
      document.body.removeChild(overlay);
    }
  };
  
  // Fechar ao clicar no X
  closeBtn.onclick = function(e) {
    e.stopPropagation();
    document.body.removeChild(overlay);
  };
} 