import os
import re
import subprocess
import random
import streamlit as st
from dotenv import load_dotenv
from google import genai
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Override loaded variables if environment variables already exist
load_dotenv(override=True)

# --- Configuration ---
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")

# Automatically use relative path
CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")

EMBEDDING_MODEL = "text-embedding-004"
API_KEY = os.environ.get("GOOGLE_API_KEY", "")
MAX_HISTORY = 3
TEMP_AUDIO_FILE = "web_voice.mp3"

# --- UI Configuration Setup ---
st.set_page_config(
    page_title="星佳的数字生态",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialize Clients ---
@st.cache_resource
def get_clients():
    client = genai.Client(api_key=API_KEY)
    
    available = []
    for m in client.models.list():
        if 'gemini' in m.name.lower() and 'generate' in str(getattr(m, 'supported_actions', '')).lower():
            available.append(m.name)
            
    chosen_model = "gemini-2.0-flash" 
    for preferred in ["gemini-2.5-pro", "gemini-2.0-flash", "gemini-1.5-pro"]:
        for a in available:
            if preferred in a:
                chosen_model = a
                break
        if chosen_model != "gemini-2.0-flash":
            break
            
    # --- 最终修复：VM 的 access scopes 已修正为 cloud-platform，恢复使用原生的 Vertex AI Embeddings ---
    from langchain_google_vertexai import VertexAIEmbeddings
    embeddings = VertexAIEmbeddings(model_name=EMBEDDING_MODEL, project=PROJECT_ID, location=LOCATION)

    vectorstore = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings, collection_name="wechat_articles")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    return client, chosen_model, retriever, vectorstore

# --- Helper Functions ---
def format_docs(docs, for_writer=False):
    formatted = []
    for d in docs:
        source = d.metadata.get('source_file', '未知文章')
        label = "参考篇目" if for_writer else "摘自文章"
        formatted.append(f"【{label}：《{source}》】\n{d.page_content}")
    return "\n\n---\n\n".join(formatted)

def clean_for_tts(text):
    text = re.sub(r'[*_#`]', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text) 
    text = text.replace('\n', '。')
    # Clean up sources
    text = re.split(r'\(\s*💡 \*\*引用的历史灵感\*\*', text)[0]
    return text[:800] 

def generate_audio(text):
    clean_txt = clean_for_tts(text)
    cmd = f'edge-tts --text "{clean_txt}" --voice zh-CN-YunxiNeural --write-media {TEMP_AUDIO_FILE}'
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except Exception as e:
        print(f"TTS Error: {e}")
        return False

# --- App Logic ---
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        expected_password = os.environ.get("APP_PASSWORD", "")
        if st.session_state["password"] == expected_password: 
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "🔒 请输入专属顾问咨询访问口令", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "🔒 请输入专属顾问咨询访问口令", type="password", on_change=password_entered, key="password"
        )
        st.error("🔑 口令不正确，请重新输入或联系星佳获取。")
        return False
    else:
        return True

def main():
    if not check_password():
        st.stop()
        
    if not os.path.exists(CHROMA_PERSIST_DIR):
        st.error(f"❌ 找不到本地知识库目录：{CHROMA_PERSIST_DIR}。请先运行 `rag_ingest.py`。")
        st.stop()
        
    # Navigation (Move to top so UI shell always loads)
    st.sidebar.title("🌌 星佳的数字生态")
    app_mode = st.sidebar.radio("选择功能模块", ["🧠 灵魂导师 (对话)", "✍️ 替身写作 (AI Writer)", "🤔 思想图谱 (Knowledge Graph)", "🐦 推特分发机 (Twitter Agent)"])
    st.sidebar.markdown("---")

    try:
        client, chosen_model, retriever, vectorstore = get_clients()
        st.sidebar.info(f"**模型**: `{chosen_model}`\n\n**知识库**: 1.8万+ 切片")
    except Exception as e:
        st.error("❌ 核心大脑连接被阻断！")
        st.warning("系统无法正常启动，具体原因如下（您的免费 API 密钥已被谷歌安全机制封禁）：", icon="⚠️")
        st.code(str(e))
        st.markdown("""
        **解决方案：**
        由于我们刚才将其推到了公开的 GitHub 仓库，您的旧 `GOOGLE_API_KEY` 已经被谷歌巡检发现并自动停用。
        请您立刻去申请一个新的，然后在此处填入：
        """)
        new_key = st.text_input("🔑 输入全新的 GOOGLE_API_KEY", type="password")
        if st.button("更新密钥并重启系统"):
            env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
            if os.path.exists(env_file):
                with open(env_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                with open(env_file, 'w', encoding='utf-8') as f:
                    found = False
                    for line in lines:
                        if line.startswith("GOOGLE_API_KEY="):
                            f.write(f"GOOGLE_API_KEY={new_key}\n")
                            found = True
                        else:
                            f.write(line)
                    if not found:
                        f.write(f"\nGOOGLE_API_KEY={new_key}\n")
                        
            # Force update of os.environ and cached variable
            os.environ["GOOGLE_API_KEY"] = new_key
            global API_KEY
            API_KEY = new_key
            
            # Clear resource cache to force a re-init
            st.cache_resource.clear()
            st.rerun()
        st.stop()

    if app_mode == "🧠 灵魂导师 (对话)":
        render_chat_mentor(client, chosen_model, vectorstore)
    elif app_mode == "✍️ 替身写作 (AI Writer)":
        render_ai_writer(client, chosen_model, vectorstore)
    elif app_mode == "🤔 思想图谱 (Knowledge Graph)":
        render_knowledge_graph(client, chosen_model, vectorstore)
    elif app_mode == "🐦 推特分发机 (Twitter Agent)":
        render_twitter_agent(client, chosen_model, vectorstore)

# --- Feature 1: Chat Mentor ---
def render_chat_mentor(client, chosen_model, vectorstore):
    st.title("🧠 星佳的数字导师")
    st.markdown("汇聚五年思考结晶，可以在侧边栏开启语音播报。")
    
    enable_voice = st.sidebar.checkbox("🔊 开启语音播报 (TTS)", value=False)
    if st.sidebar.button("🧹 清空对话记忆", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "你好，星佳。我是你的数字分身与老朋友。最近有什么困惑，说来听听？", "audio": None}]
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("audio") and os.path.exists(message["audio"]):
                st.audio(message["audio"])

    if prompt := st.chat_input("有什么困惑？说来听听..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            audio_placeholder = st.empty()
            
            with st.spinner('导师沉思中...'):
                search_query = prompt
                if st.session_state.chat_history:
                    search_query = f"关于 {st.session_state.chat_history[-1]['q']} 的探讨: {prompt}"
                
                docs = vectorstore.similarity_search(search_query, k=5) 
                context_str = format_docs(docs)
                
                unique_sources = list(set([d.metadata.get('source_file', '未知') for d in docs]))
                
                history_str = ""
                if st.session_state.chat_history:
                    history_str = "\n【最近的对话历史】：\n"
                    for h in st.session_state.chat_history:
                        history_str += f"星佳: {h['q']}\n导师: {h['a'][:150]}...\n"
                        
                voice_rule = "你的回答必须非常口语化，像老朋友在面对面聊天（不要用列条目），字数精简，以便转化为语音。" if enable_voice else "你的排版要美观清晰，适合阅读。"
                
                sys_prompt = f"""你是星佳的数字克隆体也是他的人生导师。
请结合历史文章片段和对话上下文，深入探讨并解答他当下的困惑。

【要求】：
1. 具有启发性，像深交多年的挚友在启发他思考。
2. 潜移默化地化用他过去写过的心得与金句。
3. {voice_rule}

{history_str}

【历史片段】：
{context_str}

【当前的困惑】：
{prompt}

你的回答："""

            full_response = ""
            audio_path = None
            try:
                for chunk in client.models.generate_content_stream(model=chosen_model, contents=sys_prompt):
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                
                source_text = "\n\n*(💡 **引用的历史灵感**:*\n"
                for src in unique_sources:
                    source_text += f"*- 《{src}》*\n"
                source_text += ")"
                
                full_response += source_text
                message_placeholder.markdown(full_response)
                
                if enable_voice:
                    with st.spinner("正在生成语音..."):
                        if generate_audio(full_response):
                            audio_path = TEMP_AUDIO_FILE
                            audio_placeholder.audio(audio_path)
                
            except Exception as e:
                full_response = f"抱歉，遇到了一些技术问题：{e}"
                message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response, "audio": audio_path})
        st.session_state.chat_history.append({"q": prompt, "a": full_response})
        if len(st.session_state.chat_history) > MAX_HISTORY:
            st.session_state.chat_history.pop(0)

# --- Feature 2: AI Writer ---
def render_ai_writer(client, chosen_model, vectorstore):
    st.title("✍️ 替身写作 (AI Writer)")
    st.markdown("输入灵感或主题，系统将检索你的 1.8 万个历史切片，完全模仿你的笔触自动拼装出图文并茂的公众号初稿。")
    
    topic = st.text_area("文章主题或灵感关键词", placeholder="例如：为什么普通人很难真正做到长期主义？", height=100)
    
    if st.button("🚀 生成文章初稿", type="primary"):
        if not topic.strip():
            st.warning("请输入文章主题！")
            return
            
        st.markdown("---")
        result_placeholder = st.empty()
        full_article = ""
        
        with st.spinner("正在从 1.8万 个历史片段中检索相关灵感..."):
            retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
            docs = retriever.invoke(topic)
            context_str = format_docs(docs, for_writer=True)
            
            unique_sources = list(set([d.metadata.get('source_file', '未知') for d in docs]))
            st.success(f"找到了 {len(unique_sources)} 篇相关历史文章作为风格参考！")
            with st.expander("查看参考的出处"):
                for src in unique_sources:
                    st.write(f"- {src}")
                    
        with st.spinner("正在提笔撰写，模仿星佳的文风..."):
            prompt = f"""你是星佳，一位深耕互联网、教育规划、自我成长的公众号主理人。
现在你需要写一篇新的微信公众号文章初稿，主题是：【{topic}】。

请你先阅读以下你过去写过的相关文章片段，仔细体会你自己的写作文风、排版习惯、常用金句和思维逻辑：

【历史风格参考】：
{context_str}

【写作要求】：
1. 你的文章带有强烈的个人经验色彩和故事性，像是在跟读者交心。
2. 完美复刻历史参考片段中的写作风格，包括自然的分段、合理的设问、以及一针见血的断言。
3. 请为这篇文章起一个带有点“星佳味道”的标题（放在全文最前面）。
4. 字数要求在 1500 字左右，结构上要有：引入 -> 破题 -> 论证 -> 结论。
5. 直接输出 Markdown 格式的正式文章内容，不需要废话。

开始创作吧："""

            try:
                for chunk in client.models.generate_content_stream(model=chosen_model, contents=prompt):
                    if chunk.text:
                        full_article += chunk.text
                        result_placeholder.markdown(full_article + " ▌")
                result_placeholder.markdown(full_article)
            except Exception as e:
                st.error(f"生成失败：{e}")

# --- Feature 3: Knowledge Graph ---
def render_knowledge_graph(client, chosen_model, vectorstore):
    st.title("🤔 个人思想图谱")
    st.markdown("让 AI 从你的历史文章库中随机抽取大量数据，提炼并可视化你的核心理念网络。")
    
    if st.button("🧬 开始深度挖掘并生成图谱"):
        st.markdown("---")
        
        with st.spinner("正在读取知识库数据..."):
            collection_data = vectorstore._collection.get()
            all_docs = collection_data['documents']
            total_docs = len(all_docs)
            sample_size = min(200, total_docs)
            
            sampled_docs = random.sample(all_docs, sample_size)
            combined_text = "\n\n".join(sampled_docs)
            st.info(f"已从 {total_docs} 个片段中随机抽样了 {sample_size} 个核心片段。")
            
        with st.spinner("正在用大模型进行主题提炼与关系推演..."):
            prompt = f"""请分析以下这 {sample_size} 个文字片段（这只是作者过去五年文章的随机抽样）。

你的任务是提取出代表作者最核心理念、思考模型、关注领域的 **30 个**关键词或短语，并构建一个高度关联的知识图谱。

要求：
1. **结构化**：使用 Mermaid `graph LR` (从左到右) 布局。
2. **美化**：利用 `subgraph` 将相关的词汇进行聚类（例如：家庭与资产、个人成长、AI与工具）。
3. **节点分级**：最重要的 3-5 个核心词汇请使用 `节点ID(("文字"))` 这种双圈表示。
4. **社交属性**：连接线带上说明，使用 `-->|说明文字|` 格式。
5. **无损输出**：确保节点 ID 唯一，不要出现重复的节点定义。

**关键语法规则（必须严格遵守，否则图谱会渲染失败）**：
- 所有节点文字必须用英文双引号包裹，例如：`A["长期主义"]`、`B(("核心理念"))`
- subgraph 标题必须用英文双引号包裹，例如：`subgraph "个人成长"`
- 所有边的标签使用 `-->|标签|` 格式，标签内不要用引号
- 禁止使用中文标点（如：（）【】：；，），统一使用英文标点
- 禁止使用 $、&、# 这些特殊字符
- 只输出 Mermaid 代码，用 ```mermaid 前后缀包裹

【抽样材料】：
{combined_text[:60000]}

Mermaid 图表代码："""

            full_response = ""
            graph_placeholder = st.empty()
            try:
                for chunk in client.models.generate_content_stream(model=chosen_model, contents=prompt):
                    if chunk.text:
                        full_response += chunk.text
                        graph_placeholder.markdown(full_response)
                
                match = re.search(r'```mermaid(.*?)```', full_response, re.DOTALL)
                if match:
                    mermaid_code = match.group(1).strip()
                    
                    # --- Robust Mermaid Sanitization ---
                    def sanitize_mermaid_code(code):
                        """Aggressively clean LLM-generated Mermaid to prevent syntax errors."""
                        lines = code.split('\n')
                        cleaned = []
                        for line in lines:
                            # 0. Replace Chinese punctuation with ASCII equivalents
                            line = line.replace('（', '(').replace('）', ')').replace('【', '[').replace('】', ']')
                            line = line.replace('：', ':').replace('；', ';').replace('，', ',').replace('“', '"').replace('”', '"')
                            
                            # 1. Handle subgraph titles: subgraph Title Text -> subgraph "Title Text"
                            sg_match = re.match(r'^(\s*subgraph\s+)(?!")(.*?)$', line)
                            if sg_match:
                                prefix, title = sg_match.group(1), sg_match.group(2).strip()
                                if title and not title.startswith('"'):
                                    title = title.replace('"', "'")
                                    line = f'{prefix}"{title}"'
                            
                            # 2. Fix double-circle nodes: ID((text)) - ensure text is quoted
                            line = re.sub(
                                r'(\b\w+)\(\((?!")([^)]+)\)\)',
                                lambda m: f'{m.group(1)}(("{m.group(2).replace(chr(34), chr(39))}"))' , line
                            )
                            
                            # 3. Fix regular nodes with special chars: ID[text] or ID(text)
                            def quote_node(m):
                                opener, content, closer = m.group(1), m.group(2), m.group(3)
                                content = content.replace('"', "'")
                                return f'{opener}"{content}"{closer}'
                            
                            # Quote content in [] and () brackets if it contains special chars and isn't already quoted
                            line = re.sub(r'(\[)(?!")([^\]]*?[:()/\[\]&$#][^\]]*?)(\])', quote_node, line)
                            line = re.sub(r'(\()(?!")([^()]*?[:\[\]&$#/][^()]*?)(\))', quote_node, line)
                            
                            # 4. Fix edge labels: -- text --> or -->|text| ensure safe
                            def quote_edge_label(m):
                                pre, label, post = m.group(1), m.group(2), m.group(3)
                                label = label.replace('"', "'").replace('|', ' ')
                                return f'{pre}"{label}"{post}'
                            line = re.sub(r'(\|)([^|]+)(\|)', quote_edge_label, line)
                            line = re.sub(r'(--\s*)([^-|>][^->]*?)\s*(-->)', quote_edge_label, line)
                            
                            # 5. Replace characters that break Mermaid even inside quotes
                            line = line.replace('$', 'USD').replace('&', ' and ').replace('#', ' ')
                            
                            # 6. Clean up double-double quotes from multiple passes
                            line = line.replace('""', '"')
                            
                            cleaned.append(line)
                        return '\n'.join(cleaned)
                    
                    mermaid_code = sanitize_mermaid_code(mermaid_code)
                    
                    graph_placeholder.empty()
                    # 调试用：显示代码
                    with st.expander("🛠️ 查看图谱源代码 (调试用)"):
                        st.code(mermaid_code, language="mermaid")
                    
                    # 注入精美样式 + 下载按钮
                    st.components.v1.html(
                        f'''
                        <style>
                            .container {{
                                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                                border-radius: 20px;
                                padding: 30px;
                                border: 1px solid rgba(255,255,255,0.1);
                                box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
                                font-family: "Inter", "Microsoft YaHei", sans-serif;
                                overflow: auto;
                            }}
                            .header {{
                                color: #38bdf8;
                                font-size: 14px;
                                letter-spacing: 2px;
                                text-transform: uppercase;
                                margin-bottom: 20px;
                                text-align: center;
                                font-weight: 600;
                            }}
                            .footer {{
                                margin-top: 20px;
                                text-align: right;
                                color: rgba(255,255,255,0.4);
                                font-size: 12px;
                            }}
                            .mermaid {{
                                display: flex;
                                justify-content: center;
                            }}
                            .node rect, .node circle, .node polygon, .node path {{
                                fill: rgba(56, 189, 248, 0.1) !important;
                                stroke: #38bdf8 !important;
                                stroke-width: 1.5px !important;
                            }}
                            .node .label, .nodeLabel {{
                                color: #e2e8f0 !important;
                                fill: #e2e8f0 !important;
                                font-weight: 500 !important;
                            }}
                            .edgePath .path {{
                                stroke: rgba(255, 255, 255, 0.2) !important;
                                stroke-width: 1px !important;
                            }}
                            .edgeLabel {{
                                background-color: transparent !important;
                                color: #94a3b8 !important;
                                fill: #94a3b8 !important;
                                font-size: 10px !important;
                            }}
                            .cluster rect {{
                                fill: rgba(255,255,255,0.05) !important;
                                stroke: rgba(255,255,255,0.15) !important;
                            }}
                            .download-btn {{
                                display: block;
                                margin: 20px auto 0;
                                padding: 12px 32px;
                                background: linear-gradient(135deg, #38bdf8, #6366f1);
                                color: #fff;
                                border: none;
                                border-radius: 12px;
                                font-size: 16px;
                                font-weight: 600;
                                cursor: pointer;
                                transition: all 0.3s ease;
                                box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3);
                            }}
                            .download-btn:hover {{
                                transform: translateY(-2px);
                                box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5);
                            }}
                        </style>
                        <div class="container" id="graph-container">
                            <div class="header">🌌 星佳思想演化图谱 · 2026</div>
                            <div class="mermaid">
                                {mermaid_code}
                            </div>
                            <div class="footer">由 星佳数字生态 · 数字灵魂导师 驱动生成</div>
                        </div>
                        <button class="download-btn" id="dlBtn" onclick="downloadGraph()">📥 下载图谱为高清图片</button>
                        <script type="module">
                            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                            mermaid.initialize({{
                                startOnLoad: true,
                                theme: 'dark',
                                flowchart: {{ htmlLabels: false }},
                                themeVariables: {{
                                    primaryColor: '#38bdf8',
                                    primaryTextColor: '#e2e8f0',
                                    primaryBorderColor: '#38bdf8',
                                    lineColor: '#576574',
                                    secondaryColor: '#0061ff',
                                    tertiaryColor: '#fff',
                                    fontSize: '14px',
                                    fontFamily: '"Microsoft YaHei", "SimHei", "Inter", sans-serif'
                                }}
                            }});
                        </script>
                        <script>
                            function downloadGraph() {{
                                const btn = document.getElementById('dlBtn');
                                const svgEl = document.querySelector('#graph-container svg');
                                if (!svgEl) {{
                                    alert('图谱尚未渲染完成，请稍后再试');
                                    return;
                                }}
                                btn.textContent = '⏳ 正在生成高清图片...';
                                btn.disabled = true;

                                const clonedSvg = svgEl.cloneNode(true);
                                const w = svgEl.viewBox.baseVal.width || svgEl.getBoundingClientRect().width;
                                const h = svgEl.viewBox.baseVal.height || svgEl.getBoundingClientRect().height;
                                clonedSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
                                clonedSvg.setAttribute('width', w);
                                clonedSvg.setAttribute('height', h);

                                // Inject styles into cloned SVG for standalone rendering
                                const sty = document.createElementNS('http://www.w3.org/2000/svg', 'style');
                                sty.textContent = 'text,tspan{{font-family:"Microsoft YaHei","SimHei","Inter",sans-serif;fill:#e2e8f0}} '
                                    + '.node rect,.node circle,.node polygon,.node path{{fill:rgba(56,189,248,0.12);stroke:#38bdf8;stroke-width:1.5px}} '
                                    + '.edgePath .path{{stroke:rgba(255,255,255,0.25);stroke-width:1px}} '
                                    + '.edgeLabel text{{fill:#94a3b8;font-size:10px}} '
                                    + '.cluster rect{{fill:rgba(255,255,255,0.05);stroke:rgba(255,255,255,0.15)}}';
                                clonedSvg.insertBefore(sty, clonedSvg.firstChild);

                                const scale = 3;
                                const padTop = 70, padBottom = 50, padX = 40;
                                const canvasW = (w + padX * 2) * scale;
                                const canvasH = (h + padTop + padBottom) * scale;

                                // Serialize SVG to base64 data URL (avoids blob URL taint issues)
                                const svgStr = new XMLSerializer().serializeToString(clonedSvg);
                                const svgBase64 = btoa(unescape(encodeURIComponent(svgStr)));
                                const dataUrl = 'data:image/svg+xml;base64,' + svgBase64;

                                const canvas = document.createElement('canvas');
                                canvas.width = canvasW;
                                canvas.height = canvasH;
                                const ctx = canvas.getContext('2d');

                                // Draw dark gradient background
                                const grad = ctx.createLinearGradient(0, 0, canvasW, canvasH);
                                grad.addColorStop(0, '#0f172a');
                                grad.addColorStop(1, '#1e293b');
                                ctx.fillStyle = grad;
                                ctx.fillRect(0, 0, canvasW, canvasH);

                                // Header
                                ctx.fillStyle = '#38bdf8';
                                ctx.font = 'bold ' + (18 * scale) + 'px "Microsoft YaHei","Inter",sans-serif';
                                ctx.textAlign = 'center';
                                ctx.fillText('星佳思想演化图谱 · 2026', canvasW / 2, 42 * scale);

                                const img = new Image();
                                img.onload = function() {{
                                    ctx.drawImage(img, padX * scale, padTop * scale, w * scale, h * scale);

                                    // Footer
                                    ctx.fillStyle = 'rgba(255,255,255,0.4)';
                                    ctx.font = (11 * scale) + 'px "Microsoft YaHei","Inter",sans-serif';
                                    ctx.textAlign = 'right';
                                    ctx.fillText('由 星佳数字生态 · 数字灵魂导师 驱动生成', canvasW - 30 * scale, canvasH - 15 * scale);

                                    try {{
                                        const pngUrl = canvas.toDataURL('image/png');
                                        const a = document.createElement('a');
                                        a.download = '星佳思想演化图谱_2026.png';
                                        a.href = pngUrl;
                                        document.body.appendChild(a);
                                        a.click();
                                        document.body.removeChild(a);
                                        btn.textContent = '✅ 下载成功！';
                                    }} catch(e) {{
                                        // PNG export failed (canvas tainted), fall back to SVG download
                                        fallbackSvgDownload(svgStr, w, h);
                                    }}
                                    setTimeout(function(){{ btn.textContent='📥 下载图谱为高清图片'; btn.disabled=false; }}, 3000);
                                }};
                                img.onerror = function() {{
                                    // Image load failed, fall back to SVG download
                                    fallbackSvgDownload(svgStr, w, h);
                                    setTimeout(function(){{ btn.textContent='📥 下载图谱为高清图片'; btn.disabled=false; }}, 3000);
                                }};
                                img.src = dataUrl;
                            }}

                            function fallbackSvgDownload(innerSvg, w, h) {{
                                // Wrap the SVG with a dark background for standalone viewing
                                const wrapper = '<svg xmlns="http://www.w3.org/2000/svg" width="' + (w+80) + '" height="' + (h+120) + '">'
                                    + '<rect width="100%" height="100%" fill="#0f172a"/>'
                                    + '<text x="' + ((w+80)/2) + '" y="45" text-anchor="middle" fill="#38bdf8" font-size="22" font-weight="bold" '
                                    + 'font-family="Microsoft YaHei,SimHei,Inter,sans-serif">星佳思想演化图谱 · 2026</text>'
                                    + '<g transform="translate(40,70)">' + innerSvg + '</g>'
                                    + '<text x="' + (w+50) + '" y="' + (h+105) + '" text-anchor="end" fill="rgba(255,255,255,0.4)" font-size="12" '
                                    + 'font-family="Microsoft YaHei,SimHei,Inter,sans-serif">由 星佳数字生态 · 数字灵魂导师 驱动生成</text>'
                                    + '</svg>';
                                const blob = new Blob([wrapper], {{type:'image/svg+xml;charset=utf-8'}});
                                const url = URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.download = '星佳思想演化图谱_2026.svg';
                                a.href = url;
                                document.body.appendChild(a);
                                a.click();
                                document.body.removeChild(a);
                                setTimeout(function(){{ URL.revokeObjectURL(url); }}, 1000);
                                document.getElementById('dlBtn').textContent = '✅ 已下载 SVG 格式';
                            }}
                        </script>
                        ''',
                        height=850,
                        scrolling=True
                    )
                    st.success("图谱渲染完成！现在的视觉效果非常适合截图发送至社交平台。")
                else:
                    st.warning("未能提取到图谱代码。")
            except Exception as e:
                st.error(f"提取失败：{e}")

# --- Feature 4: Twitter Agent ---
def render_twitter_agent(client, chosen_model, vectorstore):
    st.title("🐦 推特分发机 (Twitter Agent)")
    st.markdown("半自动防封版：系统将从你的海量公众号历史中提取灵光一闪的商业/人生洞察，并将其转化为适合在 X (Twitter) 上发布的高质量双语推文，甚至附带配图提示词。")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("想聊点什么方向？（留空则完全随机碰撞）", placeholder="例如：认知破局、投资、或者是时间管理...")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("✨ 提炼生成爆款推文", type="primary", use_container_width=True)
        
    if generate_btn:
        st.markdown("---")
        result_placeholder = st.empty()
        full_tweet = ""
        
        with st.spinner("正在进入 1.8 万个记忆切片中打捞灵感..."):
            if topic.strip():
                retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
                docs = retriever.invoke(topic)
                context_str = format_docs(docs)
                sources = list(set([d.metadata.get('source_file', '未知') for d in docs]))
            else:
                collection_data = vectorstore._collection.get()
                all_docs = collection_data['documents']
                all_metadatas = collection_data['metadatas']
                sample_indices = random.sample(range(len(all_docs)), 5)
                
                docs = []
                for idx in sample_indices:
                    docs.append(Document(page_content=all_docs[idx], metadata=all_metadatas[idx]))
                
                context_str = format_docs(docs)
                sources = list(set([d.metadata.get('source_file', '未知') for d in docs]))

        with st.spinner("正在用极为犀利的文字重塑推特内容..."):
            topic_instruction = f"当前用户非常明确地希望你探讨的主题是：【{topic}】。你必须绝对优先围绕这个主题展开推文！如果你提供的历史碎片中没有直接相关的内容，请结合你自身的商业认知强行切入到该主题！\n" if topic.strip() else ""
            
            prompt = f"""你是星佳，一位在 X (Twitter) 上拥有高影响力的华语商业与个人成长博主。
请结合以下从你过去公众号文章中提取的【思想切片】，写一条能在推特上引发广泛共鸣和转发的高质量推文（Tweet）。

{topic_instruction}
【思想切片来源】：
{context_str}

【推文写作规范】：
1. 语言：输出【中文版】和地道的【英文版】双语对照。
2. 风格：犀利、通透、反直觉。带有“硅谷大佬”般的极简极客范。
3. 格式：第一句话必须极其吸睛（Hook）。正文切分短句，多用空行。字数控制在能一次发完的长度（中文 140 字以内）。
4. 标签：在推文末尾加上 2-3 个合适的英文 Hashtag（如 #Mindset #Crypto 等）。
5. 配图指令：在最底下，附带提供一段完美的英文 AI 绘画 Prompt，描述一张适合这条推文的极简高级感配图（例如：A cinematic high-end photography of ...）。

直接输出排版好的推文结果："""

            try:
                for chunk in client.models.generate_content_stream(model=chosen_model, contents=prompt):
                    if chunk.text:
                        full_tweet += chunk.text
                        result_placeholder.markdown(full_tweet + " ▌")
                
                full_tweet += "\n\n---\n*💡 灵感来源溯源：*\n"
                for src in sources:
                    full_tweet += f"- 《{src}》\n"
                    
                result_placeholder.markdown(full_tweet)
                st.success("✅ 签发完毕！你可以复制上方带感的内容和中文直接发推。如果需要配图，把最下方的英文 Prompt 扔给 Midjourney 或 Imagen 即可。")
                
            except Exception as e:
                st.error(f"生成失败：{e}")

if __name__ == "__main__":
    main()
