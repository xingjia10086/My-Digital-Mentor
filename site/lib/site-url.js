const FALLBACK_URL = "http://localhost:3000";

function normalizeUrl(value) {
  if (!value) {
    return null;
  }

  const withProtocol = value.startsWith("http") ? value : `https://${value}`;
  return withProtocol.replace(/\/$/, "");
}

export function getSiteUrl() {
  return (
    normalizeUrl(process.env.NEXT_PUBLIC_SITE_URL) ||
    normalizeUrl(process.env.VERCEL_PROJECT_PRODUCTION_URL) ||
    FALLBACK_URL
  );
}

