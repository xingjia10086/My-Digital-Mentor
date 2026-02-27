# -*- coding: utf-8 -*-
from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        if self.page_no() > 1:  # 封面不显示页眉
            self.set_font('Arial', '', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, '星佳人生指南 · 孟母三迁心法', 0, 0, 'L')
            self.cell(0, 10, f'第 {self.page_no()-1} 页', 0, 0, 'R')
            self.ln(15)
    
    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font('Arial', '', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, '基于2019-2025年1268篇原创文章整理', 0, 0, 'C')
    
    def chapter_title(self, title, level=1):
        if level == 1:
            self.set_font('Arial', 'B', 16)
            self.set_text_color(51, 51, 51)
            self.ln(10)
            self.cell(0, 10, title, 0, 1, 'L')
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)
        else:
            self.set_font('Arial', 'B', 13)
            self.set_text_color(70, 70, 70)
            self.ln(8)
            self.cell(0, 8, title, 0, 1, 'L')
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 6, body)
        self.ln()
    
    def quote_box(self, quote):
        self.set_fill_color(240, 248, 255)
        self.set_draw_color(100, 149, 237)
        self.set_line_width(0.5)
        self.cell(5)
        self.set_font('Arial', 'I', 11)
        self.set_text_color(60, 60, 60)
        self.multi_cell(180, 6, f'"{quote}"', 1, 'L', True)
        self.ln(5)

def create_pdf():
    pdf = PDF()
    pdf.add_page()
    
    # 封面
    pdf.set_font('Arial', 'B', 28)
    pdf.set_y(80)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(0, 15, '星佳人生指南', 0, 1, 'C')
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, '从宁夏到深圳再到香港的孟母三迁之路', 0, 1, 'C')
    pdf.ln(20)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, '基于2019-2025年1268篇原创文章提炼', 0, 1, 'C')
    pdf.cell(0, 8, '星佳 · 爱米 著', 0, 1, 'C')
    pdf.ln(30)
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 8, '"人是目的，不是手段"', 0, 1, 'C')
    
    # 目录页
    pdf.add_page()
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 15, '目 录', 0, 1, 'C')
    pdf.ln(10)
    
    contents = [
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
    
    for title, subtitle in contents:
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(51, 51, 51)
        pdf.cell(0, 10, title, 0, 1, 'L')
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 6, subtitle, 0, 1, 'L')
        pdf.ln(3)
    
    # 正文内容 - 核心理念篇
    pdf.add_page()
    pdf.chapter_title('一、核心理念篇', 1)
    
    pdf.chapter_title('1. 人生定位', 2)
    pdf.quote_box('星佳是个小人物 —— 承认渺小，但不放弃成长')
    pdf.chapter_body('从宁夏到深圳再到香港，我始终记得自己是谁。不是大V，不是专家，只是一个愿意持续学习、记录生活的小人物。这种定位让我保持谦卑，也让我敢于尝试。')
    
    pdf.quote_box('人是目的，不是手段 —— 技术再发达，最终也是为人服务')
    pdf.chapter_body('在AI时代，很多人担心被技术取代。但只要我们记住：技术是为了让人生活得更好，而不是让人成为技术的奴隶，就不会迷失方向。')
    
    pdf.chapter_title('2. 行动哲学', 2)
    pdf.quote_box('焦虑本身没有用，行动才有')
    pdf.chapter_body('2023年ChatGPT刚火的时候，身边很多人都在焦虑。但我选择直接开始用，用到哪里不会了，再搜索一下怎么解决。先用起来，在用的过程中，你自然就会了。')
    
    pdf.quote_box('先上车，再换车')
    pdf.chapter_body('无论是买房、移民还是学习新技能，我的原则都是：先上车，再换车。你不先用起来，永远不知道这个东西能给你带来什么。深圳买房的上车门槛，真的不高。')
    
    pdf.chapter_title('3. 学习之道', 2)
    pdf.quote_box('门槛降低了，但要求提高了')
    pdf.chapter_body('以前学编程需要几年，现在用AI几天就能做出一个作品。但这不是说学习变简单了，而是要求提高了。以前只要会写代码，现在还要会提问、会判断、会整合。')
    
    pdf.quote_box('值钱的是提出好问题的能力，以及判断答案好坏的能力')
    pdf.chapter_body('AI时代，答案太容易获得了。真正值钱的是你能提出什么好问题，以及你能判断AI给的答案对不对、好不好。')
    
    # 家庭经营篇
    pdf.add_page()
    pdf.chapter_title('二、家庭经营篇', 1)
    
    pdf.chapter_title('1. 夫妻关系', 2)
    pdf.quote_box('最好的夫妻关系是互相成全')
    pdf.chapter_body('爱米从银川的移动公司辞职来到深圳，我们一起从零开始。她负责家庭资产配置，我负责内容创作。两个人的认知同步，才能走得更远。')
    
    pdf.chapter_title('2. 亲子教育', 2)
    pdf.quote_box('AI可以给你答案，但不能代替你蹲下来，耐心地陪孩子看一条鱼')
    pdf.chapter_body('带小太阳去菜市场，他用豆包问"鱼为什么能在水里呼吸"。AI给出了答案，但更重要的是，他是拉着爸爸的手，站在鱼摊前，亲眼看着那些活蹦乱跳的鱼。')
    
    pdf.quote_box('所有的教育离不开父母的以身作则')
    pdf.chapter_body('你想让孩子成为什么样的人，首先父母先成为这样的人。父母好学、视学习为乐，孩子定尚学、以学习为乐。')
    
    pdf.chapter_title('3. 家庭氛围', 2)
    pdf.quote_box('平凡又幸福的一天')
    pdf.chapter_body('这是我最珍惜的生活状态。不是每天都轰轰烈烈，而是有家人陪伴，有事情可做，有希望在前面。')
    
    # 事业发展篇
    pdf.add_page()
    pdf.chapter_title('三、事业发展篇', 1)
    
    pdf.quote_box('顶级的商业思维是要做到：极致的利他，帮助别人获得财富，自己才会拥有财富')
    pdf.chapter_body('孟母三迁一直秉承这个理念。不管是帮客户办理深圳落户，还是香港身份规划，我们都是先想怎么帮客户解决问题。客大客小，都会用心去做。')
    
    pdf.quote_box('从0开始学编程的第X天')
    pdf.chapter_body('40岁开始学编程，很多人会觉得晚了。但我和小星星一起，用AI做出了贪吃蛇游戏。科技技术越普及，门槛越低，带来的生产力提升就是指数级增长。')
    
    # 资产配置篇
    pdf.add_page()
    pdf.chapter_title('四、资产配置篇', 1)
    
    pdf.quote_box('《六个早点和国际化》—— 给孩子更多选择')
    pdf.chapter_body('早点买房、早点落户、早点教育、早点国际化、早点学AI、早点记录。这六个"早点"构成了我们对未来的规划。')
    
    pdf.chapter_body('办理香港身份，不是为了逃离，而是为了给孩子多一个选择。可以使用ChatGPT，可以参加DSE考试，可以申请海外大学。选择权，才是最宝贵的资产。')
    
    # 生活智慧篇
    pdf.add_page()
    pdf.chapter_title('五、生活智慧篇', 1)
    
    pdf.quote_box('不能只工作没生活')
    pdf.chapter_body('为了给未来的AI助手提供更多真情实感的语料，我需要记录生活。写一篇记叙文，记录平凡又幸福的一天。')
    
    pdf.quote_box('30年来，不抽烟不喝酒也很少应酬')
    pdf.chapter_body('简单生活，给了我更多的时间和精力陪伴家人、学习新技能。几万个读者里，只有父母才是最铁的那几个。')
    
    # 金句合集
    pdf.add_page()
    pdf.chapter_title('六、金句合集', 1)
    
    pdf.chapter_title('关于AI时代', 2)
    quotes_ai = [
        'AI不会替代程序员，但会用AI的程序员会替代不会用AI的程序员',
        '先当工具用，别想太多',
        '与其焦虑AI会替代什么，不如想想AI能让我们有更多时间去珍惜什么',
        '不是编程变简单了，是工具变强了',
    ]
    for q in quotes_ai:
        pdf.quote_box(q)
    
    pdf.chapter_title('关于家庭', 2)
    quotes_family = [
        '人是目的，不是手段',
        '热爱指的就是，哪怕父母反复阻止你，也挡不住你想方设法要去做的事',
        '你的经历，你的故事，你的情感，这就是你的护城河',
    ]
    for q in quotes_family:
        pdf.quote_box(q)
    
    pdf.chapter_title('关于成长', 2)
    quotes_growth = [
        '40岁开始学编程的第X天',
        '从宁夏到深圳和香港的孟母三迁之路',
        '只要定下了买房的目标，路就会越走越宽',
    ]
    for q in quotes_growth:
        pdf.quote_box(q)
    
    # 年度关键词
    pdf.add_page()
    pdf.chapter_title('七、年度关键词演变', 1)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(80, 80, 80)
    
    timeline_data = [
        ('2020', '深圳、房产、创业', '起步期'),
        ('2021', '香港、身份、教育', '稳步增长'),
        ('2022', '双城生活、跨境', '爆发期'),
        ('2023', '香港教育、DSE', '巅峰期'),
        ('2024', '创业、团队、客户', '调整期'),
        ('2025', 'AI编程、亲子', '新起点'),
    ]
    
    for year, keywords, stage in timeline_data:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(20, 8, year, 0, 0, 'L')
        pdf.set_font('Arial', '', 11)
        pdf.cell(80, 8, keywords, 0, 0, 'L')
        pdf.set_text_color(100, 149, 237)
        pdf.cell(40, 8, stage, 0, 1, 'L')
        pdf.set_text_color(80, 80, 80)
    
    pdf.ln(10)
    pdf.chapter_body('趋势总结：房产博主 → 移民教育博主 → AI编程博主')
    
    # 10条建议
    pdf.add_page()
    pdf.chapter_title('八、给读者的10条建议', 1)
    
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
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(51, 51, 51)
        pdf.cell(0, 8, f'{i}. {advice}', 0, 1, 'L')
        pdf.ln(3)
    
    # 附录：孟母三迁心法
    pdf.add_page()
    pdf.chapter_title('附录：孟母三迁心法', 1)
    pdf.set_font('Arial', 'I', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 6, '孟母三迁，不只是地理上的搬家，而是为了给下一代创造更好的成长环境。从宁夏到深圳，再到香港——这是一个家庭对"什么是好的教育"持续探索的过程。')
    pdf.ln(10)
    
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(0, 10, '三迁心法', 0, 1, 'L')
    pdf.ln(5)
    
    migrations = [
        ('第一迁：宁夏→深圳', '环境即教育', '打破认知天花板、敢于归零、目标感驱动'),
        ('第二迁：深圳→香港', '给孩子选择权', '身份规划、双城平衡、父母先行'),
        ('第三迁：传统→AI', '父母是最好的AI老师', '父母先学、AI亲子工具、培养人味'),
    ]
    
    for title, core, practice in migrations:
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(70, 70, 70)
        pdf.cell(0, 8, title, 0, 1, 'L')
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(100, 149, 237)
        pdf.cell(0, 6, f'核心心法：{core}', 0, 1, 'L')
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 6, f'实践要点：{practice}', 0, 1, 'L')
        pdf.ln(5)
    
    # 封底
    pdf.add_page()
    pdf.set_y(100)
    pdf.set_font('Arial', 'I', 12)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, '"与其焦虑AI会替代什么，不如想想AI能让我们有更多时间去珍惜什么"', 0, 1, 'C')
    pdf.ln(20)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, '星佳 · 爱米', 0, 1, 'C')
    pdf.cell(0, 8, '从宁夏到深圳和香港的孟母三迁之路', 0, 1, 'C')
    pdf.cell(0, 8, '持续记录1268篇原创文章', 0, 1, 'C')
    
    # 保存
    output_path = r'D:\GPT\AI-demo\gongzhonghao\星佳人生指南_孟母三迁心法.pdf'
    pdf.output(output_path)
    print(f'PDF已生成: {output_path}')
    print(f'文件大小: {os.path.getsize(output_path)} 字节')

if __name__ == '__main__':
    create_pdf()
