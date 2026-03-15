import LandingPage from "../../components/LandingPage";
import { landingContent } from "../../lib/content";

export const metadata = {
  title: "Personal AI Writer | My Digital Mentor",
  description:
    "Turn your past writing into an AI writing system that sounds like you. Import your archive, retrieve your old ideas, and generate new drafts grounded in your own voice.",
  openGraph: {
    title: "Personal AI Writer | My Digital Mentor",
    description:
      "Turn your past writing into an AI writing system that sounds like you. A deployable bilingual landing site for My Digital Mentor.",
    siteName: "My Digital Mentor",
    type: "website",
    locale: "en_US",
    url: "/en",
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
    title: "Personal AI Writer | My Digital Mentor",
    description:
      "Turn your past writing into an AI writing system that sounds like you. A deployable bilingual landing site for My Digital Mentor.",
    images: ["/opengraph-image"]
  }
};

export default function EnglishLandingPage() {
  return <LandingPage content={landingContent.en} />;
}
