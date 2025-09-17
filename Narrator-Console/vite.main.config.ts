import { defineConfig } from 'vite';
import { resolve } from 'path';

// https://vitejs.dev/config
export default defineConfig({
  resolve: {
    // Some libs that can run in both Web and Node.js, such as `axios`, we need to tell Vite to build them in Node.js.
    browserField: false,
    conditions: ['node'],
    mainFields: ['module', 'jsnext:main', 'jsnext'],
  },
  build: {
    ssr: true,
    sourcemap: true,
    outDir: 'dist-main',
    rollupOptions: {
      external: [
        'electron',
        ...Object.keys(require('./package.json').dependencies || {}),
      ],
      input: {
        index: resolve(__dirname, 'src/main.ts'),
      },
      output: {
        format: 'cjs',
        entryFileNames: '[name].js',
      },
    },
  },
});