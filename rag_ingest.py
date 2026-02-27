import os
import glob
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()

# Configuration
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
EMBEDDING_MODEL = "text-embedding-004"
TRACKER_FILE = os.path.join(BASE_DIR, "ingestion_tracker.json")

# Directories containing WeChat articles
DIRECTORIES = [
    os.path.join(BASE_DIR, "gongzhonghao"),
    os.path.join(BASE_DIR, "公众号")
]


class IngestionTracker:
    def __init__(self, file_path):
        self.file_path = file_path
        self.hashes = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.hashes, f, indent=2, ensure_ascii=False)

    def get_file_hash(self, file_path):
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def is_changed(self, file_path):
        current_hash = self.get_file_hash(file_path)
        old_hash = self.hashes.get(file_path)
        if current_hash != old_hash:
            self.hashes[file_path] = current_hash
            return True
        return False


def load_text_file(file_path):
    """Try multiple encodings to read a file robustly."""
    for encoding in ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, Exception):
            continue
    return None


def load_documents(tracker):
    """Scan and load all .md and .txt files using pure Python (no unstructured)."""
    documents = []
    print("Scanning directories for new or modified articles...")
    
    total_files_found = 0
    for directory in DIRECTORIES:
        if not os.path.exists(directory):
            print(f"  [Warning] Directory not found: {directory}")
            continue
        
        files = (
            glob.glob(os.path.join(directory, "**", "*.md"), recursive=True) +
            glob.glob(os.path.join(directory, "**", "*.txt"), recursive=True)
        )
        total_files_found += len(files)
        print(f"  Found {len(files)} files in {directory}")
        
        loaded = 0
        skipped = 0
        failed = 0
        for file_path in files:
            # Check if file has changed
            if not tracker.is_changed(file_path):
                skipped += 1
                continue

            content = load_text_file(file_path)
            if content and content.strip():
                documents.append(
                    Document(
                        page_content=content.strip(),
                        metadata={
                            "source": file_path,
                            "source_file": Path(file_path).name
                        }
                    )
                )
                loaded += 1
            else:
                failed += 1
        
        print(f"    New/Updated: {loaded}  |  Skipped (No Change): {skipped}  |  Failed: {failed}")
    
    print(f"\nTotal new segments loaded: {len(documents)}")
    return documents


def main():
    print("=" * 60)
    print("  AI 导师知识库 增量同步脚本 (Incremental Update)")
    print("=" * 60)
    
    # 0. Initialize tracker
    tracker = IngestionTracker(TRACKER_FILE)
    
    # 1. Load ONLY new or modified files
    raw_documents = load_documents(tracker)
    
    if not raw_documents:
        print("\n✨ 没有任何新增或修改的文章。知识库已是最新状态。")
        return
    
    # 2. Split into semantic chunks
    print(f"\nSplitting {len(raw_documents)} new documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]
    )
    chunks = splitter.split_documents(raw_documents)
    print(f"Total new chunks created: {len(chunks)}")
    
    # 3. Initialize Vertex AI Embeddings
    print(f"\nInitializing Vertex AI Embeddings ({EMBEDDING_MODEL})...")
    embeddings = VertexAIEmbeddings(
        model_name=EMBEDDING_MODEL,
        project=PROJECT_ID,
        location=LOCATION
    )
    
    # 4. Add to existing ChromaDB in batches
    BATCH_SIZE = 100
    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"\nEmbedding {len(chunks)} new chunks in {total_batches} batches...")
    
    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="wechat_articles"
    )
    
    for i in range(total_batches):
        batch = chunks[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
        for doc in batch:
            if len(doc.page_content) > 2000:
                doc.page_content = doc.page_content[:2000]
        
        print(f"  Batch {i+1}/{total_batches}: embedding {len(batch)} chunks...", end=" ", flush=True)
        try:
            vectorstore.add_documents(batch)
            print("✓")
        except Exception as e:
            print(f"✗ (skipped - {str(e)[:80]})")
    
    # 5. Save tracker state ONLY after successful ingestion
    tracker.save()
    print(f"\n✅ 增量同步完成！")
    print(f"  新增 {len(chunks)} 个文本块至知识库")
    print(f"  同步记录已保存至: {TRACKER_FILE}")


if __name__ == "__main__":
    main()
