import LandingPage from "@/components/LandingPage";
import { landingContent } from "@/lib/content";

export const metadata = {
  title: "Personal AI Writer | My Digital Mentor",
  description:
    "Turn your past writing into an AI writing system that sounds like you. Import your archive, retrieve your old ideas, and generate new drafts grounded in your own voice."
};

export default function EnglishLandingPage() {
  return <LandingPage content={landingContent.en} />;
}
