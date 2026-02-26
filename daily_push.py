import os
import json
import random
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from langchain_community.vectorstores import Chroma
from langchain_google_vertexai import VertexAIEmbeddings

# --- Configuration ---
FEISHU_APP_ID = "cli_a91397ee08f81bdb"
FEISHU_APP_SECRET = "J1FL9TPMD97NY8wu76FNGcZL4Y6PQ0AA"
# Use the precise open_id of the target user
TARGET_USER_ID = "ou_ef03183d5527e0efbf021ca2c1ea3228"

PROJECT_ID = "gen-lang-client-0834352502" 
LOCATION = "us-central1"
CHROMA_PERSIST_DIR = r"D:\GPT\AI-demo\chroma_db"
EMBEDDING_MODEL = "text-embedding-004"

print("=== 初始化 星佳数字导师 (每日灵感引擎) ===")

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


# 2. Randomly select a philosophical theme
themes = [
    "长期主义", "破局", "拒绝内卷", "认知升级", "财富自由", 
    "精力管理", "人生战略", "香港身份与教育规划", "孤独与独处",
    "职场向上管理", "商业模式", "如何面对焦虑"
]
selected_theme = random.choice(themes)
print(f"今日随机抽取主题: 【{selected_theme}】")

# 3. Retrieve a related insight from history
docs = vectorstore.similarity_search(selected_theme, k=1)
if not docs:
    print("知识库中未找到相关片段。")
    exit()

doc = docs[0]
source_file = doc.metadata.get('source_file', '未知文章')
content_preview = doc.page_content.strip()

# Truncate content for the card if it's too long
if len(content_preview) > 300:
    content_preview = content_preview[:300] + "..."


# 4. Construct Feishu Rich Text Card (Message Card)
card_content = {
    "config": {
        "wide_screen_mode": True
    },
    "header": {
        "template": "blue",
        "title": {
            "content": "🌅 星佳的数字大脑：今日金句推送",
            "tag": "plain_text"
        }
    },
    "elements": [
        {
            "tag": "div",
            "text": {
                "content": f"**今日主题**：{selected_theme}\n**出自文章**：《{source_file}》\n\n\n**当年你是这么写的：**\n\n*{content_preview}*",
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
                    "content": "✨ 保持专注，拒绝内卷。新的一天，破局而生。",
                    "tag": "lark_md"
                }
            ]
        }
    ]
}

# 5. Send Proactive Message
print(f"准备向用户 {TARGET_USER_ID} 发送飞书卡片...")
# Notice: In a real scenario, you need the actual open_id, user_id, or email of the recipient.
# For testing, we will ask the user how they want to specify themselves.
request = CreateMessageRequest.builder() \
    .receive_id_type("open_id") \
    .request_body(CreateMessageRequestBody.builder()
        .receive_id(TARGET_USER_ID)
        .msg_type("interactive")
        .content(json.dumps(card_content))
        .build()) \
    .build()

response = lark_client.im.v1.message.create(request)

if response.success():
    print("✅ 推送成功！")
else:
    print(f"❌ 推送失败: {response.code}, {response.msg}")
