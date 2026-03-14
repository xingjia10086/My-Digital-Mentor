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
- Production URL is resolved automatically from `NEXT_PUBLIC_SITE_URL` or Vercel's `VERCEL_PROJECT_PRODUCTION_URL`.

## Deployment

This folder can be deployed as a standalone Next.js app to:

- Vercel
- Netlify
- Railway
- a VPS with `next start`

## Vercel

1. Import this GitHub repository in Vercel.
2. Set the Root Directory to `site`.
3. Build command: `npm run build`
4. Output setting: Next.js default
5. Optional custom environment variable:

```text
NEXT_PUBLIC_SITE_URL=https://your-domain.com
```

If you do not set `NEXT_PUBLIC_SITE_URL`, the app will use Vercel's production domain automatically.
