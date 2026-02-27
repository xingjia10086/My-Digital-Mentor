import traceback

print("=== VertexAI Embeddings Final Test ===")
try:
    from langchain_google_vertexai import VertexAIEmbeddings
    e = VertexAIEmbeddings(
        model_name="text-embedding-004",
        project="gen-lang-client-0834352502",
        location="us-central1"
    )
    r = e.embed_query("hello world")
    print("SUCCESS! Embedding dimension:", len(r))
    print("First 3 values:", r[:3])
except Exception as ex:
    print("FAILED:", ex)
    traceback.print_exc()
