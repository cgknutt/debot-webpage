import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Determine if we're running in Lando
const isLando = process.env.LANDO === 'ON'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    host: true, // Listen on all addresses
    strictPort: true, // Don't try other ports if 5173 is taken
    hmr: {
      host: 'localhost',
      clientPort: 5173
    },
    proxy: {
      '/api': {
        // If running in Lando, use the backend service name
        // Otherwise, use the direct Uvicorn URL
        target: isLando 
          ? process.env.VITE_API_URL || 'http://backend:8000'
          : 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
        configure: (proxy) => {
          proxy.on('proxyRes', function(proxyRes, req, res) {
            if (proxyRes.headers.location) {
              // Strip the host portion to make relative redirects
              proxyRes.headers.location = new URL(proxyRes.headers.location).pathname;
            }
          });
        },
        // Automatically detects environment and uses appropriate backend URL
      }
    }
  }
}) 