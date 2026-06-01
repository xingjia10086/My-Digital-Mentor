import { getSiteUrl } from "../lib/site-url";
import mmsqSummary from "../public/ai-summary.json";

const MMSQ_BASE = "https://mengmusanqian.com.cn";
const MMSQ_BASE_ROUTES = ["/knowledge/", "/manuals/", "/qa/", "/cases/", "/about/"];

function uniqueRoutes(routes) {
  return Array.from(new Set(routes));
}

export default function sitemap() {
  const base = getSiteUrl();
  const now = new Date();
  const mmsqRoutes = uniqueRoutes([
    ...MMSQ_BASE_ROUTES,
    ...mmsqSummary.services.map((service) => `/services/${service.slug}/`),
    ...mmsqSummary.manualLibrary.map((manual) => new URL(manual.url).pathname),
    ...mmsqSummary.contentLibrary.map((article) => new URL(article.url).pathname)
  ]);

  return [
    {
      url: `${base}/en`,
      lastModified: now,
      changeFrequency: "weekly",
      priority: 0.9
    },
    {
      url: `${base}/zh`,
      lastModified: now,
      changeFrequency: "weekly",
      priority: 0.9
    },
    ...mmsqRoutes.map((route) => ({
      url: `${MMSQ_BASE}${route}`,
      lastModified: now,
      changeFrequency: "weekly",
      priority: route === "/qa/" ? 0.9 : 0.8
    }))
  ];
}
