import "./globals.css";
import { getSiteUrl } from "../lib/site-url";

const title = "Personal AI Writer | My Digital Mentor";
const description =
  "Turn your past writing into an AI writing system that sounds like you. A deployable bilingual landing site for My Digital Mentor.";
const siteUrl = getSiteUrl();

export const metadata = {
  metadataBase: new URL(siteUrl),
  title,
  description,
  applicationName: "My Digital Mentor",
  openGraph: {
    title,
    description,
    siteName: "My Digital Mentor",
    type: "website",
    locale: "en_US",
    images: [
      {
        url: "/opengraph-image",
        width: 1200,
        height: 630,
        alt: "Personal AI Writer by My Digital Mentor"
      }
    ]
  },
  twitter: {
    card: "summary_large_image",
    title,
    description,
    images: ["/opengraph-image"]
  },
  alternates: {
    languages: {
      en: "/en",
      zh: "/zh"
    }
  }
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
