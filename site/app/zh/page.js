import LandingPage from "../../components/LandingPage";
import { landingContent } from "../../lib/content";

export const metadata = {
  title: "AI 写作分身 | My Digital Mentor",
  description:
    "把你过去写过的文章，变成一个会继续帮你写的 AI 写作分身。导入旧内容、检索旧观点、保留表达方式，生成更像你的新稿。",
  openGraph: {
    title: "AI 写作分身 | My Digital Mentor",
    description:
      "把你过去写过的文章，变成一个会继续帮你写的 AI 写作分身。导入旧内容、检索旧观点、保留表达方式，生成更像你的新稿。",
    siteName: "My Digital Mentor",
    type: "website",
    locale: "zh_CN",
    url: "/zh",
    images: [
      {
        url: "/opengraph-image",
        width: 1200,
        height: 630,
        alt: "AI 写作分身 by My Digital Mentor"
      }
    ]
  },
  twitter: {
    card: "summary_large_image",
    title: "AI 写作分身 | My Digital Mentor",
    description:
      "把你过去写过的文章，变成一个会继续帮你写的 AI 写作分身。导入旧内容、检索旧观点、保留表达方式，生成更像你的新稿。",
    images: ["/opengraph-image"]
  }
};

export default function ChineseLandingPage() {
  return <LandingPage content={landingContent.zh} />;
}
