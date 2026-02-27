# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

# 金句列表
quotes = [
    {
        'text': '人是目的，不是手段',
        'subtext': '技术再发达，最终也是为人服务',
        'category': '核心理念',
        'color_scheme': 'blue'
    },
    {
        'text': '先上车，再换车',
        'subtext': '买房、移民、学习都是一个道理',
        'category': '行动哲学',
        'color_scheme': 'orange'
    },
    {
        'text': '焦虑本身没有用，行动才有',
        'subtext': '2023年ChatGPT刚火时的感悟',
        'category': 'AI时代',
        'color_scheme': 'green'
    },
    {
        'text': 'AI可以给你答案，但不能代替你\n蹲下来，耐心地陪孩子看一条鱼',
        'subtext': '菜市场教育哲学的真谛',
        'category': '亲子教育',
        'color_scheme': 'warm'
    },
    {
        'text': '你的经历，你的故事，你的情感，\n这就是你的护城河',
        'subtext': 'AI无法替代的真实人生',
        'category': '人生定位',
        'color_scheme': 'purple'
    },
    {
        'text': '门槛降低了，但要求提高了',
        'subtext': 'AI时代的学习之道',
        'category': '学习哲学',
        'color_scheme': 'teal'
    },
    {
        'text': '平凡又幸福的一天',
        'subtext': '最珍贵的生活状态',
        'category': '生活智慧',
        'color_scheme': 'pink'
    },
    {
        'text': '极致的利他，才能极致的利己',
        'subtext': '孟母三迁的商业哲学',
        'category': '创业心法',
        'color_scheme': 'gold'
    },
    {
        'text': '不是编程变简单了，\n是工具变强了',
        'subtext': '40岁学编程的感悟',
        'category': 'AI时代',
        'color_scheme': 'dark'
    },
    {
        'text': '值钱的是提出好问题的能力，\n以及判断答案好坏的能力',
        'subtext': 'AI时代最值钱的能力',
        'category': '学习哲学',
        'color_scheme': 'navy'
    },
    {
        'text': '几万个读者里，\n只有父母才是最铁的那几个',
        'subtext': '珍惜最亲近的人',
        'category': '家庭经营',
        'color_scheme': 'red'
    },
    {
        'text': '热爱指的就是，\n哪怕父母反复阻止你，\n也挡不住你想方设法要去做的事',
        'subtext': '发现孩子的真正兴趣',
        'category': '亲子教育',
        'color_scheme': 'coral'
    },
]

def get_colors(scheme):
    colors = {
        'blue': {'bg': (240, 248, 255), 'primary': (70, 130, 180), 'text': (50, 50, 50)},
        'orange': {'bg': (255, 248, 240), 'primary': (255, 140, 0), 'text': (50, 50, 50)},
        'green': {'bg': (240, 255, 240), 'primary': (34, 139, 34), 'text': (50, 50, 50)},
        'warm': {'bg': (255, 250, 240), 'primary': (210, 105, 30), 'text': (50, 50, 50)},
        'purple': {'bg': (248, 240, 255), 'primary': (128, 0, 128), 'text': (50, 50, 50)},
        'teal': {'bg': (240, 255, 255), 'primary': (0, 128, 128), 'text': (50, 50, 50)},
        'pink': {'bg': (255, 240, 245), 'primary': (255, 105, 180), 'text': (50, 50, 50)},
        'gold': {'bg': (255, 250, 240), 'primary': (218, 165, 32), 'text': (50, 50, 50)},
        'dark': {'bg': (45, 45, 45), 'primary': (100, 149, 237), 'text': (240, 240, 240)},
        'navy': {'bg': (25, 25, 50), 'primary': (100, 149, 237), 'text': (240, 240, 240)},
        'red': {'bg': (255, 240, 240), 'primary': (220, 20, 60), 'text': (50, 50, 50)},
        'coral': {'bg': (255, 245, 240), 'primary': (255, 127, 80), 'text': (50, 50, 50)},
    }
    return colors.get(scheme, colors['blue'])

def create_poster(quote_data, index):
    # 创建图片（小红书/朋友圈尺寸 3:4）
    width, height = 900, 1200
    colors = get_colors(quote_data['color_scheme'])
    
    img = Image.new('RGB', (width, height), colors['bg'])
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体
    try:
        font_large = ImageFont.truetype("simhei.ttf", 48)
        font_medium = ImageFont.truetype("simhei.ttf", 32)
        font_small = ImageFont.truetype("simhei.ttf", 24)
    except:
        try:
            font_large = ImageFont.truetype("msyh.ttc", 48)
            font_medium = ImageFont.truetype("msyh.ttc", 32)
            font_small = ImageFont.truetype("msyh.ttc", 24)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # 顶部装饰条
    draw.rectangle([0, 0, width, 8], fill=colors['primary'])
    
    # 类别标签
    category = quote_data['category']
    bbox = draw.textbbox((0, 0), category, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text((width - text_width - 40, 40), category, fill=colors['primary'], font=font_small)
    
    # 主标题
    text = quote_data['text']
    lines = text.split('\n')
    y_start = 350
    line_height = 70
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = y_start + i * line_height
        draw.text((x, y), line, fill=colors['text'], font=font_large)
    
    # 副标题
    subtext = quote_data['subtext']
    bbox = draw.textbbox((0, 0), subtext, font=font_medium)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = y_start + len(lines) * line_height + 60
    draw.text((x, y), subtext, fill=(128, 128, 128), font=font_medium)
    
    # 底部装饰
    draw.rectangle([width//4, height-150, width*3//4, height-146], fill=colors['primary'])
    
    # 底部签名
    draw.text((width//2 - 150, height-100), '—— 星佳人生指南', fill=colors['text'], font=font_small)
    draw.text((width//2 - 180, height-60), '基于1268篇原创文章提炼', fill=(150, 150, 150), font=ImageFont.load_default())
    
    # 保存
    filename = f'quote_poster_{index+1:02d}.png'
    output_path = os.path.join(r'D:\GPT\AI-demo\gongzhonghao', filename)
    img.save(output_path, 'PNG')
    return filename

def main():
    print('Starting to generate quote posters...')
    print(f'Total {len(quotes)} quotes')
    print()
    
    generated = []
    for i, quote in enumerate(quotes):
        try:
            filename = create_poster(quote, i)
            generated.append(filename)
            print(f'[OK] Generated: {filename}')
            print(f'  Content: {quote["text"][:30]}...')
        except Exception as e:
            print(f'[FAIL] Generation failed ({i+1}): {e}')
    
    print()
    print(f'生成完成! 共 {len(generated)} 张海报')
    print('File list:')
    for f in generated:
        print(f'  - {f}')

if __name__ == '__main__':
    main()
