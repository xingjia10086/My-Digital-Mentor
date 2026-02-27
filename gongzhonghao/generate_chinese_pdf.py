# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

def create_chinese_pdf():
    # 尝试注册中文字体
    font_paths = [
        'C:/Windows/Fonts/simhei.ttf',  # 黑体
        'C:/Windows/Fonts/simsun.ttc',  # 宋体
        'C:/Windows/Fonts/msyh.ttc',    # 微软雅黑
        'C:/Windows/Fonts/simkai.ttf',  # 楷体
    ]
    
    chinese_font = None
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font_name = os.path.basename(font_path).split('.')[0]
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                chinese_font = font_name
                print(f'成功加载字体: {font_name}')
                break
            except Exception as e:
                print(f'加载字体失败 {font_path}: {e}')
                continue
    
    if not chinese_font:
        print('警告: 未找到中文字体，将使用默认字体')
        chinese_font = 'Helvetica'
    
    # 创建PDF
    output_path = r'D:\GPT\AI-demo\gongzhonghao\星佳人生指南_精美版.pdf'
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # 定义样式
    styles = getSampleStyleSheet()
    
    # 封面标题样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=chinese_font,
        fontSize=36,
        textColor=HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        leading=50
    )
    
    # 副标题样式
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=16,
        textColor=HexColor('#7F8C8D'),
        spaceAfter=20,
        alignment=TA_CENTER,
        leading=24
    )
    
    # 章节标题样式
    chapter_style = ParagraphStyle(
        'ChapterTitle',
        parent=styles['Heading2'],
        fontName=chinese_font,
        fontSize=22,
        textColor=HexColor('#2980B9'),
        spaceAfter=20,
        spaceBefore=30,
        leading=30
    )
    
    # 小节标题样式
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading3'],
        fontName=chinese_font,
        fontSize=16,
        textColor=HexColor('#34495E'),
        spaceAfter=12,
        spaceBefore=20,
        leading=22
    )
    
    # 正文样式
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=12,
        textColor=HexColor('#2C3E50'),
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=20,
        firstLineIndent=24
    )
    
    # 金句样式（引用框）
    quote_style = ParagraphStyle(
        'QuoteStyle',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=13,
        textColor=HexColor('#8E44AD'),
        spaceAfter=15,
        spaceBefore=15,
        leftIndent=30,
        rightIndent=30,
        leading=22,
        alignment=TA_LEFT
    )
    
    # 页脚样式
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=9,
        textColor=HexColor('#95A5A6'),
        alignment=TA_CENTER
    )
    
    story = []
    
    # ========== 封面 ==========
    story.append(Spacer(1, 8*cm))
    story.append(Paragraph('星佳人生指南', title_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph('从宁夏到深圳再到香港的孟母三迁之路', subtitle_style))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph('基于2019-2025年1268篇原创文章提炼', subtitle_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('星佳 · 爱米 著', subtitle_style))
    story.append(Spacer(1, 4*cm))
    
    # 封面金句
    cover_quote = ParagraphStyle(
        'CoverQuote',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=14,
        textColor=HexColor('#7F8C8D'),
        alignment=TA_CENTER,
        fontStyle='italic'
    )
    story.append(Paragraph('"人是目的，不是手段"', cover_quote))
    story.append(PageBreak())
    
    # ========== 目录 ==========
    story.append(Paragraph('目 录', chapter_style))
    story.append(Spacer(1, 1*cm))
    
    toc_items = [
        ('一、核心理念篇', '人生定位 · 行动哲学 · 学习之道'),
        ('二、家庭经营篇', '夫妻关系 · 亲子教育 · 家庭氛围'),
        ('三、事业发展篇', '创业心法 · 职业转型 · 工作态度'),
        ('四、资产配置篇', '房产投资 · 身份规划 · 风险管理'),
        ('五、生活智慧篇', '时间管理 · 人际交往 · 自我认知'),
        ('六、金句合集', 'AI时代 · 家庭 · 成长 · 选择'),
        ('七、年度关键词演变', '2020-2025轨迹'),
        ('八、给读者的10条建议', '可执行的清单'),
        ('附录：孟母三迁心法', '家庭教育实践录'),
    ]
    
    for title, subtitle in toc_items:
        story.append(Paragraph(title, section_style))
        story.append(Paragraph(subtitle, body_style))
        story.append(Spacer(1, 0.3*cm))
    
    story.append(PageBreak())
    
    # ========== 核心理念篇 ==========
    story.append(Paragraph('一、核心理念篇', chapter_style))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph('1. 人生定位', section_style))
    story.append(Paragraph(
        '"星佳是个小人物"——承认渺小，但不放弃成长。从宁夏到深圳再到香港，我始终记得自己是谁。不是大V，不是专家，只是一个愿意持续学习、记录生活的小人物。这种定位让我保持谦卑，也让我敢于尝试。',
        body_style
    ))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph('★ 人是目的，不是手段', quote_style))
    story.append(Paragraph(
        '技术再发达，最终也是为人服务。在AI时代，很多人担心被技术取代。但只要我们记住：技术是为了让人生活得更好，而不是让人成为技术的奴隶，就不会迷失方向。',
        body_style
    ))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph('★ 你的经历，你的故事，你的情感，这就是你的护城河', quote_style))
    story.append(Paragraph(
        'AI无法替代的真实人生。星佳写了6年公众号，写了1200多篇文章。如果让AI来模仿我的风格，它当然可以写得八九不离十。但它写不出我和爱米从宁夏到深圳再到香港的这段经历，写不出我们挤在自如合租屋里一个月3000块房租的日子，写不出深吹夫妇这个公众号一路走来的点点滴滴。',
        body_style
    ))
    
    story.append(Paragraph('2. 行动哲学', section_style))
    story.append(Paragraph('★ 焦虑本身没有用，行动才有', quote_style))
    story.append(Paragraph(
        '2023年ChatGPT刚火的时候，身边很多人都在焦虑。但我选择直接开始用，用到哪里不会了，再搜索一下怎么解决。先用起来，在用的过程中，你自然就会了。',
        body_style
    ))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph('★ 先上车，再换车', quote_style))
    story.append(Paragraph(
        '无论是买房、移民还是学习新技能，我的原则都是：先上车，再换车。你不先用起来，永远不知道这个东西能给你带来什么。深圳买房的上车门槛，真的不高。',
        body_style
    ))
    
    story.append(Paragraph('3. 学习之道', section_style))
    story.append(Paragraph('★ 门槛降低了，但要求提高了', quote_style))
    story.append(Paragraph(
        '以前学编程需要几年，现在用AI几天就能做出一个作品。但这不是说学习变简单了，而是要求提高了。以前只要会写代码，现在还要会提问、会判断、会整合。',
        body_style
    ))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph('★ 值钱的是提出好问题的能力，以及判断答案好坏的能力', quote_style))
    story.append(Paragraph(
        'AI时代，答案太容易获得了。真正值钱的是你能提出什么好问题，以及你能判断AI给的答案对不对、好不好。',
        body_style
    ))
    
    story.append(PageBreak())
    
    # ========== 家庭经营篇 ==========
    story.append(Paragraph('二、家庭经营篇', chapter_style))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph('1. 夫妻关系', section_style))
    story.append(Paragraph('★ 最好的夫妻关系是互相成全', quote_style))
    story.append(Paragraph(
        '爱米从银川的移动公司辞职来到深圳，我们一起从零开始。她负责家庭资产配置，我负责内容创作。两个人的认知同步，才能走得更远。',
        body_style
    ))
    
    story.append(Paragraph('2. 亲子教育', section_style))
    story.append(Paragraph(
        '★ AI可以给你答案，但不能代替你蹲下来，耐心地陪孩子看一条鱼',
        quote_style
    ))
    story.append(Paragraph(
        '带小太阳去菜市场，他用豆包问"鱼为什么能在水里呼吸"。AI给出了答案，但更重要的是，他是拉着爸爸的手，站在鱼摊前，亲眼看着那些活蹦乱跳的鱼。这种体验，是坐在电脑前问AI得不到的。',
        body_style
    ))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph('★ 所有的教育离不开父母的以身作则', quote_style))
    story.append(Paragraph(
        '你想让孩子成为什么样的人，首先父母先成为这样的人。父母好学、视学习为乐，孩子定尚学、以学习为乐。',
        body_style
    ))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        '★ 热爱指的就是，哪怕父母反复阻止你，也挡不住你想方设法要去做的事',
        quote_style
    ))
    story.append(Paragraph(
        '发现孩子的真正兴趣。小星星痴迷游戏和豆包里的推荐视频，但转念一想，自己的小时候也是很痴迷电脑的。可能"热爱"指的就是，哪怕父母反复阻止你，也挡不住你想方设法要去做的事。',
        body_style
    ))
    
    story.append(Paragraph('3. 家庭氛围', section_style))
    story.append(Paragraph('★ 平凡又幸福的一天', quote_style))
    story.append(Paragraph(
        '这是我最珍惜的生活状态。不是每天都轰轰烈烈，而是有家人陪伴，有事情可做，有希望在前面。',
        body_style
    ))
    
    story.append(PageBreak())
    
    # ========== 事业发展篇 ==========
    story.append(Paragraph('三、事业发展篇', chapter_style))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph('★ 极致的利他，才能极致的利己', quote_style))
    story.append(Paragraph(
        '孟母三迁一直秉承这个理念。不管是帮客户办理深圳落户，还是香港身份规划，我们都是先想怎么帮客户解决问题。客大客小，都会用心去做。顶级的商业思维是要做到：极致的利他，帮助别人获得财富，自己才会拥有财富。',
        body_style
    ))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph('★ 从0开始学编程的第X天', quote_style))
    story.append(Paragraph(
        '40岁开始学编程，很多人会觉得晚了。但我和小星星一起，用AI做出了贪吃蛇游戏。科技技术越普及，门槛越低，带来的生产力提升就是指数级增长。',
        body_style
    ))
    
    story.append(PageBreak())
    
    # ========== 资产配置篇 ==========
    story.append(Paragraph('四、资产配置篇', chapter_style))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph('★ 《六个早点和国际化》——给孩子更多选择', quote_style))
    story.append(Paragraph(
        '早点买房、早点落户、早点教育、早点国际化、早点学AI、早点记录。这六个"早点"构成了我们对未来的规划。',
        body_style
    ))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        '办理香港身份，不是为了逃离，而是为了给孩子多一个选择。可以使用ChatGPT，可以参加DSE考试，可以申请海外大学。选择权，才是最宝贵的资产。',
        body_style
    ))
    
    story.append(PageBreak())
    
    # ========== 金句合集 ==========
    story.append(Paragraph('五、金句合集', chapter_style))
    story.append(Spacer(1, 0.5*cm))
    
    quotes_by_category = [
        ('关于AI时代', [
            'AI不会替代程序员，但会用AI的程序员会替代不会用AI的程序员',
            '先当工具用，别想太多',
            '与其焦虑AI会替代什么，不如想想AI能让我们有更多时间去珍惜什么',
            '不是编程变简单了，是工具变强了',
        ]),
        ('关于家庭', [
            '人是目的，不是手段',
            '热爱指的就是，哪怕父母反复阻止你，也挡不住你想方设法要去做的事',
            '你的经历，你的故事，你的情感，这就是你的护城河',
        ]),
        ('关于成长', [
            '40岁开始学编程的第X天',
            '从宁夏到深圳和香港的孟母三迁之路',
            '只要定下了买房的目标，路就会越走越宽',
        ]),
    ]
    
    for category, quotes in quotes_by_category:
        story.append(Paragraph(category, section_style))
        for quote in quotes:
            story.append(Paragraph(f'• {quote}', quote_style))
        story.append(Spacer(1, 0.3*cm))
    
    story.append(PageBreak())
    
    # ========== 年度关键词演变 ==========
    story.append(Paragraph('六、年度关键词演变', chapter_style))
    story.append(Spacer(1, 0.5*cm))
    
    # 创建表格
    table_data = [['年份', '关键词', '阶段']]
    timeline = [
        ('2020', '深圳、房产、创业', '起步期'),
        ('2021', '香港、身份、教育', '稳步增长'),
        ('2022', '双城生活、跨境', '爆发期'),
        ('2023', '香港教育、DSE', '巅峰期'),
        ('2024', '创业、团队、客户', '调整期'),
        ('2025', 'AI编程、亲子', '新起点'),
    ]
    
    for year, keywords, stage in timeline:
        table_data.append([year, keywords, stage])
    
    table = Table(table_data, colWidths=[3*cm, 8*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2980B9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), chinese_font),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9FA')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#BDC3C7')),
        ('FONTNAME', (0, 1), (-1, -1), chinese_font),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), HexColor('#F8F9FA')]),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 1*cm))
    
    story.append(Paragraph(
        '趋势总结：房产博主 → 移民教育博主 → AI编程博主',
        body_style
    ))
    
    story.append(PageBreak())
    
    # ========== 10条建议 ==========
    story.append(Paragraph('七、给读者的10条建议', chapter_style))
    story.append(Spacer(1, 0.5*cm))
    
    advices = [
        '先用起来，别想太多 —— 不管学什么都不需要等准备好',
        '投资你的"人味" —— 多花时间陪家人，这是AI做不到的',
        '学习提问，而不是学习答案 —— AI时代最值钱的能力',
        '先上车，再换车 —— 买房、移民、换工作都是这个道理',
        '人是目的，不是手段 —— 技术再发达也是为人服务',
        '极致的利他，才能极致的利己 —— 商业的本质',
        '父母是孩子的镜像神经元 —— 你想让孩子成为什么样的人，先成为那样的人',
        '平凡又幸福的一天 —— 这就是生活的意义',
        '40岁开始学编程也不晚 —— 终身学习的态度',
        '你的经历就是你的护城河 —— 没有人能复制你的人生',
    ]
    
    for i, advice in enumerate(advices, 1):
        story.append(Paragraph(f'{i}. {advice}', body_style))
        story.append(Spacer(1, 0.2*cm))
    
    story.append(PageBreak())
    
    # ========== 附录 ==========
    story.append(Paragraph('附录：孟母三迁心法', chapter_style))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph(
        '孟母三迁，不只是地理上的搬家，而是为了给下一代创造更好的成长环境。从宁夏到深圳，再到香港——这是一个家庭对"什么是好的教育"持续探索的过程。',
        body_style
    ))
    story.append(Spacer(1, 0.5*cm))
    
    migrations = [
        ('第一迁：宁夏→深圳', '环境即教育', '打破认知天花板、敢于归零、目标感驱动'),
        ('第二迁：深圳→香港', '给孩子选择权', '身份规划、双城平衡、父母先行'),
        ('第三迁：传统→AI', '父母是最好的AI老师', '父母先学、AI亲子工具、培养人味'),
    ]
    
    for title, core, practice in migrations:
        story.append(Paragraph(title, section_style))
        story.append(Paragraph(f'核心心法：{core}', quote_style))
        story.append(Paragraph(f'实践要点：{practice}', body_style))
        story.append(Spacer(1, 0.5*cm))
    
    story.append(PageBreak())
    
    # ========== 封底 ==========
    story.append(Spacer(1, 10*cm))
    story.append(Paragraph('"与其焦虑AI会替代什么，', cover_quote))
    story.append(Paragraph('不如想想AI能让我们有更多时间去珍惜什么"', cover_quote))
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph('星佳 · 爱米', subtitle_style))
    story.append(Paragraph('从宁夏到深圳和香港的孟母三迁之路', subtitle_style))
    story.append(Paragraph('持续记录1268篇原创文章', subtitle_style))
    
    # 生成PDF
    doc.build(story)
    print(f'\n✅ PDF生成成功！')
    print(f'文件路径: {output_path}')
    print(f'文件大小: {os.path.getsize(output_path) / 1024:.2f} KB')

if __name__ == '__main__':
    create_chinese_pdf()
