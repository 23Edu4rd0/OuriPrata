/**
 * Escapa texto antes de interpolar em HTML.
 *
 * Nome de peça, URL de imagem e termo de busca chegam do banco, do
 * localStorage ou da própria barra de busca — nada disso é confiável.
 * Sem escapar, um nome como <img src=x onerror=...> vira código executado
 * na página (XSS).
 *
 * Aspas simples e duplas também são escapadas para que o resultado possa ser
 * usado dentro de atributos, não só entre tags.
 */
window.escapeHtml = function (valor) {
  if (valor === null || valor === undefined) return '';
  return String(valor)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
};
