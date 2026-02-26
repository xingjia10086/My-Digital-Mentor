import os
import json
import time
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ID = "gen-lang-client-0834352502"
LOCATION = "us-central1"
PHOTO_DIR = r"D:\GPT\AI-demo\Buddhism-Photos"
BRAIN_DIR = r"C:\Users\xingj\.gemini\antigravity\brain\06d1296e-0570-43ef-85ea-4e580e2f5b62"
ANALYSIS_FILE = os.path.join(BRAIN_DIR, "buddhism_analysis_v3.json")
PPT_OUTLINE_FILE = os.path.join(BRAIN_DIR, "buddhism_ppt_outline_v3.md")

# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location=LOCATION)

# Try different model versions to find one that works in the project
MODEL_VERSIONS = ["gemini-1.5-flash-001", "gemini-1.5-flash-002", "gemini-1.5-pro-001", "gemini-1.5-pro-002"]

def get_working_model():
    for version in MODEL_VERSIONS:
        try:
            m = GenerativeModel(version)
            # Test with a simple prompt
            m.generate_content("test")
            print(f"Successfully connected to model: {version}")
            return m
        except Exception as e:
            print(f"Model {version} failed: {str(e)}")
    return None

model = get_working_model()

def analyze_photo(image_path):
    """Analyzes a single photo using Vertex AI Gemini."""
    if not model:
        return "ERROR: No working model found."
        
    print(f"Analyzing: {os.path.basename(image_path)}")
    
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    image_part = Part.from_data(data=image_data, mime_type="image/jpeg")
    
    prompt = """
    你是一位对佛学艺术和历史有深厚造诣的研究专家。请以导师助手的视角分析这张调研照片：
    1. 视觉描述：照片里展示了什么？（佛像、壁画、寺庙建筑细节、经书、或研究现场等）。
    2. 专业属性：如果可能，请识别其流派（如汉传、藏传、南传）、年代风格或特定题材。
    3. 价值挖掘：这张照片作为研究資料的价值在哪里？体现了研究者怎样的努力（如：选取的角度独到、捕捉到了罕见的细节、实地考察的艰辛等）。
    4. 汇报要点：请提炼1个足以在PPT中通过一句话打动导师的精彩结论。

    请用精准、富有文化底蕴且略带赞赏的中文回答。
    """

    try:
        response = model.generate_content(
            [image_part, prompt],
            generation_config={"temperature": 0.4, "max_output_tokens": 800},
            safety_settings=[
                SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH),
            ]
        )
        return response.text
    except Exception as e:
        return f"FAILED: {str(e)}"

def main():
    if not model:
        print("Fatal Error: Could not initialize any model.")
        return

    files = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not files:
        print("No images found.")
        return

    # Process first 10 for quick validation
    target_files = files[:10] 
    results = []

    print(f"Starting Phase 3 analysis of {len(target_files)} sample photos...")
    
    for filename in target_files:
        path = os.path.join(PHOTO_DIR, filename)
        res = analyze_photo(path)
        results.append({"filename": filename, "analysis": res})
        time.sleep(1)

    # Save raw analysis
    with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"DONE! Analysis saved to {ANALYSIS_FILE}")

if __name__ == "__main__":
    main()
