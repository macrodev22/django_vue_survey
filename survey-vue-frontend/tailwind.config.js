/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js}"],
  purge: ['./index.html', './src/**/*.{vue,js,jsx,tsx}'],
  theme: {
    extend: {
      keyframes: {
        'fade-in-down': {
          'from': {
            transform: 'translateY(-0.75rem) translateX(-50%)',
            opacity: '0'
          },
          'to' : {
            transform: 'translateY(0rem) translateX(-50%)',
            opacity: '1'
          }
        },
        'pop': {
          'from': {
            opacity: '0',
            transform: 'scale(0.5, 0.5)'
          },
          'to': {
            opacity: '1',
            transform: 'scale(1, 1)',
          }
        }
      },
      animation: {
        'fade-in-down': 'fade-in-down 0.2s ease-in-out both',
        'pop': 'pop 0.2s cubic-bezier(0.26, 0.53, 0.74, 1.48) both',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

