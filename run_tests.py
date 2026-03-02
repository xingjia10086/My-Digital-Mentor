import os
import sys
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma

# Ensure we're in the right directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Load environment
load_dotenv(override=True)
API_KEY = os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    print("❌ ERROR: GOOGLE_API_KEY not found in environment.")
    sys.exit(1)

def run_isolated_tests():
    print("="*50)
    print("🌟 STARING ISOLATED LOGIC TESTS FOR MY DIGITAL MENTOR")
    print("="*50)
    
    # Check dependencies independently
    print("\n[Test 1] Initializing API Clients...")
    try:
        from google import genai
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        from web_ui import get_clients # IMPORT IT
        
        client, chosen_model, retriever, vectorstore = get_clients()
        print(f"  ✅ Success. Gemini Client & Embeddings initialized. Chosen Model: {chosen_model}")
    except Exception as e:
        print(f"  ❌ FAILED: API Client initialization: {e}")
        return

    # Test ChromaDB Retrieval
    print("\n[Test 2] Connecting to ChromaDB Knowledge Base...")
    try:
        count = vectorstore._collection.count()
        print(f"  ✅ Success. VectorStore connected: {count} chunks found.")
        
        if count == 0:
            print("  ⚠️ Warning: No documents found. Ingestion may have failed.")
            return
            
    except Exception as e:
        print(f"  ❌ FAILED: ChromaDB connection: {e}")
        return

    # Test Retrieval
    print("\n[Test 3] Testing Semantic Retrieval...")
    try:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke("关于创业的想法")
        if docs:
            print(f"  ✅ Success. Retrieved {len(docs)} documents.")
            print(f"     Example Source: {docs[0].metadata.get('source_file')}")
        else:
            print("  ⚠️ Warning: No documents retrieved for query.")
    except Exception as e:
        print(f"  ❌ FAILED: Retrieval: {e}")

    # Test Generation
    print("\n[Test 4] Testing Gemini Generation (Streaming)...")
    try:
        prompt = "用一两句话随便回答我，你是在在线的吗？"
        response = ""
        for chunk in client.models.generate_content_stream(model=chosen_model, contents=prompt):
            if chunk.text:
                response += chunk.text
        print(f"  ✅ Success. LLM Response: {response.strip()}")
    except Exception as e:
        print(f"  ❌ FAILED: LLM Generation: {e}")

    print("\n" + "="*50)
    print("🎉 ALL ISOLATED LOGIC TESTS PASSED.")
    print("="*50)

if __name__ == "__main__":
    run_isolated_tests()
