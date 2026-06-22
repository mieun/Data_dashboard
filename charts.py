# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 저장 폴더 생성
save_dir = 'C:/Users/KOSTA/Desktop/claude-test/05_이미지자료'
os.makedirs(save_dir, exist_ok=True)

df = pd.read_csv('C:/Users/KOSTA/Desktop/claude-test/핀테크_정제완료.csv')

# ① 업종별 총 거래금액 막대그래프
fig, ax = plt.subplots(figsize=(10, 6))
업종별 = df.groupby('가맹점업종')['거래금액'].sum().sort_values(ascending=False)
bars = ax.bar(업종별.index, 업종별.values, color='#2563EB')
ax.set_title('업종별 총 거래금액', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('업종', fontsize=12)
ax.set_ylabel('거래금액 (원)', fontsize=12)
for bar, val in zip(bars, 업종별.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(업종별.values) * 0.01,
            f'{val:,.0f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(f'{save_dir}/01_업종별_총거래금액.png', dpi=150)
plt.close()
print('① 업종별 총 거래금액 막대그래프 저장 완료')

# ② 결제수단 비중 도넛차트
fig, ax = plt.subplots(figsize=(8, 8))
결제수단별 = df['결제수단'].value_counts()
colors = ['#2563EB', '#60A5FA', '#93C5FD', '#BFDBFE', '#DBEAFE']
wedges, texts, autotexts = ax.pie(
    결제수단별.values,
    labels=결제수단별.index,
    autopct='%1.1f%%',
    colors=colors,
    wedgeprops=dict(width=0.5),
    startangle=90
)
for text in texts:
    text.set_fontsize(12)
for autotext in autotexts:
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')
ax.set_title('결제수단 비중', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(f'{save_dir}/02_결제수단_비중.png', dpi=150)
plt.close()
print('② 결제수단 비중 도넛차트 저장 완료')

# ③ 월별 거래액 추이 선그래프
df['거래일시'] = pd.to_datetime(df['거래일시'])
df['월'] = df['거래일시'].dt.to_period('M')
월별 = df.groupby('월')['거래금액'].sum().sort_index()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(월별.index.astype(str), 월별.values, color='#2563EB', linewidth=2.5, marker='o', markersize=6)
ax.fill_between(range(len(월별)), 월별.values, alpha=0.15, color='#2563EB')
ax.set_title('월별 거래액 추이', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('월', fontsize=12)
ax.set_ylabel('거래금액 (원)', fontsize=12)
ax.set_xticks(range(len(월별)))
ax.set_xticklabels(월별.index.astype(str), rotation=45, ha='right')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e8:.1f}억'))
ax.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(f'{save_dir}/03_월별_거래액_추이.png', dpi=150)
plt.close()
print('③ 월별 거래액 추이 선그래프 저장 완료')

print(f'\n모든 차트가 {save_dir} 에 저장되었습니다.')
