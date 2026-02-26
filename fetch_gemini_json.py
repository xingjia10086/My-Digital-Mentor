import os
import json
import time
import google.generativeai as genai

API_KEY = "AIzaSyDuVkQKk3GH6MjS-bzIQgVkhSZ-utvwUBg"
PHOTO_DIR = r"D:\GPT\AI-demo\Buddhism-Photos"
genai.configure(api_key=API_KEY)

MASTER_PROMPT = """
你是一位顶尖的藏传佛教艺术专家和资深学术汇报顾问。
我为你上传了数十张关于佛教艺术、寺庙建筑、壁画和相关调研的照片。
【重要警告：你必须严格使用这些照片原始的文件名，绝对不能自己编造类似 image_1.jpg 这样的假名字。我会把所有合法的文件名列表附在最后。】

请你【全局同时分析】这些照片，提取出最重要的文化精神、建筑特色和信仰具象，为我生成一份可以直接用来给导师汇报的精美 PPT 结构。

请务必返回一个合法的 JSON 数组，格式如下：
[
  {
    "type": "cover",
    "title": "（主标题）",
    "subtitle": "（副标题）",
    "meta": "（汇报人）",
    "image": "（必须从我提供的合法文件名列表中挑选1张真实存在的原始文件名，连同后缀名一起输出）"
  },
  {
    "type": "toc",
    "title": "研究框架",
    "items": ["一", "二", "三"]
  },
  {
    "type": "section",
    "title": "壹",
    "subtitle": "（章节标题）"
  },
  {
    "type": "content",
    "title": "（本页核心结论）",
    "bullets": ["要点1", "要点2", "要点3"],
    "image": "（必须从我提供的合法文件名列表中挑选1张真实存在的原始文件名）"
  },
  {
    "type": "ending",
    "title": "感谢聆听",
    "subtitle": "敬请导师批评指正",
    "image": "（挑选1张真实存在的原始文件名）"
  }
]

要求：
1. 深入挖掘照片中的颜色（红、黄等）、建筑形制、符号等深层含义。
2. 最少生成 10 页，最多 15 页。
3. 返回的结果必须是纯 JSON，不要有任何 Markdown 语法如 ```json。
4. 【致命要求】：JSON中的所填写的 `image` 字段的值必须100%存在于我最后提供的文件名列表里，否则程序会崩溃！
"""

files = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
existing_files = {f.display_name: f for f in genai.list_files()}

uploaded_files = []
for filename in files:
    if filename in existing_files:
        uploaded_files.append(existing_files[filename])

print(f"Re-using {len(uploaded_files)} files from Gemini...")

print("\nCalling Gemini 3.1 Pro Preview...")
model = genai.GenerativeModel('models/gemini-3.1-pro-preview')
filenames_str = "合法的文件名列表如下：\n" + "\n".join(files)
final_prompt = MASTER_PROMPT + "\n\n" + filenames_str
payload = [final_prompt] + uploaded_files

response = model.generate_content(payload, generation_config={"temperature": 0.2})

text = response.text.strip()
if text.startswith("```json"): text = text[7:]
if text.endswith("```"): text = text[:-3]

with open('slides.json', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved to slides.json!")
