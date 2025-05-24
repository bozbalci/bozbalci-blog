import { defineConfig } from 'vite';
import { resolve } from 'path';
import { readdirSync, statSync } from 'fs';
import tailwindcss from '@tailwindcss/vite';
import vue from '@vitejs/plugin-vue';

const getEntryPoints = (baseDir) => {
  const appsDir = resolve(__dirname, baseDir);
  return readdirSync(appsDir)
    .filter((dir) => statSync(resolve(appsDir, dir)).isDirectory())
    .map((dir) => resolve(baseDir, dir, 'app.js'))
    .filter((file) => statSync(file, { throwIfNoEntry: false })?.isFile());
};

export default defineConfig({
  server: {
    host: true,
    port: 5173,
  },
  plugins: [tailwindcss(), vue()],
  base: '/static',
  build: {
    manifest: 'manifest.json',
    outDir: resolve('./notcms/static/dist'),
    rollupOptions: {
      input: [
        'notcms/static/css/main.css',
        ...getEntryPoints('notcms/static/js'),
      ],
      output: {
        entryFileNames: '[hash].js',
        assetFileNames: '[hash].[ext]',
      },
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'notcms/static/js'),
      vue: 'vue/dist/vue.esm-bundler',
    },
  },
});
