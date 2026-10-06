import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    server: {
        port: 3000,
        proxy: {
            '/api': {
                // По умолчанию — локальный бэкенд; для проверки на тестовой базе: VITE_API_TARGET=http://localhost:8001
                target: process.env.VITE_API_TARGET || 'http://localhost:8000',
                changeOrigin: true,
            },
        },
    },
});