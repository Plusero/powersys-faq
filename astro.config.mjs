import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { site, base } from './site.config.mjs';

export default defineConfig({
  site,
  base,
  output: 'static',
  trailingSlash: 'always',
  integrations: [sitemap()],
  markdown: { shikiConfig: { theme: 'github-light' } },
});
