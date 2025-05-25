/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      // Todas tus vistas HTML de Flask
      "./app/templates/**/*.html",
      // Si tienes JavaScript que usa clases de Tailwind
      "./app/static/js/**/*.js"
    ],
    theme: {
      extend: {
        
      },
    },
    plugins: [
      // Añade plugins de Tailwind si los necesitas
    ],
  }
  