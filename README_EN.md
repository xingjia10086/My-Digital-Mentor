<p align="center">
  <img src="docs/images/ai_mentor.png" width="600" alt="AI Mentor Preview"/>
</p>

<h1 align="center">🌌 My Digital Mentor</h1>

<p align="center">
  <b>A Full-Stack Personal AI Ecosystem Powered by Local RAG + Google Gemini</b>
</p>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/中文文档-E53935?style=for-the-badge&logo=translate&logoColor=white" alt="Chinese Version"/></a>
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick%20Start-00C853?style=for-the-badge&logo=rocket&logoColor=white" alt="Quick Start"/></a>
</p>

---

## 💡 What Is This?

This is a full-stack AI system that **perfectly revives your thinking patterns**.

By feeding the system your own articles, journals, or research notes, it builds a "Second Brain" that belongs to you — providing a 24/7 virtual mentor, automatic tweet generation, and powerful knowledge graph extraction.

> *"Pour thousands of your past articles into AI's brain and let it learn to speak, write, and even tweet in your own voice."*

---

## 🆕 Recent Updates

**v1.1.0** (2026-03)
- **Knowledge Graph Export Fix**: Completely fixed the bug where special symbols caused Mermaid rendering to crash.
- **High-Res Graph Download**: You can now export and download the generated Knowledge Graph as a 3x High-Res PNG image with a premium dark gradient background, perfect for sharing on social platforms.

---

## 🎯 Feature Showcase

### 🧠 AI Mentor (Soul Counselor)
Confide your troubles anytime. It responds with wisdom by cleverly referencing golden lines and paragraphs from your own past writings, with optional text-to-speech.

<p align="center">
  <img src="docs/images/ai_mentor.png" width="700" alt="AI Mentor"/>
</p>

---

### ✍️ AI Writer (Ghost Writer)
Generates 1500+ word long-form articles that perfectly mimic **your writing style**. The system retrieves relevant historical articles from your knowledge base and deeply learns your voice before creating original content.

<p align="center">
  <img src="docs/images/ai_writer.png" width="700" alt="AI Writer"/>
</p>

---

### 🤔 Knowledge Graph
Automatically samples from your article archive to extract and visualize your core belief network as a stunning, shareable mind map.

<p align="center">
  <img src="docs/images/knowledge_graph.png" width="700" alt="Knowledge Graph"/>
</p>

---

### 🐦 Twitter Agent
Randomly digs up gems from your subconscious fragment library, rewrites them as compelling bilingual tweets (Chinese + English), with an AI image prompt attached.

<p align="center">
  <img src="docs/images/twitter_agent.png" width="700" alt="Twitter Agent"/>
</p>

---

## 🚀 Quick Start

### 1️⃣ Prerequisites
Make sure you have **Python 3.10+** installed. Then:

```bash
git clone https://github.com/xingjia10086/My-Digital-Mentor.git
cd My-Digital-Mentor
pip install -r requirements.txt
```

### 2️⃣ Configure API Keys

Find `.env.example` in the project root, **copy and rename it to `.env`**, then fill in your keys:

| Variable | Purpose | How to Get |
|---|---|---|
| `GOOGLE_API_KEY` | 🧠 Core AI Engine | [Google AI Studio](https://aistudio.google.com/app/apikey) (Free) |
| `GCP_PROJECT_ID` | Vector Embedding Service | [Google Cloud Console](https://console.cloud.google.com/) |
| `APP_PASSWORD` | Login Password | Set any password you like |
| `FEISHU_APP_ID` / `SECRET` | Feishu Push (Optional) | [Feishu Open Platform](https://open.feishu.cn/) |
| `TWITTER_API_KEY` etc. | Auto Tweet (Optional) | [Twitter Developer](https://developer.twitter.com/) |

> 💡 **Minimum Requirement**: Only `GOOGLE_API_KEY` and `GCP_PROJECT_ID` are needed to run AI Mentor, Writer, and Knowledge Graph.

### 3️⃣ Build Your AI Brain

Place your articles (`.txt`, `.md` format) into the `公众号/` or `gongzhonghao/` folder, then run:

```bash
python rag_ingest.py
```

### 4️⃣ Launch

```bash
streamlit run web_ui.py
```

Open `http://localhost:8501` in your browser and start enjoying your personal digital ecosystem!

---

## 📁 Project Structure

```
My-Digital-Mentor/
├── web_ui.py              # 🌐 Main Web UI (Streamlit)
├── rag_ingest.py          # 📥 Knowledge Base Builder
├── daily_push.py          # 📤 Scheduled Feishu Quote Push
├── feishu_bot.py          # 🤖 Feishu Smart News Bot
├── twitter_auto_agent.py  # 🐦 Automated Twitter Publisher
├── .env.example           # 🔑 Environment Variables Template
├── requirements.txt       # 📦 Dependencies
├── 公众号/                # 📚 Sample Article Data
└── gongzhonghao/          # 📚 More Sample Articles
```

---

## ⚠️ Security

- 🔒 All secrets managed via `.env` — **never tracked by Git**
- 🛡️ Robust `.gitignore` blocks `.env`, `chroma_db/`, and other sensitive files
- ⚡ Built-in API Key recovery panel: graceful error handling instead of crashes

> **⚠️ NEVER push your `.env` file to any public repository!**

---

## 🤝 License

MIT License · Star ⭐ · Fork 🍴 · PRs Welcome 🎉

*Powered by Google Gemini & LangChain & ChromaDB*
