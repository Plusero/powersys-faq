import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { resolve, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { site, base } from '../site.config.mjs';

const root = fileURLToPath(new URL('../dist/', import.meta.url));
async function collect(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = await Promise.all(entries.map(entry => entry.isDirectory()
    ? collect(resolve(directory, entry.name))
    : [relative(root, resolve(directory, entry.name)).split(sep).join('/')]));
  return files.flat();
}

const files = new Set(await collect(root));
for (const required of ['index.html', 'faqs/index.html', 'about/index.html', '404.html', 'rss.xml', 'robots.txt', 'sitemap-index.xml', 'favicon.svg', '.nojekyll']) {
  assert(files.has(required), `Missing build artifact: ${required}`);
}
const html = new Map(await Promise.all([...files].filter(file => file.endsWith('.html'))
  .map(async file => [file, await readFile(resolve(root, file), 'utf8')])));
const decode = value => value.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'");
const ids = new Map([...html].map(([file, text]) => [file, new Set([...text.matchAll(/\bid="([^"]+)"/g)].map(match => decode(match[1])))]));

function artifactFor(url) {
  assert(url.pathname.startsWith(base), `URL omits the configured base path ${base}: ${url}`);
  const path = decodeURIComponent(url.pathname.slice(base.length));
  return files.has(path) ? path : `${path.replace(/\/?$/, '/')}index.html`.replace(/^\//, '');
}
function checkLocalUrl(value, pageUrl, source) {
  if (!value || /^(mailto:|tel:|data:|javascript:)/i.test(value)) return;
  const url = new URL(decode(value), pageUrl);
  if (url.origin !== site) return;
  const artifact = artifactFor(url);
  assert(files.has(artifact), `${source} links to missing artifact: ${url}`);
  if (url.hash && html.has(artifact)) {
    assert(ids.get(artifact).has(decodeURIComponent(url.hash.slice(1))), `${source} links to missing heading: ${url}`);
  }
}

let linksChecked = 0;
for (const [file, text] of html) {
  assert(/<html\s+lang="en"/.test(text), `${file} has no document language`);
  assert(/<title>.+?<\/title>/.test(text), `${file} has no title`);
  assert(/<meta\s+name="description"\s+content="[^"]+"/.test(text), `${file} has no description`);
  assert(/<main\s+id="main"/.test(text), `${file} has no skip-link destination`);
  const pagePath = file === 'index.html' ? '' : file.replace(/index\.html$/, '');
  const pageUrl = new URL(`${base}${pagePath}`, site);
  if (file !== '404.html') {
    const canonical = text.match(/<link\s+rel="canonical"\s+href="([^"]+)"/);
    assert.equal(canonical?.[1], pageUrl.href, `${file} has an incorrect canonical URL`);
  }
  for (const tag of text.matchAll(/<(?:a|link|script|img)\b[^>]*>/g)) {
    for (const attribute of tag[0].matchAll(/\b(?:href|src)="([^"]+)"/g)) {
      checkLocalUrl(attribute[1], pageUrl, file);
      linksChecked++;
    }
  }
}

const articleFiles = [...html.keys()].filter(file => /^faqs\/.+\/index\.html$/.test(file));
const rss = await readFile(resolve(root, 'rss.xml'), 'utf8');
assert.equal((rss.match(/<item>/g) || []).length, articleFiles.length, 'RSS item count differs from article count');
for (const match of rss.matchAll(/<link>([^<]+)<\/link>/g)) checkLocalUrl(match[1], new URL(base, site), 'rss.xml');
assert(rss.includes(`${site}${base}`), 'RSS omits the deployment base path');
const sitemapIndex = await readFile(resolve(root, 'sitemap-index.xml'), 'utf8');
const sitemapUrls = [...sitemapIndex.matchAll(/<loc>([^<]+)<\/loc>/g)];
assert(sitemapUrls.length > 0, 'Sitemap index is empty');
const indexedPages = new Set();
for (const match of sitemapUrls) {
  const sitemapUrl = new URL(decode(match[1]));
  checkLocalUrl(sitemapUrl.href, new URL(base, site), 'sitemap-index.xml');
  const sitemap = await readFile(resolve(root, artifactFor(sitemapUrl)), 'utf8');
  for (const page of sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)) {
    checkLocalUrl(page[1], new URL(base, site), 'sitemap');
    indexedPages.add(artifactFor(new URL(decode(page[1]))));
  }
}
for (const article of articleFiles) assert(indexedPages.has(article), `Article missing from sitemap: ${article}`);
const robots = await readFile(resolve(root, 'robots.txt'), 'utf8');
assert(robots.includes(`Sitemap: ${site}${base}sitemap-index.xml`), 'robots.txt points to the wrong sitemap');

console.log(`Validated ${html.size} pages, ${articleFiles.length} FAQ articles, ${linksChecked} links/assets, RSS, and sitemap at ${site}${base}`);
