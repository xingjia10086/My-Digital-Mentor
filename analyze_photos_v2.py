import os
import json
import time
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "")
LOCATION = "us-central1"
PHOTO_DIR = r"D:\GPT\AI-demo\Buddhism-Photos"
BRAIN_DIR = r"C:\Users\xingj\.gemini\antigravity\brain\06d1296e-0570-43ef-85ea-4e580e2f5b62"
ANALYSIS_FILE = os.path.join(BRAIN_DIR, "buddhism_analysis_v2.json")
PPT_OUTLINE_FILE = os.path.join(BRAIN_DIR, "buddhism_ppt_outline.md")

# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location=LOCATION)
# Using the stable 'gemini-1.5-flash' alias
model = GenerativeModel("gemini-1.5-flash")

def analyze_photo(image_path):
    """Analyzes a single photo using Vertex AI Gemini."""
    print(f"Analyzing: {os.path.basename(image_path)}")
    
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    image_part = Part.from_data(data=image_data, mime_type="image/jpeg")
    
    prompt = """
    你是一位对佛学艺术和历史有深厚造诣的研究专家。请以导师助手的视角分析这张调研照片：
    1. 视觉描述：照片里展示了什么？（佛像、壁画、寺庙建筑细节、经书、或研究现场等）。
    2. 专业属性：如果可能，请识别其流派（如汉传、藏传、南传）、年代风格或特定题材。
    3. 价值挖掘：这张照片作为研究资料的价值在哪里？体现了研究者怎样的努力（如：选取的角度独到、捕捉到了罕见的细节、实地考察的艰辛等）。
    4. 汇报要点：请提炼1个足以在PPT中通过一句话打动导师的精彩结论。

    请用精准、富有文化底蕴且略带赞賞的中文回答。
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

def generate_ppt_outline(all_analyses):
    """Synthesizes all analysis into a PPT outline."""
    print("Synthesizing analysis into PPT outline...")
    
    # We pass a summary of findings to avoid hitting token limits in the prompt
    summary_data = []
    for a in all_analyses[:15]: # Use first 15 for a representative sample
        summary_data.append(f"File {a['filename']}: {a['analysis'][:150]}...")

    summary_prompt = f"""
    基于对这 {len(all_analyses)} 张佛学考察照片的初步分析，请为我生成一份向佛学导师汇报的研究心得PPT大纲。
    
    要求：
    1. 标题要大气且学术（例如：梵像寻踪：论...的田野调查与初步思考）。
    2. 大纲逻辑清晰，包含：前言、调研轨迹、重点发现（按题材分类）、深度思考、结案感悟。
    3. 每一页幻灯片（Slide）要有明确的【标题】、【核心内容点】和【推荐配图建议】。
    4. 语言风格要体现出对佛学的敬畏心和严谨的研究态度，同时含蓄地展示出学生（用户）在收集这些资料过程中付出的巨大心力。

    分析数据示例：
    {" ".join(summary_data)}
    """

    try:
        response = model.generate_content(summary_prompt)
        return response.text
    except Exception as e:
        return f"Synthesis Error: {str(e)}"

def main():
    if not os.path.exists(PHOTO_DIR):
        print(f"Error: Directory {PHOTO_DIR} not found.")
        return

    files = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not files:
        print("No images found.")
        return

    # Process a representative subset to ensure speed and quality
    target_files = files[:30] 
    results = []

    print(f"Starting Phase 2 analysis of {len(target_files)} key photos...")
    
    for filename in target_files:
        path = os.path.join(PHOTO_DIR, filename)
        res = analyze_photo(path)
        results.append({"filename": filename, "analysis": res})
        time.sleep(0.5)

    # Save raw analysis
    with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Generate PPT Outline
    outline = generate_ppt_outline(results)
    with open(PPT_OUTLINE_FILE, "w", encoding="utf-8") as f:
        f.write(outline)

    print(f"DONE! Analysis saved to {ANALYSIS_FILE}")
    print(f"PPT Outline saved to {PPT_OUTLINE_FILE}")

if __name__ == "__main__":
    main()
