/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ['./templates/**/*.{html,js}'],
  theme: {
    extend: {
      width: {
        '5/6': '83.333333%',
      },
    },
  },
}