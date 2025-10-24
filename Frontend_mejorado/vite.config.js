
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue(), 

  ],
  define: {
    __VUE_PROD_DEVTOOLS__: false, 
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false 



  }, 
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
  server: {
    host: true,
    allowedHosts: ['localhost', '127.0.0.1', 'abriluniformes.shop'],
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
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
