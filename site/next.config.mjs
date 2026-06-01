/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return [
      { source: "/qa", destination: "/qa/index.html" },
      { source: "/knowledge", destination: "/knowledge/index.html" },
      { source: "/knowledge/:slug", destination: "/knowledge/:slug/index.html" },
      { source: "/manuals", destination: "/manuals/index.html" },
      { source: "/manuals/:slug", destination: "/manuals/:slug/index.html" },
      { source: "/services/:slug", destination: "/services/:slug/index.html" },
      { source: "/about", destination: "/about/index.html" },
      { source: "/cases", destination: "/cases/index.html" },
      { source: "/faq", destination: "/faq/index.html" }
    ];
  }
};

export default nextConfig;
