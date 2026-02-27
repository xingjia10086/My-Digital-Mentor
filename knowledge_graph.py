import os
import json
from dotenv import load_dotenv
from google import genai
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
import random

load_dotenv()

# --- Configuration ---
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "gen-lang-client-0834352502")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
EMBEDDING_MODEL = "text-embedding-004"
API_KEY = os.environ.get("GOOGLE_API_KEY", "")

client = genai.Client(api_key=API_KEY)


def main():
    print("=== 星佳的五年思想图谱 (Knowledge Graph Extractor) ===")
    
    if not os.path.exists(CHROMA_PERSIST_DIR):
        print(f"错误：找不到知识库 {CHROMA_PERSIST_DIR}")
        return

    print("\n[1/3] 装载本地知识库...")
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
    
    # Get all documents from ChromaDB
    # Note: Chroma get() returns a dict with 'documents', 'metadatas', 'ids'
    print("  正在提取全量数据...")
    collection_data = vectorstore._collection.get()
    all_docs = collection_data['documents']
    total_docs = len(all_docs)
    print(f"  成功读取 {total_docs} 个思考片段。")
    
    # We will sample 200 random chunks to find the overarching themes to save API costs & time
    # rather than processing 18k chunks, the top themes will naturally appear in a uniform random sample.
    sample_size = min(200, total_docs)
    print(f"\n[2/3] 随机抽样 {sample_size} 个核心片段进行 AI 主题提炼...")
    sampled_docs = random.sample(all_docs, sample_size)
    combined_text = "\n\n".join(sampled_docs)
    
    # Pick a model
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
            
    print(f"  采用大模型分析引擎: {chosen_model}")
    
    prompt = f"""作为一个数据分析师和心理学家，请分析以下这 {sample_size} 个文字片段（这只是作者过去五年所有写过的几千篇文章的一小部分随机抽样）。

你的任务是提取出代表作者最核心理念、思考模型、关注领域的 **30 个**关键词或短语（例如：“破局”、“长期主义”、“教育规划”、“内卷”、“资产配置”等）。

要求：
1. 请不要解释，直接输出一段 Mermaid 格式的图表代码（graph TD）。
2. 将这 30 个词汇按照它们的内在逻辑关系（比如：因果、包含、相关）连接起来。
3. 把最重要的几个词汇设为中心节点。
4. 务必只输出合法的 Mermaid 代码，用 ```mermaid 前后缀包裹，绝对不要出现引号或特殊字符导致渲染错误。

【抽样文字材料】：
{combined_text[:60000]} # Limit characters just in case it's too long

请直接给出 Mermaid 图表代码："""

    print("\n[3/3] 正在生成思想宇宙关系图...\n")
    print("=" * 60)
    full_response = ""
    for chunk in client.models.generate_content_stream(
        model=chosen_model,
        contents=prompt
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_response += chunk.text
            
    print("\n" + "=" * 60)
    
    # Save the output to a markdown file
    output_file = os.path.join(BASE_DIR, "my_mind_map.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 星佳的个人思想图谱\n\n")
        f.write("（由 AI 随机抓取历史片段生成的核心词汇逻辑关系）\n\n")
        f.write(full_response)
        
    print(f"\n✅ 思想图谱生成完毕！")
    print(f"建议：你可以将生成的 Mermaid 代码粘贴到 https://mermaid.live/ 实时查看，或查看 {output_file}。")

if __name__ == "__main__":
    main()
