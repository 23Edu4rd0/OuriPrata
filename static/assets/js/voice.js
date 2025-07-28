// ===== VOICE.JS - Funcionalidades de Voz =====

function showAlert(type, message) {
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} alert-dismissible fade show position-fixed`;
  alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9997; max-width: 300px;';
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;
  
  document.body.appendChild(alertDiv);
  
  setTimeout(() => {
    if (alertDiv.parentNode) {
      alertDiv.remove();
    }
  }, 5000);
}

function startVoiceSearch(version) {
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    showAlert('error', 'Busca por voz não é suportada neste navegador.');
    return;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  
  recognition.lang = 'pt-BR';
  recognition.continuous = false;
  recognition.interimResults = false;
  
  const input = version === 'mobile' ? document.getElementById('search-input-mobile') : document.getElementById('search-input');
  const voiceBtn = version === 'mobile' ? document.getElementById('voice-btn-mobile') : document.getElementById('voice-btn');
  
  if (!input) {
    showAlert('error', 'Campo de busca não encontrado.');
    return;
  }
  
  recognition.onstart = function() {
    isRecording = true;
    if (voiceBtn) {
      voiceBtn.innerHTML = '<i class="bi bi-mic-fill text-danger"></i>';
      voiceBtn.classList.add('recording');
    }
    showAlert('info', 'Fale agora...');
  };
  
  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    input.value = transcript;
    
    const inputEvent = new Event('input', { bubbles: true });
    input.dispatchEvent(inputEvent);
    
    showAlert('success', `Buscando por: "${transcript}"`);
  };
  
  recognition.onerror = function(event) {
    isRecording = false;
    if (voiceBtn) {
      voiceBtn.innerHTML = '<i class="bi bi-mic text-muted"></i>';
      voiceBtn.classList.remove('recording');
    }
    
    let errorMessage = 'Erro na busca por voz.';
    if (event.error === 'network') {
      errorMessage = 'Erro de rede. Verifique sua conexão e tente novamente.';
    } else if (event.error === 'not-allowed') {
      errorMessage = 'Permissão de microfone negada. Clique no ícone de microfone na barra de endereços e permita o acesso.';
    } else if (event.error === 'not-supported') {
      errorMessage = 'Busca por voz não é suportada neste navegador. Use Chrome ou Safari.';
    } else if (event.error === 'no-speech') {
      errorMessage = 'Nenhuma fala detectada. Tente falar mais alto ou mais próximo do microfone.';
    } else if (event.error === 'audio-capture') {
      errorMessage = 'Erro ao capturar áudio. Verifique se o microfone está funcionando.';
    } else {
      errorMessage = `Erro: ${event.error}. Tente novamente.`;
    }
    
    showAlert('error', errorMessage);
  };
  
  recognition.onend = function() {
    isRecording = false;
    if (voiceBtn) {
      voiceBtn.innerHTML = '<i class="bi bi-mic text-muted"></i>';
      voiceBtn.classList.remove('recording');
    }
  };
  
  try {
    recognition.start();
  } catch (error) {
    showAlert('error', 'Erro ao iniciar busca por voz.');
  }
}

function testVoiceSupportAndShowBtn() {
  const btn = document.getElementById('voice-btn');
  const btnMobile = document.getElementById('voice-btn-mobile');
  const hasSupport = ('webkitSpeechRecognition' in window) || ('SpeechRecognition' in window);
  
  if (!hasSupport) {
    if (btn) btn.style.display = 'none';
    if (btnMobile) btnMobile.style.display = 'none';
    return;
  }
  
  try {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    let tested = false;
    
    recognition.onstart = function() {
      tested = true;
      recognition.abort();
      if (btn) btn.style.display = '';
      if (btnMobile) btnMobile.style.display = '';
    };
    
    recognition.onerror = function(event) {
      if (btn) btn.style.display = 'none';
      if (btnMobile) btnMobile.style.display = 'none';
    };
    
    recognition.start();
    
    setTimeout(function() {
      if (!tested) {
        if (btn) btn.style.display = 'none';
        if (btnMobile) btnMobile.style.display = 'none';
      }
    }, 2000);
    
  } catch (e) {
    if (btn) btn.style.display = 'none';
    if (btnMobile) btnMobile.style.display = 'none';
  }
} 