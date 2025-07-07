/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./catalogo/templates/**/*.html",
    "./catalogo/static/**/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        'montserrat': ['Montserrat', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
