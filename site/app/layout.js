import "./globals.css";
import { headers } from "next/headers";
import { getSiteUrl } from "../lib/site-url";

const siteUrl = getSiteUrl();

export const metadata = {
  metadataBase: new URL(siteUrl),
  applicationName: "My Digital Mentor",
  alternates: {
    languages: {
      en: "/en",
      zh: "/zh"
    }
  }
};

export default async function RootLayout({ children }) {
  const requestHeaders = await headers();
  const pathname = requestHeaders.get("x-pathname") || "/en";
  const htmlLang = pathname.startsWith("/zh") ? "zh" : "en";

  return (
    <html lang={htmlLang}>
      <body>{children}</body>
    </html>
  );
}
