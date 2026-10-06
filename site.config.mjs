// Override these values for another repository or a custom domain.
const url = new URL(process.env.SITE_URL || 'https://plusero.github.io');
if (!['http:', 'https:'].includes(url.protocol) || url.pathname !== '/') {
  throw new Error('SITE_URL must be an HTTP(S) origin, e.g. https://plusero.github.io');
}
const configuredBase = process.env.SITE_BASE_PATH ?? '/powersys-faq/';
const trimmedBase = configuredBase.replace(/^\/+|\/+$/g, '');
export const site = url.origin;
export const base = trimmedBase ? `/${trimmedBase}/` : '/';
