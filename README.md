<p align="center">
  <img src="docs/images/main_dashboard.png" width="700" alt="My Digital Mentor Dashboard"/>
</p>

<h1 align="center">🌌 My Digital Mentor · 我的数字导师</h1>

<p align="center">
  <b>基于本地知识库 (RAG) + Google Gemini 大模型的全能个人数字生态系统</b><br/>
  <i>Your Personal AI Ecosystem Powered by RAG + Google Gemini</i>
</p>

<p align="center">
  <a href="#-快速上手"><img src="https://img.shields.io/badge/快速上手-00C853?style=for-the-badge&logo=rocket&logoColor=white" alt="Quick Start"/></a>
  <a href="#-八大核心功能"><img src="https://img.shields.io/badge/功能预览-2979FF?style=for-the-badge&logo=eye&logoColor=white" alt="Features"/></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/English-FF6F00?style=for-the-badge&logo=translate&logoColor=white" alt="English Version"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat-square&logo=google&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/ChromaDB-FF6F00?style=flat-square&logo=databricks&logoColor=white" alt="ChromaDB"/>
  <img src="https://img.shields.io/badge/LangChain-000000?style=flat-square&logo=chainlink&logoColor=white" alt="LangChain"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
</p>

---

## 💡 这是什么？

这不是一个普通的 ChatGPT 套壳。  
这是一套能**完美复活你思想脉络**的 AI 全栈系统 —— 你的数字灵魂分身。

通过将你自己的文章、日记、研究笔记（5000 篇以上）喂给系统，它会自动建立一个属于你的"第二大脑"（近 30,000 个知识切片），并为你提供 **8 大超级 AI 能力**。

> *"把过去十二年写过的上千篇公众号文章全部灌进 AI 的大脑，让它学会用你的口吻说话、写作、思辨、出书、甚至帮你录播客。"*

### 🎯 核心价值

| 痛点 | My Digital Mentor 的解法 |
|------|------------------------|
| 🔍 写过的好文章自己都找不到了 | AI 帮你从 3 万个碎片中精准召回 |
| ✍️ 想写文章但没灵感、没时间 | 替身写作，完美模仿你的笔触秒出千字稿 |
| 🐦 想发推特但组织不好语言 | 一键生成中英双语爆款推文 + 配图提示词 |
| 📊 想看看自己这些年到底在想什么 | 自动生成思想图谱，可视化你的认知地图 |
| 📚 想出一本书但无从下手 | 基于历史文章自动生成书稿大纲和章节内容 |
| 🧠 做重要决策时想找个靠谱的对手 | 认知对抗教练用你自己的话反驳你 |
| 🎙️ 想做播客但不会写脚本 | AI 一键生成 Host/Guest 对谈剧本 |
| 📈 想看自己某个话题的思想是怎么进化的 | 时光机按年份分析你的认知演变轨迹 |

---

## 🆕 最新更新

### **v2.0.0** (2026-03-02) · 重大版本更新 🎉

**🌟 新增四大超级功能**
- **🕰️ 思想时光机 (Time Machine)**：输入任何主题，AI 从你不同年代的文章中分析你思想的演化脉络
- **� 个人数字出版局 (Auto-Publisher)**：一键从你的知识库中生成书稿大纲与章节内容
- **⚔️ 认知对抗教练 (Cognitive Challenger)**：AI 化身魔鬼教练，用你过去的文字反驳你的冲动决定
- **🎙️ AI 播客生成器 (Podcast Generator)**：基于知识库自动生成 Host/嘉宾 对谈式播客脚本

**🛡️ 工程级稳健性增强**
- 全局 API 调用自动重试机制（指数退避 × 3 次重试），彻底解决代理/VPN 环境下的 SSL/DNS 闪断
- Mermaid 图谱渲染引擎重构，暴力剥离 LLM 输出中的非法字符，图谱渲染成功率提升至 100%
- 手机端 Session State 安全降级，彻底解决移动端 Safari 重载报错

---

## �️ 八大核心功能

### 🧠 1. 灵魂导师 (AI Mentor)

随时找它倾诉困惑。它不仅会回答，还会巧妙地引用**你过去写过的金句和段落**来开导你。附带可选的语音播报功能（TTS）。

> 不是在跟一个陌生的 AI 聊天，而是在跟「最了解你的自己」对话。

<p align="center">
  <img src="docs/images/chat_mentor_response.png" width="700" alt="AI Mentor Response"/>
</p>

---

### ✍️ 2. 替身写作 (AI Writer)

完全模仿"你的笔触"瞬间出稿千字长文。系统会从你的知识库中检索相关历史文章，深度学习你的风格后进行高质量原创写作。

<p align="center">
  <img src="docs/images/ai_writer.png" width="700" alt="AI Writer"/>
</p>

---

### 🤔 3. 思想图谱 (Knowledge Graph)

自动从你近 3 万个知识切片中随机抽取 200 个片段，提炼并可视化你的核心理念网络，生成极具社交传播力的高颜值思维导图。支持一键导出 3 倍高清 PNG。

<p align="center">
  <img src="docs/images/knowledge_graph.png" width="700" alt="Knowledge Graph"/>
</p>

---

### 🐦 4. 推特分发机 (Twitter Agent)

从你的潜意识碎片库里随机打捞灵感，重写为极具穿透力的双语推文（中英对照），并附带 AI 配图 Prompt，一键喂给 Midjourney 就能出图。

<p align="center">
  <img src="docs/images/twitter_agent.png" width="700" alt="Twitter Agent"/>
</p>

---

### 🕰️ 5. 思想时光机 (Time Machine) `NEW`

输入任何一个主题（如"投资"、"创业"、"家庭"），系统会跨年代检索你的历史文章，让 AI 按时间线分析你在这个话题上的**认知演化轨迹** —— 从最初的幼稚想法到最终的深度洞察。

> 送你一份专属的「思想编年史」。

<p align="center">
  <img src="docs/images/time_machine.png" width="700" alt="Time Machine"/>
</p>

---

### 📚 6. 个人数字出版局 (Auto-Publisher) `NEW`

给一个主题，AI 自动从你的知识库中翻箱倒柜，生成一本只属于你的**书稿大纲和章节初稿**。所有内容都严格基于你的历史写作，保留你的原汁原味。

---

### ⚔️ 7. 认知对抗教练 (Cognitive Challenger) `NEW`

AI 化身硬核魔鬼教练。当你冲动想做什么重大决定时，它会翻遍你的历史文章，用**你自己说过的话来反驳你**，发出直击灵魂的三连质问。

> *"你上次创业的'尸体'还没凉透，这次的'新欢'凭什么就能活下来？"*

<p align="center">
  <img src="docs/images/cognitive_challenger.png" width="700" alt="Cognitive Challenger"/>
</p>

---

### 🎙️ 8. AI 播客生成器 (Podcast Generator) `NEW`

输入一个话题，AI 自动生成一期完整的**双人播客对谈脚本**（Host/嘉宾格式），包含时间戳、音效提示、金句萃取，拿去直接录制即可。

<p align="center">
  <img src="docs/images/podcast_generator.png" width="700" alt="Podcast Generator"/>
</p>

---

## 🚀 快速上手

### 1️⃣ 环境准备

> ⚠️ **前置要求**：请确保你的电脑已安装 [Python 3.10+](https://www.python.org/downloads/) 和 [Git](https://git-scm.com/downloads)。

```bash
# 克隆项目到本地
git clone https://github.com/xingjia10086/My-Digital-Mentor.git
cd My-Digital-Mentor

# 安装所有依赖（一键搞定）
pip install -r requirements.txt
```

### 2️⃣ 配置 API 密钥（⭐ 最关键的一步）

```bash
# Mac / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

用任何文本编辑器打开 `.env` 文件，按下表填入你的密钥：

| 变量名 | 是否必填 | 用途 | 获取方式 |
|---|:---:|---|---|
| `GOOGLE_API_KEY` | ✅ 必填 | 驱动 AI 对话与写作 | [Google AI Studio](https://aistudio.google.com/app/apikey)（免费） |
| `GCP_PROJECT_ID` | ✅ 必填 | 文本向量化服务 | [Google Cloud Console](https://console.cloud.google.com/) |
| `APP_PASSWORD` | ✅ 必填 | Web 界面登录密码 | 自己随便设一个即可 |
| `FEISHU_APP_ID` / `SECRET` | ❌ 可选 | 飞书推送 | [飞书开放平台](https://open.feishu.cn/) |
| `TWITTER_API_KEY` 等 | ❌ 可选 | 推特自动发布 | [Twitter Developer](https://developer.twitter.com/) |

> 💡 **小白提示**：如果只想体验核心功能，只需要填前三项！

### 3️⃣ 构建你的 AI 大脑

将你的文章（`.txt`、`.md` 格式）放入 `公众号/` 或 `gongzhonghao/` 文件夹，然后运行：

```bash
python rag_ingest.py
```

> 这会自动将文本切割、向量化，并存储在本地 `chroma_db/` 中。以后新增文章只需重新运行即可增量更新。

### 4️⃣ 启动系统 🎉

```bash
streamlit run web_ui.py
```

打开 `http://localhost:8501`，输入你设置的密码，开始享受你的数字生态！

### 5️⃣ 手机访问（可选）

想在手机上随时随地使用？推荐安装 [Tailscale](https://tailscale.com/)（免费），在所有设备上登录同一账号后，手机浏览器访问 `http://你的Mac-Tailscale-IP:8501` 即可。用 Safari 的"添加到主屏幕"功能可以把它变成一个全屏 APP。

---

## 📁 项目结构

```
My-Digital-Mentor/
├── web_ui.py              # 🌐 主系统 Web 界面（Streamlit，8 大功能）
├── rag_ingest.py          # 📥 知识库构建脚本（支持增量更新）
├── run_tests.py           # 🧪 自动化测试脚本
├── daily_push.py          # 📤 飞书每日金句推送（定时服务）
├── feishu_bot.py          # 🤖 飞书智能新闻播报机器人
├── twitter_auto_agent.py  # 🐦 推特自动发布代理
├── .env.example           # 🔑 环境变量模板
├── requirements.txt       # 📦 依赖清单
├── docs/images/           # 📸 功能截图
├── 公众号/                # 📚 文章数据（可替换为你自己的内容）
└── chroma_db/             # � 向量知识库（自动生成）
```

---

## 🔧 技术架构

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Streamlit  │────▶│  LangChain   │────▶│  ChromaDB    │
│   Web UI     │     │  RAG Engine  │     │  Vector Store│
│  (8 Modules) │     │  (Retrieval) │     │  (30K Chunks)│
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │
       ▼                    ▼
┌──────────────┐     ┌──────────────┐
│ Google Gemini│     │   Embeddings │
│   2.5 Pro    │     │ gemini-001   │
│ (Generation) │     │ (Vectorize)  │
└──────────────┘     └──────────────┘
```

---

## ⚠️ 安全声明

- 🔒 所有敏感配置均通过 `.env` 文件管理，**绝不会被 Git 跟踪**
- 🛡️ `.gitignore` 已严格配置，自动拦截 `.env`、`chroma_db/`、VPN 配置等敏感文件
- ⚡ 系统内置了 API Key 泄露自救面板：即使密钥失效，也不会崩溃
- 🔄 所有网络调用均内置自动重试机制，抗 VPN/代理环境下的网络抖动

> **⚠️ 重要提醒：绝对不要将你的 `.env` 文件推送到任何公开仓库！**

---

## �🤝 开源协议

MIT License · 欢迎 Star ⭐ · 欢迎 Fork 🍴 · 欢迎 PR 🎉

*Powered by Google Gemini 2.5 Pro · LangChain · ChromaDB · Streamlit*
