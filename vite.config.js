import { defineConfig } from "vite";
import { resolve } from "path";
import tailwindcss from "@tailwindcss/vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [tailwindcss(), vue()],
  base: "/static",
  build: {
    manifest: "manifest.json",
    outDir: resolve("./static/dist"),
    rollupOptions: {
      input: [
        "static/styles/main.css",
        "static/scripts/lightbox-single.js",
        "static/scripts/lightbox-multi.js",
        "static/scripts/theme-toggle.js",
        "static/scripts/apps/barbell/app.js",
      ],
      output: {
        entryFileNames: "[hash].js",
        assetFileNames: "[hash].[ext]",
      },
    },
  },
  resolve: {
    alias: {
      "@": resolve(__dirname, "static/scripts"),
      vue: "vue/dist/vue.esm-bundler",
    },
  },
});
