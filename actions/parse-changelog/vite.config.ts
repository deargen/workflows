import commonjs from "@rollup/plugin-commonjs"
import { nodeResolve } from "@rollup/plugin-node-resolve"
import { defineConfig } from "vite"

export default defineConfig({
  build: {
    // where to put the output
    outDir: "dist",
    // wipe dist on each build
    emptyOutDir: true,
    // build as a “library” with a single entry
    lib: {
      entry: "src/index.ts", // your single TS file
      formats: ["cjs"], // output as CommonJS; use ["es"] for ES modules
      fileName: () => "index.js", // always call it index.js
    },
    // tweak the target if you need a lower ES version
    target: "node20",
    minify: false,
    sourcemap: true,
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
      plugins: [
        // 3) resolve node_modules
        nodeResolve({ preferBuiltins: true }),
        // 4) convert CJS deps → ES so they bundle
        commonjs(),
      ],
    },
  },
})
