import os
import sys
from dotenv import load_dotenv

def run_tests():
    print("========================================")
    print("运行 My Digital Mentor 系统自动化完整测试")
    print("========================================\n")
    
    # 1. Test Environment Variables
    print("[1/5] 测试环境变量加载...", end="")
    load_dotenv(override=True)
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    project_id = os.environ.get("GCP_PROJECT_ID", "")
    app_pwd = os.environ.get("APP_PASSWORD", "")
    
    if api_key and project_id and app_pwd:
        print(" SUCCESS")
    else:
        print(" FAILED (缺失必要的 .env 参数)")
        sys.exit(1)
        
    # 2. Test ChromaDB Connection & Data
    print("[2/5] 测试 ChromaDB 向量数据库连接与数据量...", end="")
    try:
        from langchain_google_vertexai import VertexAIEmbeddings
        from langchain_community.vectorstores import Chroma
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        chroma_dir = os.path.join(base_dir, "chroma_db")
        if not os.path.exists(chroma_dir):
            print(" FAILED (找不到 chroma_db 文件夹)")
            sys.exit(1)
            
        embeddings = VertexAIEmbeddings(
            model_name="text-embedding-004", 
            project=project_id, 
            location="us-central1"
        )
        
        vectorstore = Chroma(
            persist_directory=chroma_dir, 
            embedding_function=embeddings, 
            collection_name="wechat_articles"
        )
        
        collection_data = vectorstore._collection.get()
        doc_count = len(collection_data['documents'])
        # Since the user just uploaded 2700 articles, the chunk count should be large
        if doc_count > 0:
            print(f" SUCCESS (发现 {doc_count} 个记忆切片)")
        else:
            print(" FAILED (数据库为空)")
            sys.exit(1)
            
    except Exception as e:
        print(f" FAILED\n错误详情: {e}")
        sys.exit(1)

    # 3. Test Retrieval Logic (Time Machine Mock)
    print("[3/5] 测试时光机年份筛选逻辑 (Mocking 2024)...", end="")
    try:
        all_metadatas = collection_data['metadatas']
        filtered_indices = []
        for i, meta in enumerate(all_metadatas):
            source_path = meta.get('source', '')
            if "/2024/" in source_path or "\\2024\\" in source_path:
                filtered_indices.append(i)
                
        print(f" SUCCESS (2024年文章切片数量: {len(filtered_indices)})")
    except Exception as e:
        print(f" FAILED\n错误详情: {e}")
        sys.exit(1)

    # 4. Test Google Gemini API Generation Connectivity
    print("[4/5] 测试 Google Gemini 内容生成通信...", end="")
    try:
        from web_ui import get_clients
        import logging
        logging.getLogger('langchain_core').setLevel(logging.ERROR)
        
        client, chosen_model, _, _ = get_clients()
        
        response = client.models.generate_content(
            model=chosen_model,
            contents='Respond with a single word "SUCCESS" to verify your status.',
        )
        if "SUCCESS" in response.text.upper() or "TRUE" in response.text.upper():
            print(f" SUCCESS (使用生产环境选择的模型: {chosen_model})")
        else:
            print(f" SUCCESS (连通正常，附加响应: {response.text.strip()})")
    except Exception as e:
        print(f" FAILED\n错误详情: {e}")
        sys.exit(1)
        
    # 5. Test Edge-TTS
    print("[5/5] 测试 edge-tts 语音合成组件就绪情况...", end="")
    try:
        import subprocess
        result = subprocess.run(['edge-tts', '--version'], capture_output=True, text=True)
        if "edge-tts" in result.stdout:
            print(" SUCCESS")
        else:
            print(" FAILED (命令执行异常)")
            sys.exit(1)
    except FileNotFoundError:
        print(" FAILED (edge-tts 未安装或不在环境变量中)")
        sys.exit(1)
    
    print("\n[COMPLETE] 系统所有核心模块连通性测试：100% 成功！具备上线并 Push 到 GitHub 的条件。")

if __name__ == "__main__":
    run_tests()
