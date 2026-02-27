import os
import time
import random
import logging
from datetime import datetime
import schedule
import tweepy
from dotenv import load_dotenv
from google import genai
from langchain_community.vectorstores import Chroma
from langchain_google_vertexai import VertexAIEmbeddings

load_dotenv()

# --- Logging Setup ---
logging.basicConfig(
    filename='twitter_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

# --- Twitter API Credentials (User Needs to Fill These) ---
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET", "")
# ==========================================================

# --- Vertex AI & ChromaDB Setup ---
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "gen-lang-client-0834352502")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
EMBEDDING_MODEL = "text-embedding-004"
API_KEY = os.environ.get("GOOGLE_API_KEY", "")
MODEL_NAME = "gemini-2.5-pro"  

def init_twitter_client():
    """初始化 Twitter v2 客户端"""
    if not TWITTER_API_KEY:
        logging.error("❌ 尚未配置 Twitter API 密钥！请在 .env 文件中填入。")
        return None
    
    try:
        client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET
        )
        return client
    except Exception as e:
        logging.error(f"Twitter 客户端初始化失败: {e}")
        return None

def generate_tweet_content():
    """从数据库捞取知识并提炼为推文"""
    logging.info("🧠 开始从 ChromaDB 深潜抓取记忆碎片...")
    
    try:
        # Load DB
        embeddings = VertexAIEmbeddings(model_name=EMBEDDING_MODEL, project=PROJECT_ID, location=LOCATION)
        vectorstore = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings, collection_name="wechat_articles")
        
        # Randomly sample fragments
        collection_data = vectorstore._collection.get()
        all_docs = collection_data['documents']
        
        if not all_docs:
            logging.error("知识库为空！")
            return None
            
        sample_size = min(5, len(all_docs))
        sample_indices = random.sample(range(len(all_docs)), sample_size)
        sampled_texts = [all_docs[i] for i in sample_indices]
        context_str = "\n\n---\n\n".join(sampled_texts)
        
        logging.info("🤖 记忆抓取完毕。交给 Gemini 大脑重塑推特文案...")
        
        # Call Gemini
        genai_client = genai.Client(api_key=API_KEY)
        prompt = f"""你是星佳，一位在 X (Twitter) 上拥有高影响力的华语创投、自我成长与商业博主。
请结合以下从你过去公众号文章中提取的随机【思想碎片】，提取核心论点，写一条具有极强穿透力的【纯英文推文(Tweet)】。

【历史思想碎片（随机抓取）】：
{context_str}

【写作极客指令】：
1. 必须是纯正流畅的 Native English。
2. 风格：像硅谷创投大佬的心声。极简、通透、反直觉。
3. 格式：第一句话极其吸睛（Hook）。多用短句和空行排版。总长度绝对不能超过 260 字符，不要带 emoji。
4. 结尾：必须不留空隙地加上 2 个高级别 Hashtag（例如 #Founders #Mindset）。
5. 直接输出正式的推文内容，不要包含中文，也不要讲废话。"""

        response = genai_client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        
        tweet_text = response.text.strip()
        # Ensure extremely strict cleaning for API limits
        tweet_text = tweet_text.replace('**', '').replace('"', '').replace("'", "")
        return tweet_text
        
    except Exception as e:
        logging.error(f"大模型生成推文失败: {e}")
        return None

def job_post_tweet():
    """定时任务：生成并发送推特"""
    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⏰ 定时器触发！准备执行发推流程...")
    
    twitter_client = init_twitter_client()
    if not twitter_client:
        return
        
    tweet_text = generate_tweet_content()
    if not tweet_text:
        return
        
    logging.info(f"📝 准备发送推文:\n{tweet_text}\n(Length: {len(tweet_text)})")
    
    try:
        # 真正发送至推特网络
        response = twitter_client.create_tweet(text=tweet_text)
        tweet_id = response.data['id']
        logging.info(f"✅ 发送成功! Tweet ID: {tweet_id}")
        logging.info("="*50)
    except tweepy.errors.Forbidden as fe:
        logging.error("🚫 被推特服务器拒绝 (Forbidden)！可能原因：API 没有开通 Read and Write 权限，或者发送了重复内容。")
    except Exception as e:
        logging.error(f"❌ 发送推文遭遇网络错误: {e}")

def main():
    print("="*60)
    print(" 🐦 星佳的 24 小时全自动数字生命发推机 (Proactive Agent) 已启动")
    print("="*60)
    
    # 模拟“刚开机测试一下”，可以立刻发一条，如果你不想刚启动就发，可以把下面这行注释掉
    job_post_tweet() 
    
    # --- 调度器设置 (Scheduler) ---
    # 设定每天什么时候发。为了模拟人类作息和防止被封，建议固定时间或随机休眠。
    
    # 例如：每天早上 08:30 发一条
    schedule.every().day.at("08:30").do(job_post_tweet)
    
    # 例如：每天晚上 21:15 发一条
    schedule.every().day.at("21:15").do(job_post_tweet)
    
    # 或者每隔 8 小时发一条
    # schedule.every(8).hours.do(job_post_tweet)
    
    print("\n⏳ 脚本进入终极无感潜伏模式... 按 Ctrl+C 随时终止。")
    print("日志将同步保存在目录下的 twitter_logs.txt 中。")
    
    while True:
        schedule.run_pending()
        time.sleep(60) # 每 60 秒醒来看一下时间

if __name__ == "__main__":
    main()
