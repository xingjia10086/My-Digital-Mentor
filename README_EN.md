<p align="center">
  <img src="docs/images/main_dashboard.png" width="860" alt="My Digital Mentor main dashboard"/>
</p>

<h1 align="center">My Digital Mentor</h1>

<p align="center">
  <b>Turn your past writing, notes, journals, and ideas into an AI that sounds more like you.</b>
</p>

<p align="center">
  A personal AI system built on your own knowledge base, not generic internet fluff.
</p>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/中文文档-E53935?style=for-the-badge&logo=translate&logoColor=white" alt="Chinese Version"/></a>
  <a href="#-quick-start-in-10-minutes"><img src="https://img.shields.io/badge/Quick%20Start-00C853?style=for-the-badge&logo=rocket&logoColor=white" alt="Quick Start"/></a>
  <a href="#-what-you-can-actually-do-with-it"><img src="https://img.shields.io/badge/Feature%20Tour-2979FF?style=for-the-badge&logo=grid&logoColor=white" alt="Feature Tour"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat-square&logo=google&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/RAG-Personal%20Knowledge%20Base-111111?style=flat-square" alt="RAG"/>
  <img src="https://img.shields.io/badge/ChromaDB-FF6F00?style=flat-square&logo=databricks&logoColor=white" alt="ChromaDB"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
</p>

---

## Why this project is different

Most AI products try to answer:

> "Can AI become smarter?"

This project asks a more personal question:

> "Can AI become more like me?"

My Digital Mentor is not another chatbot wrapper.  
It is a local RAG-powered personal AI system that uses your own writing as the source of truth.

That means it can:

- retrieve your old ideas when you forgot where you wrote them
- answer with context grounded in your past writing
- draft new articles in a style closer to your voice
- map your thinking across years
- challenge your decisions using your own previous arguments
- turn your archive into a book outline, tweet engine, or podcast script

If you have years of accumulated content, this project turns that archive into leverage.

---

## What it feels like to use

The experience is not "ChatGPT, but with a custom prompt."

It feels more like:

- talking to a version of yourself that remembers far more than you do
- writing with an assistant that can actually pull from your old articles
- reviewing your intellectual history instead of just searching files
- building a second brain that is queryable, generative, and reusable

The key idea is simple:

> **The raw material is not the internet. It is you.**

---

## Built for creators, thinkers, and knowledge workers

This repo is especially useful if you are:

- a writer, blogger, newsletter author, or public thinker
- a founder, operator, investor, or researcher
- someone with years of journals, markdown notes, or article archives
- interested in PKM, second-brain systems, AI clones, or personal RAG workflows

If you have no real archive, the value is limited.  
If you have years of content, the value compounds fast.

---

## Visual Tour

### Main Dashboard

<p align="center">
  <img src="docs/images/main_dashboard.png" width="860" alt="Main dashboard"/>
</p>

### Mentor Conversation Experience

<p align="center">
  <img src="docs/images/chat_mentor_response.png" width="820" alt="AI mentor conversation"/>
</p>

### Writing Assistant

<p align="center">
  <img src="docs/images/ai_writer.png" width="820" alt="AI writer interface"/>
</p>

### Knowledge Graph

<p align="center">
  <img src="docs/images/knowledge_graph.png" width="820" alt="Knowledge graph"/>
</p>

### Time Machine

<p align="center">
  <img src="docs/images/time_machine.png" width="820" alt="Time machine"/>
</p>

### Cognitive Challenger

<p align="center">
  <img src="docs/images/cognitive_challenger.png" width="820" alt="Cognitive challenger"/>
</p>

### Podcast Generator

<p align="center">
  <img src="docs/images/podcast_generator.png" width="820" alt="Podcast generator"/>
</p>

### Twitter Agent

<p align="center">
  <img src="docs/images/twitter_agent.png" width="820" alt="Twitter agent"/>
</p>

---

## What you can actually do with it

The current app includes 8 core modules.

### 1. AI Mentor

Ask for advice, emotional reflection, or perspective.  
The system retrieves relevant fragments from your archive and responds with context grounded in your own past words.

This is where the product feels most uncanny:  
it can comfort you with ideas you once wrote but forgot.

### 2. AI Writer

Generate long-form drafts based on themes from your archive.  
Instead of generic content generation, it tries to continue your thinking and your tone.

Useful for:

- newsletters
- essays
- blog posts
- scripts
- speech drafts

### 3. Knowledge Graph

Sample your knowledge base, extract recurring concepts, and turn them into a visual map of your worldview.

Useful for:

- annual reviews
- personal branding
- intellectual self-audits
- social sharing

### 4. Twitter Agent

Surface old ideas from your archive and rewrite them into short-form, shareable bilingual posts with image prompts.

Useful for:

- content repurposing
- global audience experiments
- social media cadence

### 5. Time Machine

Enter a topic and trace how your thinking evolved over the years.

Useful for:

- intellectual retrospectives
- book research
- topic evolution reports
- public essays about how your views changed

### 6. Auto-Publisher

Generate a book outline and chapter draft structure from your archive.

Useful for:

- turning an article archive into a book project
- finding the hidden structure in years of scattered writing

### 7. Cognitive Challenger

Ask the AI to challenge your current decision using your own previous writing as ammunition.

Useful for:

- startup decisions
- career shifts
- investment reflection
- major life tradeoffs

### 8. Podcast Generator

Turn your ideas into a two-person podcast script with structure, dialogue, timestamps, and quotable moments.

Useful for:

- audio recording
- YouTube scripts
- live sessions
- interview prep

---

## Why people share this project

This repo is easy to share because the outputs are visual and personal.

It can produce:

- a map of your mind
- an essay in your voice
- a timeline of your beliefs
- a podcast script from your archive
- a decision critique based on your past writing

That makes it highly shareable across:

- GitHub
- X / Twitter
- LinkedIn
- creator communities
- personal knowledge management circles
- AI workflow communities

If you try it and like it, the best support is simple:

- give the repo a `Star`
- post a screenshot
- share your archive size and your results
- open an Issue or PR

---

## Quick Start in 10 Minutes

### 1. Requirements

- Python `3.10+`
- Git
- a valid `GOOGLE_API_KEY`
- a valid `GCP_PROJECT_ID`

### 2. Clone the repo

```bash
git clone https://github.com/xingjia10086/My-Digital-Mentor.git
cd My-Digital-Mentor
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env`

```bash
cp .env.example .env
```

Fill in the minimum required values:

| Variable | Required | Purpose |
|---|:---:|---|
| `GOOGLE_API_KEY` | ✅ | Gemini generation and embeddings |
| `GCP_PROJECT_ID` | ✅ | Google Cloud project |
| `APP_PASSWORD` | ✅ | Password for the local web app |

Optional:

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_TARGET_USER_ID`
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`

### 5. Add your documents

Put your `.md` and `.txt` files into either:

- `公众号/`
- `gongzhonghao/`

### 6. Build your local knowledge base

```bash
python rag_ingest.py
```

### 7. Launch the app

```bash
streamlit run web_ui.py
```

Then open:

```text
http://localhost:8501
```

---

## Before you deploy, know this

This is a real project, not a toy demo.  
That is a strength, but it also means you should expect some setup friction.

A few practical notes:

- first-time ingestion can take a while if your archive is large
- the better your archive, the better the output quality
- `rag_ingest.py` creates a local `chroma_db/`
- some environments may hit Google auth or networking issues during embedding
- local Google configuration matters for certain ingestion paths

The upside is equally real:

> **You are building a controllable personal AI system, not renting a generic one.**

---

## Project Structure

```text
My-Digital-Mentor/
├── web_ui.py              # Main Streamlit app with 8 modules
├── rag_ingest.py          # Knowledge ingestion and vectorization
├── ai_mentor.py           # Mentor-related experiment script
├── ai_writer.py           # Writing-related experiment script
├── knowledge_graph.py     # Knowledge graph generation
├── twitter_auto_agent.py  # Social publishing helper
├── daily_push.py          # Scheduled push script
├── .env.example           # Environment template
├── requirements.txt       # Python dependencies
├── docs/images/           # README screenshots
├── 公众号/                # Source article directory
├── gongzhonghao/          # Source article directory
└── chroma_db/             # Local vector store, generated after ingestion
```

---

## Tech Stack

- `Streamlit`
- `LangChain`
- `ChromaDB`
- `Google Gemini`
- `Google Embeddings`
- `Python`

---

## Why this repo deserves a Star

If you believe the future of AI is not just bigger models, but more personal models, this repo is part of that direction.

This project explores a powerful idea:

> **The most valuable AI may not be the AI that knows everything. It may be the AI that knows you.**

If that resonates, give it a `Star`.

It helps:

- more creators discover personal RAG workflows
- more developers contribute ideas and fixes
- more people treat their writing archive as an asset, not a graveyard

---

## Security Notes

- keep your secrets in `.env`
- never commit `.env` to a public repo
- `chroma_db/` contains your local knowledge asset
- rotate exposed API keys immediately

---

## License

MIT

If this project gave you a new idea about personal AI, digital memory, or creator tooling, star the repo and share it.

---

## More Resources

- [中文 README](README.md)
- [GitHub Growth Kit](docs/GITHUB_GROWTH_KIT.md)
- [Launch Copy Final](docs/LAUNCH_COPY_FINAL.md)
