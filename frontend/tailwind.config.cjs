/** @type {import('tailwindcss').Config}*/
const config = {
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		'./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'
	],

	darkMode: 'class',

	theme: {
		extend: {
			colors: {
				primary: 'var(--primary)',
				'primary-600': 'var(--primary)',
				background: 'var(--background)',
			}
		}
	},

	plugins: []
};

module.exports = config;
