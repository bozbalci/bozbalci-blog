import { defineConfig } from "vite";
import { resolve } from "path";
import { readdirSync, statSync } from "fs";
import tailwindcss from "@tailwindcss/vite";
import vue from "@vitejs/plugin-vue";

const getEntryPoints = (baseDir) => {
  const appsDir = resolve(__dirname, baseDir);
  return readdirSync(appsDir)
    .filter((dir) => statSync(resolve(appsDir, dir)).isDirectory())
    .map((dir) => resolve(baseDir, dir, "app.js"))
    .filter((file) => statSync(file, { throwIfNoEntry: false })?.isFile());
};

export default defineConfig({
  plugins: [tailwindcss(), vue()],
  base: "/static",
  build: {
    manifest: "manifest.json",
    outDir: resolve("./static/dist"),
    rollupOptions: {
      input: ["static/css/main.css", ...getEntryPoints("static/js")],
      output: {
        entryFileNames: "[hash].js",
        assetFileNames: "[hash].[ext]",
      },
    },
  },
  resolve: {
    alias: {
      "@": resolve(__dirname, "static/js"),
      vue: "vue/dist/vue.esm-bundler",
    },
  },
});
