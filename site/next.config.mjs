/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: "/china-guide/updates/:path*",
        destination:
          "https://china-entry-playbook.xingjia520.chatgpt.site/china-guide/updates/:path*"
      }
    ];
  }
};

export default nextConfig;
