import os
from dotenv import load_dotenv
from google import genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
EMBEDDING_MODEL = "models/gemini-embedding-001"

# Use the new google-genai SDK with the API key
API_KEY = os.environ.get("GOOGLE_API_KEY", "")
client = genai.Client(api_key=API_KEY)


def format_docs(docs):
    formatted = []
    for d in docs:
        source = d.metadata.get('source_file', '未知文章')
        formatted.append(f"【摘自文章：《{source}》】\n{d.page_content}")
    return "\n\n---\n\n".join(formatted)


def main():
    print("=== 初始化 星佳的数字导师大脑 ===")
    
    if not os.path.exists(CHROMA_PERSIST_DIR):
        print(f"错误：找不到本地知识库 {CHROMA_PERSIST_DIR}。请先运行 rag_ingest.py 构建知识库。")
        return
    
    # Session-based Conversation History
    chat_history = [] 
    MAX_HISTORY = 3 # Remember last 3 exchanges (Q&A pairs)
    
    # Show available models first and pick the best one
    print("\n[检查可用的 Gemini 模型...]")
    available = []
    for m in client.models.list():
        if 'gemini' in m.name.lower() and 'generate' in str(getattr(m, 'supported_actions', '')).lower():
            available.append(m.name)
            print(f"  ✓ {m.name}")
    
    # Pick the best available model
    chosen_model = None
    for preferred in ["gemini-2.5-pro", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]:
        for a in available:
            if preferred in a:
                chosen_model = a
                break
        if chosen_model:
            break
    
    if not chosen_model and available:
        chosen_model = available[0]
    
    if not chosen_model:
        chosen_model = "gemini-2.0-flash"
        print(f"[警告] 无法自动检测模型，使用默认值: {chosen_model}")
    else:
        print(f"\n[使用模型]: {chosen_model}")
    
    print(f"\n正在加载本地 ChromaDB...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=API_KEY
    )
    
    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="wechat_articles"
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    print("\n✅ AI 导师已上线。输入 'clear' 清空记忆，按 Ctrl+C 退出。\n")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n有什么困惑？说来听听：\n> ")
            if not user_input.strip():
                continue
            if user_input.lower() in ['exit', 'quit']:
                break
            if user_input.lower() == 'clear':
                chat_history = []
                print("\n[导师]: 好的，我已经清空了刚才的对话记忆，我们重新开始。")
                continue
                
            print("\n[导师沉思中... 正在搜索你的历史文章]")
            
            # Contextualized Query: Combine current input with previous history for better retrieval
            search_query = user_input
            if chat_history:
                # Use the last Q&A to provide thematic context for the vector search
                search_query = f"关于 {chat_history[-1]['q']} 的进一步探讨: {user_input}"

            # 1. Retrieve relevant history from ChromaDB
            # We increase k to 6 for a broader look, then re-rank or filter if needed
            docs = vectorstore.similarity_search(search_query, k=6) 
            context_str = format_docs(docs)
            
            print("\n[引用的历史灵感]:")
            unique_sources = []
            for d in docs:
                src = d.metadata.get('source_file', '未知')
                if src not in unique_sources:
                    unique_sources.append(src)
                    print(f"  📖 《{src}》")
                
            # 2. Build History String
            history_str = ""
            if chat_history:
                history_str = "\n【最近的对话历史】：\n"
                for h in chat_history:
                    history_str += f"星佳: {h['q']}\n导师: {h['a'][:200]}...\n" # Keep history summary concise
            
            # 3. Build the mentor prompt
            prompt = f"""你是星佳的数字克隆体也是他的人生导师。你汇聚了他过去五年的思考结晶与经验。
请结合下面这些他当年写下的历史文章片段，并融入顶尖的心理学与哲学战略思维，
以一位包容且充满智慧的良师益友的口吻，结合当前的对话上下文，深入探讨并解答他当下的困惑。

【注意规则】：
1. 你的回答要具有启发性，像是一位深交多年的挚友在启发他思考。
2. 潜移默化地化用他过去写过的心得、比喻与金句。
3. 允许适度的一针见血，甚至是温柔的“冒犯”，以达到导师开导的效果。

{history_str}

【回忆起你的过往思考片段】：
{context_str}

【星佳当前的困惑/追问】：
{user_input}

你的回答："""

            print("\n[导师的回答]:")
            full_response = ""
            # 4. Stream using the new google-genai SDK
            for chunk in client.models.generate_content_stream(
                model=chosen_model,
                contents=prompt
            ):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_response += chunk.text
            print("\n")
            
            # 5. Update History
            chat_history.append({"q": user_input, "a": full_response})
            if len(chat_history) > MAX_HISTORY:
                chat_history.pop(0)

            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n导师休息了。再见。")
            break
        except Exception as e:
            print(f"\n[发生错误]: {e}")

if __name__ == "__main__":
    main()
