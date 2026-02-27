import os
import json
import time
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = os.environ.get("GOOGLE_API_KEY", "")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTO_DIR = os.path.join(BASE_DIR, "Buddhism-Photos")
BRAIN_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(BRAIN_DIR, exist_ok=True)
ANALYSIS_FILE = os.path.join(BRAIN_DIR, "buddhism_analysis_final.json")
PPT_OUTLINE_FILE = os.path.join(BRAIN_DIR, "buddhism_ppt_outline_final.md")

# Configure Google AI SDK
genai.configure(api_key=API_KEY)

def get_best_model():
    print("Listing available models...")
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print(f"Available models: {models}")
        # Prioritize 1.5 Flash
        for m in ["models/gemini-1.5-flash-latest", "models/gemini-1.5-flash", "models/gemini-1.5-pro-latest", "models/gemini-1.5-pro"]:
            if m in models:
                print(f"Selecting model: {m}")
                return genai.GenerativeModel(m)
        if models:
            print(f"Falling back to: {models[0]}")
            return genai.GenerativeModel(models[0])
    except Exception as e:
        print(f"Error listing models: {e}")
    return None

model = get_best_model()

def analyze_photo(image_path):
    """Analyzes a single photo using Google AI Gemini."""
    if not model: return "ERROR: No model"
    print(f"Analyzing: {os.path.basename(image_path)}")
    try:
        img = Image.open(image_path)
        prompt = """
        你是一位对佛学艺术和历史有深厚造诣的研究专家。请以导师助手的视角分析这张调研照片：
        1. 视觉描述：照片里展示了什么？（佛像、壁画、寺庙建筑细节、经书、或研究现场等）。
        2. 专业属性：识别流派（如汉传、藏传、南传）、年代风格或特定题材。
        3. 价值挖掘：这张照片作为研究资料的价值在哪里？体现了研究者怎样的努力。
        4. 汇报要点：提炼1个能在PPT中打动导师的精彩结论。
        """
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"FAILED: {str(e)}"

def main():
    if not model: return
    files = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    results = []
    print(f"Processing {len(files)} photos...")
    for filename in files:
        res = analyze_photo(os.path.join(PHOTO_DIR, filename))
        results.append({"filename": filename, "analysis": res})
        time.sleep(4) # More conservative RPM for free tier

    with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Synthesis
    valid = [r for r in results if not r['analysis'].startswith("FAILED")]
    summary_text = "\n".join([f"- {r['filename']}: {r['analysis'][:200]}" for r in valid[:10]])
    prompt = f"基于以下调研分析，生成一份大气的佛学研究PPT大纲：\n{summary_text}"
    try:
        outline = model.generate_content(prompt).text
        with open(PPT_OUTLINE_FILE, "w", encoding="utf-8") as f:
            f.write(outline)
    except: pass
    print("FINISHED")

if __name__ == "__main__":
    main()
