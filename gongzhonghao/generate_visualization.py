# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 读取数据
with open(r'D:\GPT\AI-demo\gongzhonghao\analysis_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. 生成词频条形图（前20个关键词）
fig, ax = plt.subplots(figsize=(12, 8))
keywords = data['keywords'][:20]
words = [k[0] for k in keywords]
counts = [k[1] for k in keywords]

bars = ax.barh(range(len(words)), counts, color='#4A90E2')
ax.set_yticks(range(len(words)))
ax.set_yticklabels(words)
ax.invert_yaxis()
ax.set_xlabel('出现频率', fontsize=12)
ax.set_title('星佳公众号 TOP 20 关键词 (2020-2025)', fontsize=16, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 添加数值标签
for i, (bar, count) in enumerate(zip(bars, counts)):
    ax.text(count + 5, i, str(count), va='center', fontsize=10)

plt.tight_layout()
plt.savefig(r'D:\GPT\AI-demo\gongzhonghao\word_frequency.png', dpi=150, bbox_inches='tight')
print('词频图已保存: word_frequency.png')
plt.close()

# 2. 生成人物关系图（环形图）
fig, ax = plt.subplots(figsize=(10, 8))
characters = data['characters']
if characters:
    names = [c[0] for c in characters]
    values = [c[1] for c in characters]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    
    wedges, texts, autotexts = ax.pie(values, labels=names, autopct='%1.1f%%',
                                       colors=colors[:len(names)],
                                       startangle=90, textprops={'fontsize': 12})
    ax.set_title('星佳公众号人物出现频率分布', fontsize=16, fontweight='bold', pad=20)
    
    # 添加图例
    legend_labels = [f'{name}: {val}次' for name, val in characters]
    ax.legend(legend_labels, title="人物", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

plt.tight_layout()
plt.savefig(r'D:\GPT\AI-demo\gongzhonghao\character_distribution.png', dpi=150, bbox_inches='tight')
print('人物分布图已保存: character_distribution.png')
plt.close()

# 3. 生成时间线分布图（按年份统计事件类型）
fig, ax = plt.subplots(figsize=(14, 8))

timeline = data['timeline']
year_keyword_count = {}
for event in timeline:
    year = event['year']
    keyword = event['keyword']
    if year not in year_keyword_count:
        year_keyword_count[year] = {}
    year_keyword_count[year][keyword] = year_keyword_count[year].get(keyword, 0) + 1

# 准备堆叠条形图数据
years = sorted(year_keyword_count.keys())
all_keywords = list(set([k for yk in year_keyword_count.values() for k in yk.keys()]))
colors_map = plt.cm.Set3(range(len(all_keywords)))

bottom = [0] * len(years)
for idx, keyword in enumerate(all_keywords):
    values = [year_keyword_count[year].get(keyword, 0) for year in years]
    ax.bar(years, values, bottom=bottom, label=keyword, color=colors_map[idx])
    bottom = [b + v for b, v in zip(bottom, values)]

ax.set_xlabel('年份', fontsize=12)
ax.set_ylabel('文章数量', fontsize=12)
ax.set_title('星佳公众号主题演变时间线 (2020-2025)', fontsize=16, fontweight='bold', pad=20)
ax.legend(title='主题关键词', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(r'D:\GPT\AI-demo\gongzhonghao\timeline_evolution.png', dpi=150, bbox_inches='tight')
print('时间线图已保存: timeline_evolution.png')
plt.close()

# 4. 生成年度文章数量统计
fig, ax = plt.subplots(figsize=(12, 6))
year_counts = {'2020': 156, '2021': 177, '2022': 252, '2023': 266, '2024': 188, '2025': 88}
years = list(year_counts.keys())
counts = list(year_counts.values())

bars = ax.bar(years, counts, color=['#E74C3C', '#E67E22', '#F1C40F', '#27AE60', '#3498DB', '#9B59B6'])
ax.set_xlabel('年份', fontsize=12)
ax.set_ylabel('文章数量', fontsize=12)
ax.set_title('星佳公众号年度发文统计 (2020-2025)', fontsize=16, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 添加数值标签
for bar, count in zip(bars, counts):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
            f'{count}篇', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(r'D:\GPT\AI-demo\gongzhonghao\yearly_stats.png', dpi=150, bbox_inches='tight')
print('年度统计图已保存: yearly_stats.png')
plt.close()

print('\n所有可视化图表已生成完成！')
print('文件列表:')
print('1. word_frequency.png - 词频TOP20')
print('2. character_distribution.png - 人物关系分布')
print('3. timeline_evolution.png - 主题演变时间线')
print('4. yearly_stats.png - 年度发文统计')
