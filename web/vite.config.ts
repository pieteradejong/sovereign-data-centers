import { fileURLToPath, URL } from 'node:url'

import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Tailwind 4 is configured in CSS (@theme in src/styles/index.css), so there is no
// tailwind.config.ts and no postcss.config.js here.
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
  server: { port: 5173, host: true },
  preview: { port: 4173, host: true },
  build: {
    outDir: 'dist',
    // d3 is the only heavy dependency; splitting it keeps the entry chunk small.
    rollupOptions: {
      output: {
        manualChunks: {
          react: ['react', 'react-dom', 'react-router-dom'],
          d3: ['d3', 'topojson-client'],
        },
      },
    },
  },
})
