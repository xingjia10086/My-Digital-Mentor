import logging
import traceback
import os
from dotenv import load_dotenv

load_dotenv()

print("--- Testing VertexAIEmbeddings ---")
try:
    from langchain_google_vertexai import VertexAIEmbeddings
    e1 = VertexAIEmbeddings(model_name='text-embedding-004', project=os.environ.get("GCP_PROJECT_ID", ""), location='us-central1')
    res1 = e1.embed_query('hello')
    print("VERTEX SUCCESS. Length:", len(res1))
except Exception as ex:
    print("VERTEX FAILED:", ex)
    traceback.print_exc()

print("--- Testing GoogleGenerativeAIEmbeddings (models/text-embedding-004) ---")
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    API_KEY = os.environ.get("GOOGLE_API_KEY", "")
    e2 = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004', google_api_key=API_KEY)
    res2 = e2.embed_query('hello')
    print("GENAI (004) SUCCESS. Length:", len(res2))
except Exception as ex:
    print("GENAI (004) FAILED:", ex)
    traceback.print_exc()

print("--- Testing GoogleGenerativeAIEmbeddings (models/embedding-001) ---")
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    API_KEY = os.environ.get("GOOGLE_API_KEY", "")
    e3 = GoogleGenerativeAIEmbeddings(model='models/embedding-001', google_api_key=API_KEY)
    res3 = e3.embed_query('hello')
    print("GENAI (001) SUCCESS. Length:", len(res3))
except Exception as ex:
    print("GENAI (001) FAILED:", ex)
    traceback.print_exc()
