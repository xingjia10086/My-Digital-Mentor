import { getSiteUrl } from "../lib/site-url";

export default function robots() {
  return {
    rules: {
      userAgent: "*",
      allow: "/"
    },
    sitemap: [`${getSiteUrl()}/sitemap.xml`, "https://mengmusanqian.com.cn/sitemap.xml"]
  };
}
