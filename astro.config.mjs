import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { site, base } from './site.config.mjs';

export default defineConfig({
  site,
  base,
  output: 'static',
  trailingSlash: 'always',
  integrations: [sitemap()],
  markdown: { shikiConfig: { themes: { light: 'github-light', dark: 'github-dark' } } },
});
