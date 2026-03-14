import LandingPage from "@/components/LandingPage";
import { landingContent } from "@/lib/content";

export const metadata = {
  title: "AI 写作分身 | My Digital Mentor",
  description:
    "把你过去写过的文章，变成一个会继续帮你写的 AI 写作分身。导入旧内容、检索旧观点、保留表达方式，生成更像你的新稿。"
};

export default function ChineseLandingPage() {
  return <LandingPage content={landingContent.zh} />;
}
