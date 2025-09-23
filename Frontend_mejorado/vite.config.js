
// vite.config.js
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
  server: {
    host: true,
    allowedHosts: ['localhost', '127.0.0.1', 'abriluniformes.shop'],
    proxy: {
      '/api': {
        target: 'http://backend:8000',   // 👈 servicio del backend en docker
        changeOrigin: true,
        secure: false,
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
            // 🔑 truco: quita el Origin para que Django no haga el "origin check"
            proxyReq.removeHeader('origin')
          })
        },
      },
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
  },
})
