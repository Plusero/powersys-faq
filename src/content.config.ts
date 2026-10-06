import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const faqs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/faqs' }),
  schema: z.object({
    title: z.string().min(1),
    description: z.string().min(1).max(200),
    published: z.coerce.date(),
    updated: z.coerce.date().optional(),
    topic: z.string().min(1),
    tags: z.array(z.string().min(1)).default([]),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
    takeaway: z.string().min(1),
  }),
});

export const collections = { faqs };
