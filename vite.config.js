import {defineConfig} from 'vite';
import {resolve} from 'path';
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [
      tailwindcss()
  ],
  base: "/static",
  build: {
    manifest: "manifest.json",
    outDir: resolve("./static/dist"),
    rollupOptions: {
      input: [
        "static/styles/main.css",
        "static/scripts/lightbox-single.js",
        "static/scripts/lightbox-multi.js",
        "static/scripts/theme-toggle.js"
      ],
      output: {
        entryFileNames: "[hash].js",
        assetFileNames: "[hash].[ext]",
      }
    },
  },
})
