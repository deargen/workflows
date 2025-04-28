import { defineConfig } from "vite"

export default defineConfig({
  build: {
    // where to put the output
    outDir: "dist",
    // wipe dist on each build
    emptyOutDir: true,
    // tweak the target if you need a lower ES version
    target: "node16",
    minify: false,
    sourcemap: false,

    ssr: "src/index.ts",

    // if you have dependencies you don’t want to bundle, list them here:
    rollupOptions: {
      input: "src/index.ts",
      output: {
        format: "cjs",
        entryFileNames: "index.js",
      },
      external: [
        // tell Rollup *not* to bundle built-in modules
        ...require("node:module").builtinModules,
        // + electron if you’re calling Electron APIs directly:
        // "electron"
      ],
    },
  },

  ssr: {
    noExternal: true,
  },
})
