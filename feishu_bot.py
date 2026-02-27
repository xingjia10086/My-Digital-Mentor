import os
import json
import re
import logging
import threading
import feedparser
from dotenv import load_dotenv
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from google import genai
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

load_dotenv()

# --- Configuration ---
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
EMBEDDING_MODEL = "text-embedding-004"
API_KEY = os.environ.get("GOOGLE_API_KEY", "")

MODEL_NAME = "gemini-2.5-pro"  

print("=== 初始化 星佳数字导师 (视觉分发矩阵升级版) ===")
print("正在连接 Google Gemini 和本地 ChromaDB 知识库...")
genai_client = genai.Client(api_key=API_KEY)
lark_client = lark.Client.builder().app_id(FEISHU_APP_ID).app_secret(FEISHU_APP_SECRET).build()

vertexai.init(project=PROJECT_ID, location=LOCATION)
# 初始化 Google Imagen 画图模型 (升级到最新的 002 版本)
try:
    from vertexai.preview.vision_models import ImageGenerationModel
    imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
except Exception as e:
    print(f"Imagen3 载入失败: {e}")
    imagen_model = None

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

chat_histories = {}
MAX_HISTORY = 3

CACHE_FILE = os.path.join(BASE_DIR, "feishu_processed.json")
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r") as f:
            processed_msg_ids = json.load(f)
    except:
        processed_msg_ids = []
else:
    processed_msg_ids = []
MAX_PROCESSED = 200

def save_cache():
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(processed_msg_ids, f)
    except:
        pass

def format_docs(docs):
    formatted = []
    for d in docs:
        source = d.metadata.get('source_file', '未知文章')
        formatted.append(f"【摘自文章：《{source}》】\n{d.page_content}")
    return "\n\n---\n\n".join(formatted)

def fetch_daily_news():
    feeds = {
        "36氪 (商业创投)": "https://36kr.com/feed",
        "Hacker News (全球前沿科技)": "https://news.ycombinator.com/rss",
        "V2EX (极客热榜)": "https://www.v2ex.com/index.xml",
        "ReadHub (科技动态)": "https://readhub.cn/rss",
        "华尔街见闻 (全球宏观与市场)": "https://wallstreetcn.com/rss/gold",
        "华尔街日报 WSJ (港美股与财经)": "https://cn.wsj.com/zh-hans/rss",
        "FT中文网 (金融时报)": "https://www.ftchinese.com/rss/feed",
        "第一财经 (大陆与港股盘面)": "https://www.yicai.com/rss/news.xml"
    }
    news_text = ""
    for name, url in feeds.items():
        try:
            f = feedparser.parse(url)
            news_text += f"\n【{name}】\n"
            for entry in f.entries[:5]: # 从每个源抓取前 5 条
                news_text += f"- {entry.title}\n"
        except Exception as e:
            pass
    return news_text

def process_message(sender_id, text, message_id):
    history = chat_histories.get(sender_id, [])
    if text.strip().lower() in ['clear', '清除记忆', '清空记忆']:
        chat_histories[sender_id] = []
        reply_msg(message_id, "🧠 咔嚓！我已经清空了刚才的对话上下文，让我们开启一个全新的话题吧。")
        return
        
    is_xhs = False
    is_tiktok = False
    is_news = False
    actual_query = text
    
    if text.lower().startswith("/xhs "):
        is_xhs = True
        actual_query = text[5:].strip()
    elif text.lower().startswith("/tiktok "):
        is_tiktok = True
        actual_query = text[8:].strip()
    elif text.lower().strip() == "/news":
        is_news = True
        actual_query = "请帮我解读今天的科技商业晨报。"
    elif text.lower().startswith("/news "):
        is_news = True
        actual_query = text[6:].strip()
    
    search_query = actual_query
    if history and not (is_xhs or is_tiktok or is_news):
        search_query = f"关于 {history[-1]['q']} 的进一步探讨: {actual_query}"
        
    print(f"\n[检索意图]: {search_query}")
    docs = vectorstore.similarity_search(search_query, k=6) 
    context_str = format_docs(docs)
    unique_sources = list(set([d.metadata.get('source_file', '未知') for d in docs]))
    
    history_str = ""
    if history and not (is_xhs or is_tiktok or is_news):
        history_str = "\n【最近的对话历史】：\n"
        for h in history:
            history_str += f"星佳: {h['q']}\n导师: {h['a'][:150]}...\n"
            
    if is_xhs:
        prompt = f"""你是星佳旗下的金牌小红书爆款文案操盘手。你的任务是将深沉的商业思考重塑为高赞、高收藏的小红书图文文案。
请基于以下星佳的【历史文章片段】，针对用户提出的主题：“{actual_query}”，写一篇小红书图文脚本。

【非常重要：配图指令】：在文末，请务必用特定的标签包围一段纯英文的生图 Prompt，这会让 AI 画师生成小红书封面图。
**你必须确保这张图是典型的高质量“小红书爆款风格”**（例如：极简高级感、明亮治愈系、商务精英桌面、或者精致的平铺摆件）。
请在 Prompt 中强制加入以下关键词来控制画风：`editorial photography`, `lifestyle aesthetic`, `bright natural lighting`, `high-end minimalism`, `shot on iPhone 15 Pro`, `8k resolution`, `photorealistic`。
格式必须是：
<image_prompt>A highly detailed, beautiful minimalistic flat lay style photography featuring [具体物品/场景], editorial photography, lifestyle aesthetic, bright natural lighting, high-end minimalism, 8k resolution.</image_prompt>

【小红书风格要求】：
1. 标题必须极具吸引力，加入适当的emoji，不超过20字，并在最前面独立成行。
2. 第一段爆发共鸣，一秒拉住读者。
3. 正文采用列表式，重点词句加粗，富有“呼吸感”。
4. 结尾要有总结金句和互动引导。附带3-5个Hashtag。

【星佳的历史文章片段】：
{context_str}
"""
    elif is_tiktok:
        prompt = f"""你是星佳旗下的顶尖短视频编导。请基于以下星佳的【历史文章片段】，写一篇极具网感的短视频口播脚本（约200-300字）。

【非常重要】：在文末，请务必用特定的标签包围一段英文的生图 Prompt，这会让 AI 画师生成配合视频调性的插图封面。格式必须是：
<image_prompt>A cinematic, ultra-realistic portrait photography of XXX...</image_prompt>

【短视频剧本规范】：
1. 黄金前三秒：直接痛点开大。
2. 情绪推高：语言极简、犀利，多用断句。带上画面和语气提示。
3. 结尾：抛出一个反问句，激发评论欲。

【星佳的历史文章片段】：
{context_str}
"""
    elif is_news:
        today_news = fetch_daily_news()
        prompt = f"""你是星佳的数字克隆体。每天清晨，你都会作为“主动情报捕手”，用你的认知模型过滤并解读当天发生的世界大事，提供《今日商业简评》。

【核心指令：用户特殊问答要求】：
当前用户非常明确地希望你解答或点评的主题是：【{actual_query}】。
你必须**绝绝对对优先**围绕这个主题展开这篇晨报！不要去扯完全无关的新闻。如果你在下面抓取的新闻聚合中找不到直接相关的内容，请调用你自身(Gemini 1.5)庞大的金融、科技知识储备去强行解答用户指定的主题！

【今日辅助素材仓库（刚刚自动抓取的部分科技与商业动态）】：
{today_news}

【星佳的历史底层认知与破局价值观】：
{context_str}

写一篇深度且辛辣的【专属晨报】发给星佳本人。要求：
1. **死守主题**：第一段开门见山，直接回答和剖析用户问的【{actual_query}】相关话题。
2. **知识融合**：将今日素材（如果有相关）和你自身的大模型储备，以及星佳的历史心血观点（如周期、长期主义、破局）三者完美融合。
3. **犀利通透**：语气要像星佳本人一样：通透、犀利、带有一点俯瞰全局的“局外人清醒”。
4. **精美排版**：使用 Markdown 丰富格式（加粗、列表、适当emoji），适合在手机飞书上碎片化阅读体验。
5. **【非常重要：配图指令】**：文末必须包含英文生图 Prompt 生成晨报封面，要求是带有高档商业感的清晨办公桌面：
<image_prompt>A highly detailed, beautiful minimalistic flat lay style photography featuring an aesthetic morning coffee, a glowing tablet with financial charts or news UI, editorial photography, lifestyle aesthetic, bright natural morning lighting, 8k resolution.</image_prompt>
"""
    else:
        prompt = f"""你是星佳的数字克隆体也是他的人生导师。
结合历史文章片段，结合当前的对话上下文，深入探讨并解答他当下的困惑。
要有启发性，化用写过的心得与金句。使用 Markdown 排版。

{history_str}

【发掘历史思考片段】：
{context_str}

【当前困惑】：
{actual_query}
"""

    try:
        response = genai_client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        reply = response.text
        
        # Check if we need to generate an image
        image_prompt_match = re.search(r"<image_prompt>(.*?)</image_prompt>", reply, re.DOTALL)
        image_key = None
        
        if image_prompt_match and (is_xhs or is_tiktok or is_news):
            image_prompt = image_prompt_match.group(1).strip()
            # Clean reply text, rip out the tag
            reply = re.sub(r"<image_prompt>.*?</image_prompt>", "", reply, flags=re.DOTALL).strip()
            
            print(f"[{MODEL_NAME} / Imagen 3] 正在生成画作: {image_prompt}")
            try:
                images = imagen_model.generate_images(
                    prompt=image_prompt,
                    number_of_images=1,
                    aspect_ratio="3:4" if is_xhs else "16:9"
                )
                temp_image_path = "temp_generated.jpg"
                images[0].save(location=temp_image_path)
                
                # Upload to Feishu
                upload_req = CreateImageRequest.builder().request_body(
                    CreateImageRequestBody.builder()
                        .image_type("message")
                        .image(open(temp_image_path, "rb"))
                        .build()
                ).build()
                
                upload_res = lark_client.im.v1.image.create(upload_req)
                if upload_res.success():
                    image_key = upload_res.data.image_key
                    print(f"成功上传图片到飞书，Image Key: {image_key}")
            except Exception as img_e:
                print(f"画图引擎错误: {img_e}")
                reply += f"\n\n[注：自动配图失败: {img_e}]"

        reply += "\n\n---\n*📚 此文库素材溯源:* \n"
        for src in unique_sources:
            reply += f"- 《{src}》\n"
            
        if not (is_xhs or is_tiktok or is_news):
            history.append({"q": actual_query, "a": reply})
            if len(history) > MAX_HISTORY:
                history.pop(0)
            chat_histories[sender_id] = history
            
        # Send back to User
        if image_key:
            # Send the image first
            img_req = ReplyMessageRequest.builder() \
                .message_id(message_id) \
                .request_body(ReplyMessageRequestBody.builder()
                    .content(json.dumps({"image_key": image_key}))
                    .msg_type("image")
                    .build()) \
                .build()
            lark_client.im.v1.message.reply(img_req)
            
        # Send the text
        txt_req = ReplyMessageRequest.builder() \
            .message_id(message_id) \
            .request_body(ReplyMessageRequestBody.builder()
                .content(json.dumps({"text": reply}))
                .msg_type("text")
                .build()) \
            .build()
        lark_client.im.v1.message.reply(txt_req)

    except Exception as e:
        print(f"Generation error: {e}")
        reply_msg(message_id, f"⚠️ 数字大脑严重脱机：{e}")

def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    message = data.event.message
    if message.message_type != "text": return
    
    if message.message_id in processed_msg_ids:
        print(f"Skipping duplicate message: {message.message_id}")
        return
        
    processed_msg_ids.append(message.message_id)
    if len(processed_msg_ids) > MAX_PROCESSED:
        processed_msg_ids.pop(0)
    save_cache()
        
    content = json.loads(message.content)
    text = content.get("text", "").strip()
    text = text.replace("@_user_1", "").strip()
    
    sender_id = data.event.sender.sender_id.open_id
        
    # Process the generation in a separate thread so this function returns immediately 
    # and Feishu doesn't timeout and retry the event.
    threading.Thread(target=process_message, args=(sender_id, text, message.message_id)).start()

def reply_msg(msg_id, text):
    try:
        req = ReplyMessageRequest.builder() \
            .message_id(msg_id) \
            .request_body(ReplyMessageRequestBody.builder()
                .content(json.dumps({"text": text}))
                .msg_type("text")
                .build()) \
            .build()
        lark_client.im.v1.message.reply(req)
    except Exception as e:
        print("Reply Error")

if __name__ == "__main__":
    event_handler = lark.EventDispatcherHandler.builder("", "") \
        .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
        .build()
        
    ws_client = lark.ws.Client(
        FEISHU_APP_ID, 
        FEISHU_APP_SECRET,
        event_handler=event_handler,
        log_level=lark.LogLevel.WARNING 
    )
    
    print("\n🚀 飞书数字主编·视觉加强版 已挂载！")
    print("支持 /xhs 与 /tiktok 指令，触发后会自动调用 Imagen 3 绘图并推送到会话中。")
    ws_client.start()
