import { getCollection, type CollectionEntry } from 'astro:content';

export const withBase = (path = '') =>
  `${import.meta.env.BASE_URL.replace(/\/?$/, '/')}${path.replace(/^\/+/, '')}`;

export const faqUrl = (faq: CollectionEntry<'faqs'>) => withBase(`faqs/${faq.id}/`);

export async function publishedFaqs() {
  return (await getCollection('faqs', ({ data }) => !data.draft))
    .sort((a, b) => b.data.published.valueOf() - a.data.published.valueOf());
}

export const readingMinutes = (body = '') => Math.max(1, Math.ceil(body.split(/\s+/).length / 200));

export const formatDate = (date: Date) => new Intl.DateTimeFormat('en-GB', {
  day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC',
}).format(date);
