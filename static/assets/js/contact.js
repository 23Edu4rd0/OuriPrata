document.getElementById('contactForm').addEventListener('submit', e => {
  e.preventDefault();

  const nome = document.getElementById('nome').value.trim();
  const email = document.getElementById('email').value.trim();
  const mensagem = document.getElementById('mensagem').value.trim();

  let msg = 'Olá! Entrei em contato pelo site da OuriPrata.\n\n';
  msg += `*Nome:* ${nome}\n`;
  msg += `*E-mail:* ${email}\n`;
  msg += `\n*Mensagem:*\n${mensagem}`;

  // noopener impede que a aba aberta acesse window.opener e consiga
  // redirecionar esta página (reverse tabnabbing).
  window.open(
    `https://wa.me/5537998623061?text=${encodeURIComponent(msg)}`,
    '_blank',
    'noopener,noreferrer'
  );
});
