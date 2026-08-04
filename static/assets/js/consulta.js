document.getElementById('consultaForm').addEventListener('submit', e => {
  e.preventDefault();
  const nome    = document.getElementById('c-nome').value.trim();
  const tipo    = document.getElementById('c-tipo').value;
  const metal   = document.getElementById('c-metal').value;
  const ocasiao = document.getElementById('c-ocasiao').value;
  const orc     = document.getElementById('c-orcamento').value.trim();
  const desc    = document.getElementById('c-descricao').value.trim();

  let msg = `Olá! Gostaria de uma consulta personalizada.\n\n`;
  msg += `*Nome:* ${nome}\n`;
  if (tipo)    msg += `*Tipo de joia:* ${tipo}\n`;
  if (metal)   msg += `*Metal:* ${metal}\n`;
  if (ocasiao) msg += `*Ocasião:* ${ocasiao}\n`;
  if (orc)     msg += `*Orçamento:* ${orc}\n`;
  msg += `\n*Descrição:*\n${desc}`;

  // noopener: ver comentário em contact_us.html (reverse tabnabbing).
  window.open(
    `https://wa.me/5537998623061?text=${encodeURIComponent(msg)}`,
    '_blank',
    'noopener,noreferrer'
  );
});
