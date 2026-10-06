import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { publishedFaqs, faqUrl, withBase } from '../lib/content';

export async function GET(context: APIContext) {
  const faqs = await publishedFaqs();
  return rss({
    title: 'Power Systems FAQ',
    description: 'Practical answers to frequently asked questions in power systems.',
    site: new URL(withBase(), context.site!),
    items: faqs.map(faq => ({ title: faq.data.title, description: faq.data.description, pubDate: faq.data.published, link: faqUrl(faq) })),
    customData: '<language>en</language>',
  });
}
