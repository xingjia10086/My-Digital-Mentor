# -*- coding: utf-8 -*-
import os
import re
import json

base_path = r'D:\GPT\AI-demo\gongzhonghao'

# 关键词提取
keywords_data = {}
timeline_events = []
characters = {}

for item in os.listdir(base_path):
    item_path = os.path.join(base_path, item)
    if os.path.isdir(item_path):
        for year_folder in ['2020', '2021', '2022', '2023', '2024', '2025']:
            year_path = os.path.join(item_path, year_folder)
            if os.path.isdir(year_path):
                files = [f for f in os.listdir(year_path) if f.endswith('.md')]
                # 每年读前15篇
                for filename in files[:15]:
                    file_path = os.path.join(year_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # 提取日期
                        date_match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
                        if date_match:
                            date = date_match.group(1)
                        else:
                            date = f'{year_folder}-01-01'
                        
                        # 提取标题
                        title_match = re.search(r'\]\s*(.+?)\.md', filename)
                        if title_match:
                            title = title_match.group(1)
                        else:
                            title = ''
                        
                        # 提取关键词（2-4字词）
                        words = re.findall(r'[\u4e00-\u9fa5]{2,4}', content)
                        stopwords = set(['的', '了', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '我们', '在', '让', '还', '可以', '就是', '但是', '因为', '所以', '如果', '虽然', '被', '把', '给', '对', '能', '而', '及', '与', '或', '然后', '这里', '这个', '那个', '一些', '这些', '那些', '这样', '那样', '之', '为', '以', '于', '那么', '什么', '怎么', '现在', '今天', '明天', '昨天', '今年', '去年', '时间', '时候', '地方', '东西', '事情', '工作', '生活', '觉得', '知道', '开始', '已经', '进行', '需要', '通过', '根据', '关于', '以及', '而且', '或者', '并且', '同时', '因此', '由于', '对于', '随着', '作为', '成为', '表示', '认为', '包括', '主要', '相关', '其中', '目前', '正在', '出现', '形成', '完成', '实现', '发展', '提供', '使用', '采用', '利用', '应用', '是指', '所谓', '尤其是', '特别是', '就是', '算是', '即使是', '尽管', '固然', '虽说', '且说', '话说', '换句话说', '也就是说', '等于是说', '相当于', '类似于', '例如', '比如', '譬如', '好比', '就像', '正如', '类似', '相似', '差不多', '几乎', '简直', '根本', '绝对', '完全', '实在', '确实', '的确', '真的', '非常', '十分', '相当', '比较', '稍微', '有点', '有些', '一方面', '另一方面', '首先', '其次', '再次', '最后', '一来', '二来', '在此之后', '在此之前', '除此之外', '除非', '除了', '只有', '只是', '只要', '只能', '只好', '不得不', '必须', '一定', '肯定', '必然', '必定', '难免', '未免', '不免', '不禁', '不由', '不得不', '偏偏', '恰好', '恰巧', '正好', '刚好', '适逢', '恰逢', '正当', '正值', '正在', '每当', '每逢', '每年', '每月', '每天', '每个', '所有', '一切', '全部', '整体', '部分', '局部', '全体', '整个', '各年', '各种', '各类', '各项', '各个', '各项', '各种', '各类'])
                        
                        for word in words:
                            if word not in stopwords and len(word) >= 2:
                                keywords_data[word] = keywords_data.get(word, 0) + 1
                        
                        # 提取人物
                        names = ['星佳', '爱米', '小星星', '小太阳', '孟母', '阿曾']
                        for name in names:
                            if name in content:
                                characters[name] = characters.get(name, 0) + content.count(name)
                        
                        # 提取时间线事件
                        keywords_timeline = ['香港', '深圳', '宁夏', '买房', '落户', '搬家', '创业', 'AI', '编程', '孩子', '教育', '身份']
                        for kw in keywords_timeline:
                            if kw in title or kw in content[:500]:
                                timeline_events.append({
                                    'date': date,
                                    'year': year_folder,
                                    'keyword': kw,
                                    'title': title[:50]
                                })
                                break
                                
                    except Exception as e:
                        pass
        
        # 保存结果
        result = {
            'keywords': sorted(keywords_data.items(), key=lambda x: x[1], reverse=True)[:100],
            'characters': sorted(characters.items(), key=lambda x: x[1], reverse=True),
            'timeline': timeline_events[:50]
        }
        
        with open(r'D:\GPT\AI-demo\gongzhonghao\analysis_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print('数据分析完成！')
        print(f'提取关键词: {len(keywords_data)} 个')
        print(f'提取人物: {len(characters)} 个')  
        print(f'提取时间线事件: {len(timeline_events)} 个')
        print('\nTOP 20 关键词:')
        for word, count in result['keywords'][:20]:
            print(f'  {word}: {count}')
        print('\n人物出现频率:')
        for name, count in result['characters']:
            print(f'  {name}: {count}次')
        print('\n时间线样本:')
        for event in result['timeline'][:10]:
            print(f"  {event['date']}: [{event['keyword']}] {event['title']}")
        break
