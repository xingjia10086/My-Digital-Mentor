import os
import json
import random
import time
import schedule
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from langchain_community.vectorstores import Chroma
from langchain_google_vertexai import VertexAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
# 注意：这里需要填写真实的 user open_id，建议也可以加入到 .env 中
TARGET_USER_ID = os.environ.get("FEISHU_TARGET_USER_ID", "")

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
EMBEDDING_MODEL = "text-embedding-004"

print("=== 初始化 星佳数字导师 (定点灵感引擎) ===")

# 1. Initialize Clients
print("正在连接 本地 ChromaDB 知识库...")
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
lark_client = lark.Client.builder().app_id(FEISHU_APP_ID).app_secret(FEISHU_APP_SECRET).build()


def push_job(time_tag):
    print(f"\n--- 执行【{time_tag}】推送任务 ---")
    
    # 2. Randomly select a philosophical theme
    themes = [
        "长期主义", "破局", "拒绝内卷", "认知升级", "财富自由", 
        "精力管理", "人生战略", "香港身份与教育规划", "孤独与独处",
        "职场向上管理", "商业模式", "如何面对焦虑", "AI改变时代",
        "个人IP建立", "底层逻辑"
    ]
    selected_theme = random.choice(themes)
    print(f"随机抽取主题: 【{selected_theme}】")

    # 3. Retrieve a related insight from history (Increase k to get variability, then random choice)
    docs = vectorstore.similarity_search(selected_theme, k=15)
    if not docs:
        print("💡 知识库中未找到相关片段。")
        return

    # Randomly pick one from the top k results to avoid repetition
    doc = random.choice(docs)
    source_file = doc.metadata.get('source_file', '未知文章')
    content_preview = doc.page_content.strip()

    if len(content_preview) > 300:
        content_preview = content_preview[:300] + "..."

    # 4. Construct Feishu Rich Text Card
    card_content = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "blue",
            "title": {
                "content": f"🌅 星佳的数字大脑：{time_tag}金句推送",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": f"**触发主题**：{selected_theme}\n**出自文章**：《{source_file}》\n\n\n**当年你是这么写的：**\n\n*{content_preview}*",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "note",
                "elements": [
                    {
                        "content": "✨ 保持专注，拒绝内卷。新的一段辰光，破局而生。",
                        "tag": "lark_md"
                    }
                ]
            }
        ]
    }

    # 5. Send Proactive Message
    print(f"准备向用户 {TARGET_USER_ID} 发送飞书卡片...")
    request = CreateMessageRequest.builder() \
        .receive_id_type("open_id") \
        .request_body(CreateMessageRequestBody.builder()
            .receive_id(TARGET_USER_ID)
            .msg_type("interactive")
            .content(json.dumps(card_content))
            .build()) \
        .build()

    try:
        response = lark_client.im.v1.message.create(request)
        if response.success():
            print("✅ 推送成功！")
        else:
            print(f"❌ 推送失败: {response.code}, {response.msg}")
    except Exception as e:
        print(f"❌ 推送发生异常: {e}")

# 立即先推两条测试一下逻辑，验证是否重复
push_job("测试1 (重制版)")
time.sleep(3)
push_job("测试2 (重制版)")

# 将调度任务设定为早中晚各一次
schedule.every().day.at("09:00").do(push_job, time_tag="上午")
schedule.every().day.at("13:00").do(push_job, time_tag="中午")
schedule.every().day.at("18:30").do(push_job, time_tag="晚间")

print("\n🚀 飞书定时推送特工已启动！(将会挂起等待时间到达)")
print("设定推送时间节点：09:00, 13:00, 18:30")

# 保持进程常驻运行
while True:
    schedule.run_pending()
    time.sleep(60)
