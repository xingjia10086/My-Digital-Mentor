# -*- coding: utf-8 -*-
import os
import re
import json

base_path = r'D:\GPT\AI-demo\gongzhonghao'

# 提取金句的函数
def extract_quotes(content):
    quotes = []
    
    # 匹配加粗的金句 **xxx**
    bold_pattern = r'\*\*(.+?)\*\*'
    bold_matches = re.findall(bold_pattern, content)
    for match in bold_matches:
        match_clean = match.strip()
        if 10 <= len(match_clean) <= 100 and '。' in match_clean:
            quotes.append(match_clean)
    
    # 匹配引用的金句
    quote_pattern = r'>\s*[""""](.+?)[""""]'
    quote_matches = re.findall(quote_pattern, content, re.DOTALL)
    for match in quote_matches:
        match_clean = match.strip()
        if 15 <= len(match_clean) <= 100:
            quotes.append(match_clean)
    
    return quotes

# 遍历文章提取金句
all_quotes = []
quote_sources = []

for item in os.listdir(base_path):
    item_path = os.path.join(base_path, item)
    if os.path.isdir(item_path):
        for year_folder in ['2020', '2021', '2022', '2023', '2024', '2025']:
            year_path = os.path.join(item_path, year_folder)
            if os.path.isdir(year_path):
                files = [f for f in os.listdir(year_path) if f.endswith('.md')]
                # 每年读前25篇
                for filename in files[:25]:
                    file_path = os.path.join(year_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        quotes = extract_quotes(content)
                        for q in quotes:
                            all_quotes.append(q)
                            quote_sources.append({
                                'quote': q,
                                'year': year_folder,
                                'file': filename[:50]
                            })
                    except Exception as e:
                        pass

# 去重并筛选
seen = set()
unique_quotes = []
for qs in quote_sources:
    q = qs['quote']
    if q not in seen and 15 <= len(q) <= 120:
        seen.add(q)
        unique_quotes.append(qs)

# 按年份分组
quotes_by_year = {}
for qs in unique_quotes:
    year = qs['year']
    if year not in quotes_by_year:
        quotes_by_year[year] = []
    quotes_by_year[year].append(qs['quote'])

# 保存结果
result = {
    'total': len(unique_quotes),
    'by_year': quotes_by_year,
    'all_quotes': [qs['quote'] for qs in unique_quotes]
}

with open(r'D:\GPT\AI-demo\gongzhonghao\quotes_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'共提取 {len(unique_quotes)} 条金句')
print('\n各年份分布:')
for year in sorted(quotes_by_year.keys()):
    print(f'  {year}: {len(quotes_by_year[year])}条')

print('\n样本金句（随机30条）：')
import random
samples = random.sample(unique_quotes, min(30, len(unique_quotes)))
for i, qs in enumerate(samples, 1):
    print(f'{i}. [{qs["year"]}] {qs["quote"][:80]}...' if len(qs["quote"]) > 80 else f'{i}. [{qs["year"]}] {qs["quote"]}')
