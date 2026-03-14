import os
import re
import subprocess
from dotenv import load_dotenv
from google import genai
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

# --- Configuration ---
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "")
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
        formatted.append(f"【摘自文章：《{source}》】\n{d.page_content}")
    return "\n\n---\n\n".join(formatted)

def clean_for_tts(text):
    """移除 Markdown 等会影响语音朗读的干扰字符，让语音更自然。"""
    text = re.sub(r'[*_#`]', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text) # 移除链接
    text = text.replace('\n', '。')
    # 限制单边语音长度，防止生成太久
    return text[:800] 

def speak_text(text):
    """调用 edge-tts 生成语音并播放 (Windows 专用方案)"""
    print("\n[导师发声中... 正在生成语音🎵]")
    clean_txt = clean_for_tts(text)
    temp_file = "mentor_voice.mp3"
    
    # zh-CN-YunxiNeural: 男性知性声音; zh-CN-XiaoxiaoNeural: 女性声音
    try:
        # Generate MP3
        subprocess.run([
            "edge-tts",
            "--text",
            clean_txt,
            "--voice",
            "zh-CN-YunxiNeural",
            "--write-media",
            temp_file,
        ], check=True)
        # Play MP3 on Windows (will open default player or run silently depending on settings)
        # A lightweight cross-platform alternative if 'start' opens a big app is sometimes just to alert the user.
        print("\n✅ 语音已生成！正在使用系统默认播放器播放...")
        os.system(f"start {temp_file}") 
    except Exception as e:
        print(f"语音生成失败: {e}")

def main():
    print("=== 初始化 星佳的数字导师大脑 (🗣️ 语音交互版) ===")
    
    if not os.path.exists(CHROMA_PERSIST_DIR):
        print(f"错误：找不到本地知识库 {CHROMA_PERSIST_DIR}。请先运行 rag_ingest.py 构建知识库。")
        return
    
    chat_history = [] 
    MAX_HISTORY = 3 
    
    # Model Selection
    available = []
    for m in client.models.list():
        if 'gemini' in m.name.lower() and 'generate' in str(getattr(m, 'supported_actions', '')).lower():
            available.append(m.name)
            
    chosen_model = "gemini-2.0-flash"
    for preferred in ["gemini-2.5-pro", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]:
        for a in available:
            if preferred in a:
                chosen_model = a
                break
        if chosen_model != "gemini-2.0-flash":
            break
            
    print(f"\n[使用模型]: {chosen_model}")
    print(f"正在加载本地 ChromaDB...\n")
    
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
    
    # We use a smaller K here to ensure the TTS answer isn't overwhelmingly long or chaotic
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    print("\n✅ 语音导师已上线。输入 'clear' 清空记忆，按 Ctrl+C 退出。\n")
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
            
            search_query = user_input
            if chat_history:
                search_query = f"结合语境: {chat_history[-1]['q']} 对于 {user_input} 的探讨"

            docs = retriever.invoke(search_query)
            context_str = format_docs(docs)
            
            history_str = ""
            if chat_history:
                history_str = "\n【最近的对话】：\n"
                for h in chat_history:
                    history_str += f"星佳: {h['q']}\n导师: {h['a'][:100]}...\n"
                    
            # Prompt tailored for voice delivery (short, punchy sentences)
            prompt = f"""你是星佳的数字克隆体也是他的人生导师。
结合历史文章片段，解答他当下的困惑。

【注意规则 - 这是为了语音合成准备的口语化文案】：
1. 你的回答必须非常**口语化、口语化、口语化**，像老朋友在面对面聊天（不要用列条目、要点123这种书面结构）。
2. 把星佳曾经的金句自然地说出来，仿佛那就是你随口想到的。
3. 把回答控制在 150 字以内，字数越精简有力越好，因为要转成语音朗读！

{history_str}

【历史片段】：
{context_str}

【星佳当前的困惑】：
{user_input}

你的回答 (请直接给出一段能直接朗读的流畅口语对话)："""

            print("\n[导师的回答]:")
            full_response = ""
            for chunk in client.models.generate_content_stream(
                model=chosen_model,
                contents=prompt
            ):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_response += chunk.text
            print("\n")
            
            # Text to Speech Generation & Play
            speak_text(full_response)
            
            # Update History
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
