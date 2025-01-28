import { defineConfig } from 'cypress'

const isLocal = process.env.NODE_ENV === 'development'; // Use `NODE_ENV` to toggle
const localUrl = 'http://localhost:4173';
const renderUrl = 'https://energie-systems-planning-v2.onrender.com/';

export default defineConfig({
  e2e: {
    specPattern: 'cypress/e2e/**/*.{cy,spec}.{js,jsx,ts,tsx}',
    baseUrl: isLocal ? localUrl : renderUrl,
  },
  component: {
    specPattern: 'src/**/__tests__/*.{cy,spec}.{js,ts,jsx,tsx}',
    devServer: {
      framework: 'vue',
      bundler: 'vite',
    },
  },
})
