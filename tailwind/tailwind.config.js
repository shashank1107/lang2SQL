/** @type {import('tailwindcss').Config} */
// For setup, refer https://stackoverflow.com/a/63392427
module.exports = {
    content: ["../templates/**/*.{html,js}"],
    theme: {
        container: {
            center: true,
            padding: {
                DEFAULT: '1rem',
                sm: '2rem',
                lg: '4rem',
            }
        },
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
    ],
}
