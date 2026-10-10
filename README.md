# Power Systems FAQ

[Visit the Power Systems FAQ website](https://plusero.github.io/powersys-faq/)

A growing collection of clear, source-backed answers to frequently asked questions in power systems. Articles are written in Markdown and published as a static [Astro](https://astro.build/) website on GitHub Pages.

The first FAQ explains how probabilistic wind and solar forecasts support decisions, using [Dexter Energy's article](https://dexterenergy.ai/news/probabilistic-wind-and-solar-power-forecasting/) as a practical example.

## Run locally

Use Node.js 22.12 or newer in the Node.js 22 release line and npm. GitHub Actions uses Node.js 22.

```sh
npm ci
npm run dev
```

Open the address printed by Astro. With the default repository configuration, the site is served under `/powersys-faq/`, including during local development.

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start the development server with live updates. |
| `npm run check` | Check Astro components, TypeScript, and content types. |
| `npm run build` | Generate the static website in `dist/`. |
| `npm run validate` | Validate generated pages, links, and publication artifacts; run after a build. |
| `npm run preview` | Serve the last production build locally. |

Before publishing a change:

```sh
npm run check
npm run build
npm run validate
npm run preview
```

Commit `package-lock.json` whenever dependencies change so local and automated builds use the same dependency versions.

## Write a FAQ

1. Copy [the article template](docs/faq-template.md) to `src/content/faqs/your-question.md`.
2. Replace its frontmatter and answer with your article. Use a filename with lowercase words separated by hyphens; it becomes the article's URL slug.
3. Cite original sources with Markdown links. Use `##` for the first section heading; the site renders the article title for you.
4. Set `draft: false` when ready, run the checks above, and commit the article.

Published articles automatically appear in the FAQ archive, topic filters, search index, RSS feed, and sitemap. Set `featured: true` to highlight an article on the homepage. Drafts are excluded from published pages and feeds, including local development.

Frontmatter fields:

| Field | Meaning |
| --- | --- |
| `title` | The FAQ question and article title. |
| `description` | A short summary for article cards and search results, up to 200 characters. |
| `published` | Publication date in `YYYY-MM-DD` format. |
| `updated` | Optional revision date in `YYYY-MM-DD` format. |
| `topic` | The article's topic, such as `Forecasting`. Reuse existing names for consistent filters. |
| `takeaway` | A concise answer displayed at the start of the article. |
| `tags` | An optional list of search keywords. |
| `featured` | Optional homepage highlighting; defaults to `false`. |
| `draft` | Optional publication switch; defaults to `false`. Start new work with `true`. |

Use `public/` for assets that should be copied directly to the website. When linking an asset from an article, include the site's configured base path, for example `/powersys-faq/images/my-diagram.svg`. Check the rendered article with the production preview before publishing.

## Edit the market diagrams

The Dutch electricity market figures have a maintained [Python source](scripts/generate-market-diagrams.py). Edit the labels, colours, and layout there, then regenerate the SVGs with:

```sh
python3 scripts/generate-market-diagrams.py
python3 scripts/generate-market-diagrams.py --check
```

Python 3.9+ is needed only for diagram editing; no additional packages are required. Keep both the source and generated SVGs in version control. See [the diagram editing guide](docs/market-diagrams.md) for output paths and visual checks.

## Deploy to GitHub Pages

The repository is configured for **https://plusero.github.io/powersys-faq/**. This is the expected deployment URL; it becomes available after GitHub Pages is enabled and the deployment succeeds.

1. In [this repository's Pages settings](https://github.com/Plusero/powersys-faq/settings/pages), select **Build and deployment → Source → GitHub Actions**. This follows [GitHub's publishing instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
2. Commit the website files and push to `main`.
3. Open the repository's **Actions** tab and check the **Deploy to GitHub Pages** workflow. Its deployment job links to the published website.

For an initial setup, after reviewing the working tree:

```sh
git add README.md docs .github .gitignore .nvmrc package.json package-lock.json astro.config.mjs site.config.mjs tsconfig.json src public scripts
git commit -m "Build Power Systems FAQ website"
git push origin main
```

Each push to `main` installs dependencies with `npm ci`, checks the project, builds and validates `dist/`, then publishes it through the official GitHub Pages artifact workflow. Pull requests run the same checks without deploying. You can also select **Actions → Deploy to GitHub Pages → Run workflow**, choosing `main`. Deployment is limited to `main`, and active deployments are allowed to finish before the next starts.

The workflow uses the repository's built-in `GITHUB_TOKEN`; no personal access token or deployment secret is required. See [GitHub's custom Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) for the underlying deployment mechanism.

## Change the deployment URL

The shared `site.config.mjs` settings default to `site: https://plusero.github.io` and `base: /powersys-faq/`. The site origin and base path control internal links, assets, canonical URLs, RSS, and sitemap URLs.

For a renamed repository, a different GitHub account, or a custom domain, set the following repository **Actions variables** under **Settings → Secrets and variables → Actions → Variables**. Both workflows pass these values to the build; the defaults apply when variables are absent.

| Deployment | `SITE_URL` | `SITE_BASE_PATH` |
| --- | --- | --- |
| This repository | `https://plusero.github.io` | `/powersys-faq/` |
| Another project repository | `https://your-account.github.io` | `/your-repository/` |
| User site or custom domain | `https://your-domain.example` | `/` |

Use an absolute HTTPS origin for `SITE_URL`, and a path with leading and trailing slashes for `SITE_BASE_PATH`. For a custom domain, also configure the domain and DNS through [GitHub Pages settings](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site); build variables alone do not configure hosting or DNS.

To test an alternate URL locally, pass the same values to the build and validation commands:

```sh
SITE_URL=https://your-domain.example SITE_BASE_PATH=/ npm run build
SITE_URL=https://your-domain.example SITE_BASE_PATH=/ npm run validate
SITE_URL=https://your-domain.example SITE_BASE_PATH=/ npm run preview
```

You can update the defaults in `site.config.mjs` if the change should also apply to local development. Review any absolute Markdown asset links when changing the base path.

## Project map

```text
src/content/faqs/          Markdown FAQ articles
src/assets/diagrams/       Generated SVG article figures
src/content.config.ts     Article frontmatter schema
src/pages/                Homepage, FAQ archive, articles, and feeds
src/components/           Shared interface components
src/layouts/              Page and article layouts
src/styles/               Website styles
public/                   Static assets
scripts/validate-build.mjs Generated-site checks
.github/workflows/         Pull request checks and Pages deployment
docs/faq-template.md       Starting point for a new article
```
