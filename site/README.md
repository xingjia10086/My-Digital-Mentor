# Site

This is a standalone Next.js landing site for the `Personal AI Writer` product direction inside My Digital Mentor.

## Routes

- `/en`
- `/zh`

The root route redirects to `/en`.

## Run locally

```bash
cd site
npm install
npm run dev
```

Then open:

```text
http://localhost:3000/en
http://localhost:3000/zh
```

## Notes

- The landing pages now serve their main screenshots from `site/public/images/`.
- Open Graph image generation is included via `app/opengraph-image.js`.
- `robots` and `sitemap` are included for production deployment.
- Replace the placeholder production domain in metadata, `robots`, and `sitemap` if you deploy on a custom URL.

## Deployment

This folder can be deployed as a standalone Next.js app to:

- Vercel
- Netlify
- Railway
- a VPS with `next start`
