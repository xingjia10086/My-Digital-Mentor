import { getSiteUrl } from "../lib/site-url";

export default function sitemap() {
  const base = getSiteUrl();

  return [
    {
      url: `${base}/en`,
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 0.9
    },
    {
      url: `${base}/zh`,
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 0.9
    }
  ];
}
