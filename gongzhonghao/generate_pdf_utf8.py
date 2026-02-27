# -*- coding: utf-8 -*-
from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', '', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, 'Xingjia Life Guide', 0, new_x='LMARGIN', new_y='NEXT', align='L')
            self.cell(0, 10, f'Page {self.page_no()-1}', 0, new_x='RIGHT', new_y='TOP', align='R')
            self.ln(15)
    
    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font('helvetica', '', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, 'Based on 1268 articles (2019-2025)', 0, align='C')

def create_simple_pdf():
    pdf = PDF()
    pdf.add_page()
    
    # 封面 - 使用英文
    pdf.set_font('helvetica', 'B', 28)
    pdf.set_y(80)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(0, 15, 'XINGJIA LIFE GUIDE', 0, new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.set_font('helvetica', '', 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, 'From Ningxia to Shenzhen to Hong Kong', 0, new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(20)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 8, 'Based on 1268 original articles (2019-2025)', 0, new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.cell(0, 8, 'By Xingjia & Aimi', 0, new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(30)
    pdf.set_font('helvetica', 'I', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 8, '"People are the end, not the means"', 0, new_x='LMARGIN', new_y='NEXT', align='C')
    
    # 目录
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 18)
    pdf.cell(0, 15, 'CONTENTS', 0, new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(10)
    
    contents = [
        ('1. Core Philosophy', 'Life positioning, Action philosophy, Learning'),
        ('2. Family Management', 'Marriage, Parenting, Family atmosphere'),
        ('3. Career Development', 'Entrepreneurship, Career change, Work attitude'),
        ('4. Asset Allocation', 'Real estate, Identity planning, Risk management'),
        ('5. Life Wisdom', 'Time management, Relationships, Self-awareness'),
        ('6. Golden Quotes', 'AI era, Family, Growth, Choices'),
        ('7. Annual Keywords', '2020-2025 Evolution'),
        ('8. 10 Recommendations', 'Actionable checklist'),
        ('Appendix: Mencius Mother Method', 'Family education practice'),
    ]
    
    for title, subtitle in contents:
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(51, 51, 51)
        pdf.cell(0, 10, title, 0, new_x='LMARGIN', new_y='NEXT')
        pdf.set_font('helvetica', '', 10)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 6, subtitle, 0, new_x='LMARGIN', new_y='NEXT')
        pdf.ln(3)
    
    # 核心章节
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(0, 10, '1. CORE PHILOSOPHY', 0, new_x='LMARGIN', new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    sections = [
        ('Life Positioning', [
            '"Xingjia is a small person" - Admitting smallness, but never giving up growth',
            '"People are the end, not the means" - Technology serves people, not the other way around',
            '"Your experiences, stories, and emotions are your moat" - What AI cannot replicate',
        ]),
        ('Action Philosophy', [
            '"Anxiety is useless, only action counts"',
            '"Get on the bus first, then change buses" - Whether buying houses, immigrating, or learning',
            '"Use it first, you\'ll naturally learn in the process"',
        ]),
        ('Learning Principles', [
            '"The threshold has been lowered, but the requirements have increased"',
            '"What\'s valuable is the ability to ask good questions and judge answers"',
        ]),
    ]
    
    for title, points in sections:
        pdf.set_font('helvetica', 'B', 13)
        pdf.set_text_color(70, 70, 70)
        pdf.cell(0, 8, title, 0, new_x='LMARGIN', new_y='NEXT')
        pdf.ln(3)
        
        for point in points:
            pdf.set_fill_color(240, 248, 255)
            pdf.set_font('helvetica', 'I', 10)
            pdf.set_text_color(60, 60, 60)
            pdf.multi_cell(0, 6, f'  "{point}"', fill=True)
            pdf.ln(3)
    
    # 家庭章节
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, '2. FAMILY MANAGEMENT', 0, new_x='LMARGIN', new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    family_quotes = [
        ('Marriage', '"The best relationship is mutual fulfillment"'),
        ('Parenting', '"AI can give you answers, but cannot replace you kneeling down to patiently watch a fish with your child"'),
        ('Family Atmosphere', '"All education depends on parents setting an example"'),
        ('Daily Life', '"Ordinary yet happy days" - The most precious state of life'),
    ]
    
    for category, quote in family_quotes:
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_text_color(70, 70, 70)
        pdf.cell(0, 8, category, 0, new_x='LMARGIN', new_y='NEXT')
        pdf.set_fill_color(255, 250, 240)
        pdf.set_font('helvetica', 'I', 10)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 6, f'  {quote}', fill=True)
        pdf.ln(5)
    
    # 金句合集
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, '6. GOLDEN QUOTES COLLECTION', 0, new_x='LMARGIN', new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    all_quotes = [
        'AI won\'t replace programmers, but programmers who use AI will replace those who don\'t',
        'Use it as a tool first, don\'t overthink',
        'Instead of worrying about what AI will replace, think about what more time AI can give you to cherish',
        'Programming hasn\'t gotten easier, tools have gotten stronger',
        'Get on the bus first, then change buses',
        'People are the end, not the means',
        'Passion means that even if parents repeatedly stop you, you still find ways to do it',
        'Your experiences are your moat',
        '40 years old, day X of learning programming',
        'The journey from Ningxia to Shenzhen to Hong Kong',
        'Extreme altruism leads to extreme self-interest',
        'Among tens of thousands of readers, only parents are the most loyal',
    ]
    
    for i, quote in enumerate(all_quotes, 1):
        pdf.set_fill_color(240, 248, 255)
        pdf.set_font('helvetica', 'I', 10)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(10)
        pdf.multi_cell(170, 6, f'{i}. "{quote}"', fill=True)
        pdf.ln(2)
    
    # 年度关键词
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, '7. ANNUAL KEYWORDS EVOLUTION', 0, new_x='LMARGIN', new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    timeline = [
        ('2020', 'Shenzhen, Real estate, Startup', 'Starting period'),
        ('2021', 'Hong Kong, Identity, Education', 'Steady growth'),
        ('2022', 'Dual-city life, Cross-border', 'Explosion period'),
        ('2023', 'HK education, DSE', 'Peak period'),
        ('2024', 'Entrepreneurship, Team, Clients', 'Adjustment period'),
        ('2025', 'AI programming, Parent-child', 'New starting point'),
    ]
    
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(20, 8, 'Year', 0)
    pdf.cell(80, 8, 'Keywords', 0)
    pdf.cell(50, 8, 'Stage', 0, new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)
    
    for year, keywords, stage in timeline:
        pdf.set_font('helvetica', '', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(20, 8, year, 0)
        pdf.cell(80, 8, keywords, 0)
        pdf.set_text_color(100, 149, 237)
        pdf.cell(50, 8, stage, 0, new_x='LMARGIN', new_y='NEXT')
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 11)
    pdf.set_text_color(70, 70, 70)
    pdf.cell(0, 8, 'Evolution: Real estate blogger -> Immigration educator -> AI programming blogger', 0, new_x='LMARGIN', new_y='NEXT')
    
    # 10条建议
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, '8. 10 RECOMMENDATIONS FOR READERS', 0, new_x='LMARGIN', new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    advices = [
        'Use it first, don\'t overthink - No need to be fully prepared to start',
        'Invest in your "human touch" - Spend time with family, what AI cannot do',
        'Learn to ask questions, not just answers - Most valuable skill in AI era',
        'Get on the bus first, then change buses - For houses, immigration, jobs',
        'People are the end, not the means - Technology serves people',
        'Extreme altruism creates extreme self-interest - Business essence',
        'Parents are children\'s mirror neurons - Be who you want them to become',
        'Ordinary yet happy days - Meaning of life',
        '40 is not too late to learn programming - Lifelong learning attitude',
        'Your experiences are your moat - No one can copy your life',
    ]
    
    for i, advice in enumerate(advices, 1):
        pdf.set_font('helvetica', 'B', 10)
        pdf.set_text_color(51, 51, 51)
        pdf.multi_cell(0, 8, f'{i}. {advice}')
        pdf.ln(2)
    
    # 附录
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, 'APPENDIX: MENCIUS MOTHER METHOD', 0, new_x='LMARGIN', new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'I', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 6, 'Mencius\' mother moving three times is not just geographical relocation, but creating a better growth environment for the next generation. From Ningxia to Shenzhen to Hong Kong - this is a family\'s continuous exploration of "what is good education".')
    pdf.ln(10)
    
    migrations = [
        ('First Migration: Ningxia to Shenzhen', 'Environment is education', 'Break cognitive ceilings, dare to start from zero, goal-driven'),
        ('Second Migration: Shenzhen to Hong Kong', 'Give children choices', 'Identity planning, dual-city balance, parents go first'),
        ('Third Migration: Traditional to AI', 'Parents are the best AI teachers', 'Parents learn first, AI parenting tools, cultivate human touch'),
    ]
    
    for title, core, practice in migrations:
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(70, 70, 70)
        pdf.cell(0, 8, title, 0, new_x='LMARGIN', new_y='NEXT')
        pdf.set_font('helvetica', '', 10)
        pdf.set_text_color(100, 149, 237)
        pdf.cell(0, 6, f'Core: {core}', 0, new_x='LMARGIN', new_y='NEXT')
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 6, f'Practice: {practice}', 0, new_x='LMARGIN', new_y='NEXT')
        pdf.ln(5)
    
    # 封底
    pdf.add_page()
    pdf.set_y(100)
    pdf.set_font('helvetica', 'I', 12)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, '"Instead of worrying about what AI will replace,', 0, new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.cell(0, 10, 'think about what more time AI can give you to cherish"', 0, new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(20)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 8, 'Xingjia · Aimi', 0, new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.cell(0, 8, 'From Ningxia to Shenzhen to Hong Kong', 0, new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.cell(0, 8, '1268 articles and counting', 0, new_x='LMARGIN', new_y='NEXT', align='C')
    
    # 保存
    output_path = r'D:\GPT\AI-demo\gongzhonghao\Xingjia_Life_Guide.pdf'
    pdf.output(output_path)
    print(f'PDF generated: {output_path}')
    print(f'File size: {os.path.getsize(output_path)} bytes')

if __name__ == '__main__':
    create_simple_pdf()
