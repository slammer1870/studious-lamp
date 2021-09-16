module.exports = {
  mode: 'jit',
  purge: ['../templates/**/*.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
      'sans': ['Montserrat','Helvetica', 'Arial', 'sans-serif'],
     }},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
