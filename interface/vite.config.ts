import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    build: {
        target: 'esnext',
        outDir: '../api/static',
        emptyOutDir: true
    },
    server: {
        watch: {
            usePolling: true
        },
        port: 9001,
        host: true
    },
    css: {
        preprocessorOptions: {
            less: {
                math: 'parens-division'
            },
            scss: {
                api: 'modern-compiler'
            }
        }
    }
})
