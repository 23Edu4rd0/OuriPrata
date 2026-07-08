module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            colors: {
                cream: { 50: '#fdfaf5', 100: '#f7f2ea', 200: '#f0e8db', 300: '#e8dcc8' },
                gold: { 50: '#fdf9ee', 100: '#f8efce', 200: '#f0d98e', 300: '#e8c65a', 400: '#d4a843', 500: '#b8922e', 600: '#9a7821' },
                ink: { DEFAULT: '#241a13', muted: '#6f6259', light: '#8a7d74' },
            },
            fontFamily: {
                serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
                sans:  ['Inter', 'system-ui', 'sans-serif'],
            },
            boxShadow: {
                soft: '0 18px 50px rgba(36, 26, 19, 0.08)',
                card: '0 10px 30px rgba(36, 26, 19, 0.06)',
            },
            animation: {
                'fade-up': 'fadeUp 0.6s ease both',
            },
            keyframes: {
                fadeUp: {
                    '0%': { opacity: '0', transform: 'translateY(16px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('daisyui'),
    ],
}