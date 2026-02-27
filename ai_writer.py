import os
import argparse
from dotenv import load_dotenv
from google import genai
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

# --- Configuration ---
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "gen-lang-client-0834352502")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
EMBEDDING_MODEL = "text-embedding-004"
API_KEY = os.environ.get("GOOGLE_API_KEY", "")
client = genai.Client(api_key=API_KEY)


def format_docs(docs):
    formatted = []
    for d in docs:
        source = d.metadata.get('source_file', '未知文章')
        formatted.append(f"【参考篇目：《{source}》】\n{d.page_content}")
    return "\n\n---\n\n".join(formatted)


def generate_draft(topic):
    print("=== 星佳的数字分身：文章起草机 ===")
    print(f"\n[任务目标]: 构思关于“{topic}”的文章\n")
    
    if not os.path.exists(CHROMA_PERSIST_DIR):
        print(f"错误：找不到知识库 {CHROMA_PERSIST_DIR}")
        return
        
    print("[1/3] 正在选择最佳模型...")
    available = []
    for m in client.models.list():
        if 'gemini' in m.name.lower() and 'generate' in str(getattr(m, 'supported_actions', '')).lower():
            available.append(m.name)
            
    chosen_model = "gemini-2.0-flash"
    for preferred in ["gemini-2.5-pro", "gemini-2.0-flash", "gemini-1.5-pro"]:
        for a in available:
            if preferred in a:
                chosen_model = a
                break
        if chosen_model != "gemini-2.0-flash":
            break
            
    print(f"  ✓ 使用模型: {chosen_model}")
    
    print("\n[2/3] 正在从 1.8万 个历史片段中检索相关灵感与金句...")
    embeddings = VertexAIEmbeddings(
        model_name=EMBEDDING_MODEL,
        project=PROJECT_ID,
        location=LOCATION
    )
    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="wechat_articles"
    )
    
    # We want more context for writing than just casual conversation
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
    docs = retriever.invoke(topic)
    context_str = format_docs(docs)

    unique_sources = []
    for d in docs:
        src = d.metadata.get('source_file', '未知')
        if src not in unique_sources:
            unique_sources.append(src)
            print(f"  📖 激活记忆节点: 《{src}》")
            
    print("\n[3/3] 开始提笔撰写初稿...\n")
    print("=" * 60)
    
    prompt = f"""你是星佳，一位深耕互联网、教育规划、自我成长的公众号主理人。
现在你需要写一篇新的微信公众号文章初稿，主题是：【{topic}】。

请你先阅读以下你过去写过的相关文章片段，仔细体会你自己的写作文风、排版习惯、常用金句和思维逻辑：

【历史风格参考】：
{context_str}

【写作要求】：
1. 你的文章不是冷冰冰的科普，而是带有强烈的个人经验色彩和故事性，像是在跟读者交心。
2. 完美复刻历史参考片段中的写作风格，包括自然的分段、合理的设问、以及一针见血的断言。
3. 请为这篇文章起一个吸引人的、带有点“星佳味道”的标题（放在全文最前面）。
4. 字数要求在 1500 字以上，结构上要有：引入（引起共鸣） -> 破题（给出独家视角） -> 论证（结合具体案例或道理） -> 结论（一句有力的结语）。
5. 直接输出 Markdown 格式的正式文章内容，不需要任何介绍自己的废话。

开始创作吧："""

    for chunk in client.models.generate_content_stream(
        model=chosen_model,
        contents=prompt
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            
    print("\n")
    print("=" * 60)
    print("\n✅ 初稿生成完毕。你可以直接将 Markdown 复制到编辑器中润色。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Writer - Generate articles based on historical context.")
    parser.add_argument("-t", "--topic", type=str, required=True, help="你想写的文章主题或几个大纲关键词。")
    args = parser.parse_args()
    
    generate_draft(args.topic)
