import { defineConfig } from 'astro/config';
import { BASE, TERM_ROOT, DOC_ROOT } from './src/lib/paths.mjs';
import remarkTermLinks from './src/lib/remark-term-links.mjs';

export default defineConfig({
  site: 'https://texxxxture.github.io',
  base: BASE,
  trailingSlash: 'ignore',

  markdown: {
    remarkPlugins: [
      [remarkTermLinks, { termRoot: TERM_ROOT, docRoot: DOC_ROOT, base: BASE }],
    ],
    shikiConfig: {
      themes: { light: 'github-light', dark: 'github-dark' },
      defaultColor: 'light',
      wrap: false,
    },
  },

  build: {
    format: 'directory',
    inlineStylesheets: 'auto',
  },
});
