import { headers } from "next/headers";
import { redirect } from "next/navigation";

function getPreferredLocale(acceptLanguage = "") {
  const normalized = acceptLanguage.toLowerCase();

  return normalized.includes("zh") ? "zh" : "en";
}

export default async function HomePage() {
  const requestHeaders = await headers();
  const locale = getPreferredLocale(requestHeaders.get("accept-language") || "");

  redirect(`/${locale}`);
}
