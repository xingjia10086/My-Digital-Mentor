import os
import json
import re

print("Loading slides.json...")
try:
    with open('slides.json', 'r', encoding='utf-8') as f:
        slides_json = json.load(f)
except Exception as e:
    print("Failed to parse slides.json:", e)
    exit(1)

html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Buddhism Research Report</title>
    <style>
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; background: #1A1A2E; color: #DDDDDD; overflow: hidden; }
        .slide { width: 100vw; height: 100vh; display: none; position: absolute; top:0; left:0; align-items: center; justify-content: center; flex-direction: column; overflow: hidden; padding: 40px; box-sizing: border-box; }
        .slide.active { display: flex; animation: fadein 0.5s; }
        @keyframes fadein { from { opacity: 0; } to { opacity: 1; } }
        
        .cover { text-align: left; align-items: flex-start; justify-content: center; padding-left: 10%; background-size: cover !important; background-position: right center !important; }
        .cover .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, #1A1A2E 40%, transparent 100%); z-index: 1; }
        .cover-content { position: relative; z-index: 2; max-width: 50%; }
        .cover h1 { font-size: 4em; color: #E8D49A; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.8); }
        .cover h2 { font-size: 2em; color: #CCCCCC; margin-bottom: 40px; }
        
        .section { background: #2D1B0E; text-align: center; }
        .section h1 { font-size: 6em; color: #E8D49A; margin: 0; }
        .section h2 { font-size: 2.5em; color: #CCCCCC; margin-top: 20px; font-weight: normal; }
        
        .content { flex-direction: row; justify-content: flex-start; align-items: flex-start; }
        .content-left { width: 50%; padding: 40px 60px; display: flex; flex-direction: column; justify-content: center; height: 100%; }
        .content-left h1 { font-size: 2.5em; color: #E8D49A; margin-top: 0; border-bottom: 2px solid #E8D49A; padding-bottom: 15px; }
        .content-left ul { font-size: 1.5em; line-height: 1.8; padding-left: 20px; }
        .content-left li { margin-bottom: 20px; }
        
        .content-right { width: 50%; height: 80%; display: flex; align-items: center; justify-content: center; padding: 40px; }
        .img-container { width: 100%; height: 100%; background-position: center; background-size: contain; background-repeat: no-repeat; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        
        .toc h1 { font-size: 3em; color: #E8D49A; margin-bottom: 40px; }
        .toc ul { font-size: 1.8em; line-height: 2; list-style-type: decimal; }
        
        .controls { position: fixed; bottom: 20px; right: 20px; z-index: 100; }
        button { background: rgba(232, 212, 154, 0.2); color: #E8D49A; border: 1px solid #E8D49A; padding: 10px 20px; font-size: 20px; cursor: pointer; border-radius: 4px; border:none; margin-left:10px; }
        button:hover { background: #E8D49A; color: #1A1A2E; }
    </style>
</head>
<body>
'''

original_files = [f for f in os.listdir('D:/GPT/AI-demo/Buddhism-Photos') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

for idx, slide in enumerate(slides_json):
    s_type = slide.get('type', 'content')
    img_name = slide.get('image', '')
    
    if img_name.startswith('image_') and original_files:
        try:
            img_idx = int(re.search(r'\d+', img_name).group()) - 1
            if 0 <= img_idx < len(original_files):
                img_name = original_files[img_idx]
        except: pass
        
    # Escape single quotes and newlines just in case
    img_url = f'./Buddhism-Photos/{img_name}' if img_name else ''
    active_cls = 'active' if idx == 0 else ''
    
    if s_type == 'cover' or s_type == 'ending':
        bg_style = f"background: url('{img_url}');" if img_url else ''
        html += f'''
        <div class="slide cover {active_cls}" style="{bg_style}" id="slide-{idx}">
            <div class="overlay"></div>
            <div class="cover-content">
                <h1>{slide.get('title','')}</h1>
                <h2>{slide.get('subtitle','')}</h2>
                <p style="color:#888; font-size:1.2em;">{slide.get('meta','')}</p>
            </div>
        </div>'''
    
    elif s_type == 'section':
        html += f'''
        <div class="slide section {active_cls}" id="slide-{idx}">
            <h1>{slide.get('title','')}</h1>
            <h2>{slide.get('subtitle','')}</h2>
        </div>'''
        
    elif s_type == 'toc':
        items_html = ''.join([f'<li>{item}</li>' for item in slide.get('items', [])])
        html += f'''
        <div class="slide toc {active_cls}" id="slide-{idx}">
            <h1>{slide.get('title','')}</h1>
            <ul>{items_html}</ul>
        </div>'''
        
    else:
        bullets_html = ''.join([f'<li>{item}</li>' for item in slide.get('bullets', [])])
        img_style = f"background-image: url('{img_url}');" if img_url else ''
        html += f'''
        <div class="slide content {active_cls}" id="slide-{idx}">
            <div class="content-left">
                <h1>{slide.get('title','')}</h1>
                <ul>{bullets_html}</ul>
            </div>
            <div class="content-right">
                <div class="img-container" style="{img_style}"></div>
            </div>
        </div>'''

html += '''
<div class="controls">
    <button onclick="prev()">❮ Prev</button>
    <button onclick="next()">Next ❯</button>
</div>

<script>
    let current = 0;
    const slides = document.querySelectorAll('.slide');
    function showSlide(n) {
        slides[current].classList.remove('active');
        current = (n + slides.length) % slides.length;
        slides[current].classList.add('active');
    }
    function next() { showSlide(current + 1); }
    function prev() { showSlide(current - 1); }
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'Space') next();
        if (e.key === 'ArrowLeft') prev();
    });
</script>
</body>
</html>
'''

output_path = r"D:\GPT\AI-demo\Master_Buddhism_Report_Pro.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML presentation successfully generated!")
