import { defineConfig } from 'vite';
import { resolve } from 'path';

// https://vitejs.dev/config
export default defineConfig({
  resolve: {
    browserField: false,
    conditions: ['node'],
    mainFields: ['module', 'jsnext:main', 'jsnext'],
  },
  build: {
    ssr: true,
    sourcemap: true,
    outDir: 'dist-preload',
    rollupOptions: {
      external: [
        'electron',
      ],
      input: {
        index: resolve(__dirname, 'src/preload.ts'),
      },
      output: {
        format: 'cjs',
        entryFileNames: '[name].js',
      },
    },
  },
});