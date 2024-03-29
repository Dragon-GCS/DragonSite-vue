import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import ElementPlus from 'unplugin-element-plus/vite'
import UnoCSS from 'unocss/vite'
import UnocssIcons from '@unocss/preset-icons'

const pathSrc = resolve(__dirname, 'src')

// https://vitejs.dev/config/
export default defineConfig({
  base: "/",
  resolve: {
    alias: {'@': pathSrc},
  },
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
      imports: ['vue', 'vue-router'],
      dts: resolve(pathSrc, 'auto-imports.d.ts'),
    }),
    Components({
      resolvers: [ElementPlusResolver()],
      dts: resolve(pathSrc, 'components.d.ts'),
    }),
    ElementPlus({}),
    UnoCSS({
      presets: [
        UnocssIcons({
          // options
          prefix: 'i-',
          extraProperties: {
            display: 'inline-block'
          }
        }),
      ],
    }),
  ],
  server: {
    host:'localhost',
    port: 3333,
    proxy: {
      '/api': {target:'http://localhost:8080/', changeOrigin: true},
    }
  },
  build: {
    outDir: "../dist",
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return id.toString().split("node_modules/")[1].split("/")[0].toString()
          }
        }
      }
  }}
})
