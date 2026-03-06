import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // 允许局域网访问
    port: 5173,
    open: false,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // 后端地址
        changeOrigin: true,
      }
    }
  }
})
