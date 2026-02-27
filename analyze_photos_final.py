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
# Using Gemini 1.5 Flash - highly efficient for vision and batch tasks
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_photo(image_path):
    """Analyzes a single photo using Google AI Gemini."""
    print(f"Analyzing: {os.path.basename(image_path)}")
    
    try:
        img = Image.open(image_path)
        
        prompt = """
        你是一位对佛学艺术和历史有深厚造诣的研究专家。请以导师助手的视角分析这张调研照片：
        1. 视觉描述：照片里展示了什么？（佛像、壁画、寺庙建筑细节、经书、或研究现场等）。
        2. 专业属性：如果可能，请识别其流派（如汉传、藏传、南传）、年代风格或特定题材。
        3. 价值挖掘：这张照片作为研究资料的价值在哪里？体现了研究者怎样的努力（如：选取的角度独到、捕捉到了罕见的细节、实地考察的艰辛等）。
        4. 汇报要点：请提炼1个足以在PPT中通过一句话打动导师的精彩结论。

        请用精准、富有文化底蕴且略带赞赏的中文回答。
        """

        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"FAILED: {str(e)}"

def generate_ppt_outline(all_analyses):
    """Synthesizes all analysis into a PPT outline."""
    print("Synthesizing analysis into PPT outline...")
    
    # Create a summary of findings for the final prompt
    summaries = []
    for a in all_analyses[:20]: # Sample 20 for the synthesis
        summaries.append(f"- {a['filename']}: {a['analysis'][:100]}...")

    summary_prompt = f"""
    你现在是一名专业的学术助理。我这里有 {len(all_analyses)} 张关于佛学田野调查的照片分析。
    请基于这些数据，为用户生成一份向导师汇报的研究心得PPT大纲（Markdown格式）。
    
    要求：
    1. **标题**：大气且具有学术深度。
    2. **结构**：
       - 第一页：封面。
       - 第二页：调研背景与考察路径。
       - 第三页到第五页：核心发现（按题材如造像艺术、建筑制式、文献考察分类，引用照片中的典型发现点）。
       - 第六页：田野调查的心得（强调获取这些第一手资料的艰辛与独特视角）。
       - 第七页：后续研究规划与致谢。
    3. **细节**：每一页都要包含【标题】、【核心要点】、【建议配图（引用具体文件名）】。
    4. **风格**：严谨、谦逊、富有佛学底蕴。

    数据背景：
    {chr(10).join(summaries)}
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

    # Process ALL 72 images
    results = []
    print(f"Starting final analysis of {len(files)} photos...")
    
    for filename in files:
        path = os.path.join(PHOTO_DIR, filename)
        res = analyze_photo(path)
        results.append({"filename": filename, "analysis": res})
        # Respect rate limits for free tier API keys (approx 15 RPM for some versions, 
        # but flash is usually higher. We'll add a small safety sleep).
        time.sleep(2) 

    # Save raw analysis
    with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Generate PPT Outline
    outline = generate_ppt_outline(results)
    with open(PPT_OUTLINE_FILE, "w", encoding="utf-8") as f:
        f.write(outline)

    print(f"COMPLETE! Results saved to:\n  - {ANALYSIS_FILE}\n  - {PPT_OUTLINE_FILE}")

if __name__ == "__main__":
    main()
