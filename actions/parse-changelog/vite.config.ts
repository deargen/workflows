import { defineConfig } from "vite"
import { VitePluginNode } from "vite-plugin-node"

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
    target: "es2020",
    // if you have dependencies you don’t want to bundle, list them here:
    rollupOptions: {
      external: [
        /* e.g. "electron", "fs", "path", ... */
      ],
    },
  },
  plugins: [
    ...VitePluginNode({
      // Nodejs native Request adapter
      // currently this plugin support 'express', 'nest', 'koa' and 'fastify' out of box,
      // you can also pass a function if you are using other frameworks, see Custom Adapter section
      adapter: "express",

      // tell the plugin where is your project entry
      appPath: "./src/index.ts",

      // Optional, default: 'viteNodeApp'
      // the name of named export of you app from the appPath file
      exportName: "viteNodeApp",

      // Optional, default: false
      // if you want to init your app on boot, set this to true
      initAppOnBoot: false,

      // Optional, default: 'esbuild'
      // The TypeScript compiler you want to use
      // by default this plugin is using vite default ts compiler which is esbuild
      // 'swc' compiler is supported to use as well for frameworks
      // like Nestjs (esbuild dont support 'emitDecoratorMetadata' yet)
      // you need to INSTALL `@swc/core` as dev dependency if you want to use swc
      tsCompiler: "esbuild",

      // Optional, default: {
      // jsc: {
      //   target: 'es2019',
      //   parser: {
      //     syntax: 'typescript',
      //     decorators: true
      //   },
      //  transform: {
      //     legacyDecorator: true,
      //     decoratorMetadata: true
      //   }
      // }
      // }
      // swc configs, see [swc doc](https://swc.rs/docs/configuration/swcrc)
      swcOptions: {},
    }),
  ],
})
