import os
import json
import base64
import time
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

# Configuration
PROJECT_ID = "gen-lang-client-0834352502"
LOCATION = "us-central1" # Default location
PHOTO_DIR = r"D:\GPT\AI-demo\Buddhism-Photos"
OUTPUT_FILE = r"D:\GPT\AI-demo\buddhism_analysis.json"

# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel("gemini-1.5-flash-002")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_photo(image_path):
    print(f"Analyzing {os.path.basename(image_path)}...")
    
    # Construct parts for multimodal input
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    image_part = Part.from_data(data=image_data, mime_type="image/jpeg")
    
    prompt = """
    您是一位资深的佛学研究专家。请分析这张照片：
    1. 识别照片中的主要佛教元素（如佛像、建筑风格、特定的宗教符号或文物）。
    2. 提供这些元素的文化/宗教背景说明。
    3. 评价这张照片背后体现出的研究兴趣和努力（例如：是否是实地拍摄、观察是否细致、是否涵盖了多样性的题材）。
    4. 提取出适合放在汇报PPT中的3个核心关键词。

    请用简洁、学术且具有感悟性的中文回答。
    """

    try:
        response = model.generate_content(
            [image_part, prompt],
            generation_config={"temperature": 0.2, "max_output_tokens": 1024},
            safety_settings=[
                SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH),
                SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH),
            ]
        )
        return response.text
    except Exception as e:
        return f"Error analyzing {image_path}: {str(e)}"

def main():
    results = []
    files = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Found {len(files)} photos. Starting batch analysis...")
    
    for i, filename in enumerate(files):
        path = os.path.join(PHOTO_DIR, filename)
        analysis = analyze_photo(path)
        results.append({
            "filename": filename,
            "analysis": analysis
        })
        
        # Save progress periodically
        if (i + 1) % 5 == 0 or (i + 1) == len(files):
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Progress saved: {i + 1}/{len(files)}")
            
        time.sleep(1) # Simple rate limiting

    print(f"Analysis complete. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
