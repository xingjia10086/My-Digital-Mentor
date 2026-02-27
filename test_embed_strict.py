import traceback
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    API_KEY = os.environ.get("GOOGLE_API_KEY", "")
    print("Testing strictly 'models/gemini-embedding-001'")
    e = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-001', google_api_key=API_KEY)
    print("Instantiated model property:", getattr(e, 'model', 'unknown'))
    res = e.embed_query('hello')
    print("SUCCESS Length:", len(res))
except Exception as ex:
    print("FAILED:", ex)
    traceback.print_exc()
