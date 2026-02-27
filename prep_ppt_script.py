import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = os.environ.get("GOOGLE_API_KEY", "")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Note: BRAIN_DIR might be specific to the run, but we will keep it as is if it's external, or use relative if meant to be local.
# The original code used a hardcoded path. If we want it to run anywhere, we should probably output to the local dir or a specified dir.
BRAIN_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(BRAIN_DIR, exist_ok=True)
ANALYSIS_FILE = os.path.join(BRAIN_DIR, "buddhism_analysis_final.json")
OUTLINE_FILE = os.path.join(BRAIN_DIR, "buddhism_ppt_outline_final.md")
PPT_SCRIPT_FILE = os.path.join(BRAIN_DIR, "buddhism_ppt_script.json")

# Configure Google AI SDK
genai.configure(api_key=API_KEY)

def get_best_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in ["models/gemini-1.5-flash-latest", "models/gemini-1.5-flash", "models/gemini-1.5-pro-latest", "models/gemini-1.5-pro", "models/gemini-2.0-flash-exp"]:
            if m in models:
                return genai.GenerativeModel(m)
        if models:
            return genai.GenerativeModel(models[0])
    except Exception as e:
        print(f"Error listing models: {e}")
    return None

model = get_best_model()

def main():
    if not model:
        print("Error: Could not find a suitable model.")
        return

    # Load analysis data
    with open(ANALYSIS_FILE, "r", encoding="utf-8") as f:
        analysis_data = json.load(f)
    
    # Load outline
    with open(OUTLINE_FILE, "r", encoding="utf-8") as f:
        outline_text = f.read()

    # Sample data to avoid prompt bloat
    ref_data = []
    for item in analysis_data:
        if not item["analysis"].startswith("FAILED"):
            ref_data.append({
                "filename": item["filename"],
                "summary": item["analysis"][:150]
            })

    prompt = f"""
    你现在是一名专业的PPT设计师。基于提供的研究大纲和照片摘要，生成一个结构化的JSON文件。
    
    【研究大纲】：
    {outline_text}
    
    【照片摘要】：
    {json.dumps(ref_data[:30], ensure_ascii=False)}

    要求：
    1. 生成一个 Slide 对象的 JSON 数组。
    2. 每个 Slide 包含：title, bullet_points (3-5个), image_filename (真实存在的), layout ("TITLE_AND_CONTENT" 或 "TITLE_ONLY")。
    3. 请只返回 JSON，不要任何 Markdown 标记。
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Basic cleanup if model adds markdown anyway
        if text.startswith("```json"): text = text.split("```json")[1].split("```")[0].strip()
        elif text.startswith("```"): text = text.split("```")[1].split("```")[0].strip()

        script_data = json.loads(text)
        with open(PPT_SCRIPT_FILE, "w", encoding="utf-8") as f:
            json.dump(script_data, f, ensure_ascii=False, indent=2)
        print(f"PPT Script generated: {PPT_SCRIPT_FILE}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
