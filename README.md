<p align="center">
  <img src="docs/images/ai_mentor.png" width="600" alt="AI Mentor Preview"/>
</p>

<h1 align="center">🌌 My Digital Mentor · 我的数字导师</h1>

<p align="center">
  <b>基于本地知识库 (RAG) + Google Gemini 的个人数字生态系统与思想传承引擎</b><br/>
  <i>Your Personal AI Ecosystem Powered by RAG + Google Gemini</i>
</p>

<p align="center">
  <a href="#-快速上手"><img src="https://img.shields.io/badge/快速上手-00C853?style=for-the-badge&logo=rocket&logoColor=white" alt="Quick Start"/></a>
  <a href="#-核心功能"><img src="https://img.shields.io/badge/功能预览-2979FF?style=for-the-badge&logo=eye&logoColor=white" alt="Features"/></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/English-FF6F00?style=for-the-badge&logo=translate&logoColor=white" alt="English Version"/></a>
</p>

---

## 💡 为什么需要它？

这绝不只是一个套壳的聊天机器人，这是一套能**完美复活并传承你思想脉络**的 AI 全栈系统。

通过将你自己的文章、日记、研究笔记喂给系统，它会自动建立一个属于你的"第二大脑"，进而为你提供全天候的虚拟导师、自动发推代理、思想图谱提取、以及极具情感震撼的时光机回忆功能。

> *"把过去十年写过的上千篇公众号文章全部灌进 AI 的大脑，让它学会用你的口吻说话、写作、甚至生成年度回忆传记。" —— 星佳的数字生态*

---

## 🆕 最新更新 (Recent Updates: v1.1)

- **[NEW] ⏳ 时光机 (Time Machine) 上线**：支持提取你过去 10 年（从 2014 到 2026）的思考碎片，由 AI 自动生成跌宕起伏的**《十年思想演化传记》**。
- **[NEW] 🔥 高逼格社交海报生成引擎**：无论是知识图谱还是时光机回忆，现在都支持在前端直接渲染生成带有年度金句、暗黑渐变背景和极客水印的 **3倍超清（3x High-Res）长图海报**，一键下载，制霸朋友圈和 X (Twitter)。
- **[FIX] 模型容灾守护**：全面优化了后端 Gemini 模型的调度逻辑，无缝切换最新 API，保证系统稳定运行。

---

## 🎯 核心功能

### ⏳ 时光机与年度传记 (Time Machine)
从你长达十年的知识库中，精准打捞特定年份的记忆碎片！AI 将化身为你的私人传记作者，用极其强烈的反差（*“当年的你 vs 现在的你”*）串联起重大决定、心境转变，并为你精选出**年度四个字主题**与**最扎心金句**。最后，一键为您生成极具视觉冲击力的社交分享长图。

<p align="center">
  <b>👇 [此处在此上传时光机海报的新截图] 👇</b>
  <br>
  <img src="docs/images/time_machine_placeholder.png" width="700" alt="Time Machine Poster Placeholder"/>
  <br>
  <i>(建议上传一张带渐变背景的时光机金句海报在此)</i>
</p>

---

### 🤔 思想演化图谱 (Knowledge Graph)
不再是线性的文字阅读！系统自动从你的历史文章库中随机抽取素材，提炼核心理念的相互关联模型，并利用 Mermaid 前端为你绘制庞大的思维导图。点击下载，即可获得一张完美的高清白底知识图谱。

<p align="center">
  <img src="docs/images/knowledge_graph.png" width="700" alt="Knowledge Graph"/>
</p>

---

### � 灵魂导师 (AI Mentor)
随时找“你自己”倾诉困惑。它不仅会回答，还会巧妙地引用你过去 10 年写过真实经历与心得来开导你，让你获得穿越时空的顿悟（附带实时可选的 Azure 语音播报功能）。

<p align="center">
  <img src="docs/images/ai_mentor.png" width="700" alt="AI Mentor"/>
</p>

---

### ✍️ 替身写作 & 🐦 推特分发机
完全模仿"你的笔触"瞬间出稿千字长文，或者将你的沉思潜意识提炼成极具穿透力的双语短推文（中英对照），并在末尾为你附带完美的 Midjourney AI 配图 Prompt！

<p align="center">
  <img src="docs/images/twitter_agent.png" width="700" alt="Twitter Agent"/>
</p>

---

## 🚀 极速本地部署

### 1️⃣ 环境准备

> ⚠️ **前置要求**：请确保你的电脑已安装 [Python 3.10+](https://www.python.org/downloads/) 和 [Git](https://git-scm.com/downloads)。

打开终端（Windows: PowerShell / Mac: Terminal），依次执行：

```bash
# 克隆项目到本地
git clone https://github.com/xingjia10086/My-Digital-Mentor.git
cd My-Digital-Mentor

# 安装所有依赖（一键搞定）
pip install -r requirements.txt
```

### 2️⃣ 灵魂注入：一键配置 API 密钥

先复制一份环境变量文件：

```bash
# Windows 用户
copy .env.example .env

# Mac / Linux 用户
cp .env.example .env
```

用文本编辑器打开 `.env` 文件，填入你的**两把核心钥匙**：

| 变量名 | 是否必填 | 用途 | 获取方式 |
|---|:---:|---|---|
| `GOOGLE_API_KEY` | ✅ 必填 | 驱动整个生态的大脑 (LLM) | 在 [Google AI Studio](https://aistudio.google.com/app/apikey) 免费申请 |
| `GCP_PROJECT_ID` | ✅ 必填 | 连接 Vertex AI 生成向量 | 在 [Google Cloud Console](https://console.cloud.google.com/) 复制任意项目的 ID |
| `APP_PASSWORD` | ✅ 必填 | Web 界面的访问密码 | 随便设一个（比如 `123456`）保护你的数据 |

*(其他如飞书或推测的 Key 如不使用相关功能，直接为空即可。)*

### 3️⃣ 训练你的“第二大脑”

将你的文章数据（支持 `.txt`, `.md`，建议按年份建立文件夹分类）直接扔进项目里的 `公众号/` (或 `gongzhonghao/`) 文件夹。

随后只需执行一次该命令进行知识入库（支持无缝增量扫描，绝不重复计算）：

```bash
python rag_ingest.py
```
*(几千篇文章将在几分钟内被切分、转化为 ChromaDB 向量特征并永久保存在本地)*

### 4️⃣ 启动 Web 生态面板 🎉

一切就绪，只需要运行：

```bash
streamlit run web_ui.py
```
打开浏览器访问 `http://localhost:8501`，享受你的私人 AI 矩阵吧！

---

## 📁 核心架构

```
My-Digital-Mentor/
## 🤝 开源协议

MIT License · 欢迎 Star ⭐ · 欢迎 Fork 🍴 · 欢迎 PR 🎉

*Powered by Google Gemini & LangChain & ChromaDB*
