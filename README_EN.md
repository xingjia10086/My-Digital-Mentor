<p align="center">
  <img src="docs/images/ai_mentor.png" width="600" alt="AI Mentor Preview"/>
</p>

<h1 align="center">🌌 My Digital Mentor</h1>

<p align="center">
  <b>Your Personal AI Ecosystem & Thought Inheritance Engine Powered by RAG + Google Gemini</b>
</p>

<p align="center">
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick_Start-00C853?style=for-the-badge&logo=rocket&logoColor=white" alt="Quick Start"/></a>
  <a href="#-core-features"><img src="https://img.shields.io/badge/Features-2979FF?style=for-the-badge&logo=eye&logoColor=white" alt="Features"/></a>
  <a href="README.md"><img src="https://img.shields.io/badge/中文版-FF6F00?style=for-the-badge&logo=translate&logoColor=white" alt="Chinese Version"/></a>
</p>

---

## 💡 Why Do You Need It?

This is not just another wrapper for a chatbot. It is a full-stack AI ecosystem capable of **perfectly reviving and inheriting your train of thought**.

By feeding your own articles, diaries, and research notes into the system, it automatically builds your "Second Brain". It then acts as your 24/7 virtual mentor, automated tweeting agent, thought graph extractor, and an emotionally impactful Time Machine to review your memories.

> *"Feed thousands of articles you wrote over the past decade into the AI's brain, teaching it to speak in your tone, write like you, and even generate your annual memoir." —— 星佳的数字生态*

---

## 🆕 Recent Updates (v1.1)

- **[NEW] ⏳ Time Machine Released**: Supports extracting your memory fragments from the past 10 years (2014-2026), letting AI automatically generate your thrilling **"Decade of Thought Evolution Memoir"**.
- **[NEW] 🔥 High-End Social Poster Engine**: Whether it's a knowledge graph or a Time Machine memory, it now renders **3x High-Res social posters** directly in the frontend, complete with dark gradient backgrounds and geeky watermarks for easy sharing to X (Twitter) or WeChat moments.
- **[FIX] Model Failover Protection**: Comprehensively optimized the backend Gemini model dispatch logic, seamlessly switching to the latest APIs to guarantee system stability (fallback from locked `gemini-2.0-flash` to `gemini-2.5-pro`).

---

## 🎯 Core Features

### ⏳ Time Machine & Annual Memoir
Accurately salvage specific memory fragments from your decade-long knowledge base! The AI acts as your private biographer, using stark contrasts (*"You Then vs. You Now"*) to connect your major decisions and mindset shifts, picking out a **Four-Word Annual Theme** and the most **piercing golden quotes**. Finally, generate a visually striking social sharing poster with one click.

<p align="center">
  <b>👇 [Insert New Time Machine Poster Screenshot Here] 👇</b>
  <br>
  <img src="docs/images/time_machine_placeholder.png" width="700" alt="Time Machine Poster Placeholder"/>
  <br>
  <i>(Recommendation: Upload a Time Machine golden quote poster with a gradient background here)</i>
</p>

---

### 🤔 Thought Evolution Graph (Knowledge Graph)
No more linear reading! The system automatically samples materials from your historical article base, extracts the interconnected models of your core concepts, and draws a massive mind map for you via Mermaid frontend. Click download to get a perfect, high-res knowledge graph.

<p align="center">
  <img src="docs/images/knowledge_graph.png" width="700" alt="Knowledge Graph"/>
</p>

---

### 🧠 AI Mentor
Consult "yourself" whenever you're confused. It won't just answer; it will cleverly quote real experiences and insights you wrote over the past 10 years to enlighten you, granting you an epiphany across time (with real-time optional Azure Text-to-Speech).

<p align="center">
  <img src="docs/images/ai_mentor.png" width="700" alt="AI Mentor"/>
</p>

---

### ✍️ AI Writer & 🐦 Twitter Agent
Instantly draft 1000-word articles perfectly imitating "your penmanship", or distill your subconscious musings into penetrating bilingual short tweets (English-Chinese parallel), complete with perfect Midjourney AI illustration Prompts at the end!

<p align="center">
  <img src="docs/images/twitter_agent.png" width="700" alt="Twitter Agent"/>
</p>

---

## 🚀 Quick Start (Local Deployment)

### 1️⃣ Environment Preparation

> ⚠️ **Prerequisites**: Ensure you have [Python 3.10+](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) installed.

Open your terminal (PowerShell for Windows / Terminal for Mac) and run:

```bash
# Clone the project locally
git clone https://github.com/xingjia10086/My-Digital-Mentor.git
cd My-Digital-Mentor

# Install all dependencies
pip install -r requirements.txt
```

### 2️⃣ Soul Injection: API Key Configuration

First, copy the environment variable template:

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Open `.env` with a text editor and fill in your **two core keys**:

| Variable | Required | Purpose | How to get |
|---|:---:|---|---|
| `GOOGLE_API_KEY` | ✅ Yes | Drives the LLM ecosystem | Claim for free on [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `GCP_PROJECT_ID` | ✅ Yes | Used by Vertex AI for embeddings | Copy any project ID from [Google Cloud Console](https://console.cloud.google.com/) |
| `APP_PASSWORD` | ✅ Yes | Web UI access password | Set anything (e.g., `123456`) to protect your data |

### 3️⃣ Train Your "Second Brain"

Drop your article data (`.txt`, `.md`, categorized by year if possible) into the `gongzhonghao/` directory.

Then, execute this command once to ingest knowledge (supports seamless incremental scans, no repetitive calculation):

```bash
python rag_ingest.py
```
*(Thousands of articles will be chunked, vectorized via ChromaDB, and saved locally within minutes)*

### 4️⃣ Launch Web Dashboard 🎉

All set! Just run:

```bash
streamlit run web_ui.py
```
Open your browser at `http://localhost:8501` to enjoy your private AI matrix!

---

## 📁 Core Architecture

```
My-Digital-Mentor/
├── web_ui.py              # 🌌 [Core entry] Houses interaction logic for all 4 modules & poster rendering
├── rag_ingest.py          # 📥 [Incremental engine] Rapidly builds local vector database
├── test_system.py         # 🔍 [Debug probe] Auto-tests system environment and API connectivity
├── chroma_db/             # 🧠 (System-generated) Your native vector memory palace
├── .env.example           # 🔑 Environment config template
└── gongzhonghao/          # 📚 Local textual data pool
```

## ⚠️ Security & Privacy Statement
- 🛡️ **Absolute Localization**: Uses local ChromaDB. Apart from the unavoidable LLM generation API calls, your original articles and private data are NEVER uploaded to public cloud storage.
- 🤫 **Anti-leak Mechanism**: Incorporates strict `.gitignore` rules to block `.env` and `chroma_db/` directories from accidental GitHub uploads.

---
*Created by [星佳的数字生态](https://github.com/xingjia10086)*
