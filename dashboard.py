# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import streamlit as st

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title='핀테크 결제 대시보드', layout='wide')
st.title('핀테크 결제 대시보드')

@st.cache_data
def load_data():
    df = pd.read_csv('핀테크_정제완료.csv')
    df['거래일시'] = pd.to_datetime(df['거래일시'])
    df['월'] = df['거래일시'].dt.to_period('M').astype(str)
    return df

df = load_data()

# 사이드바 필터
st.sidebar.header('필터')
지역_목록 = ['전체'] + sorted(df['지역'].unique().tolist())
업종_목록 = ['전체'] + sorted(df['가맹점업종'].unique().tolist())
선택_지역 = st.sidebar.multiselect('지역', 지역_목록[1:], default=지역_목록[1:])
선택_업종 = st.sidebar.multiselect('업종', 업종_목록[1:], default=업종_목록[1:])

filtered = df[df['지역'].isin(선택_지역) & df['가맹점업종'].isin(선택_업종)]

# KPI 카드
st.subheader('핵심 지표')
c1, c2, c3, c4 = st.columns(4)
c1.metric('총 거래액', f"{filtered['거래금액'].sum():,.0f}원")
c2.metric('총 거래건수', f"{len(filtered):,}건")
c3.metric('평균 거래액', f"{filtered['거래금액'].mean():,.0f}원")
c4.metric('고객 수', f"{filtered['사용자ID'].nunique():,}명")

st.divider()

# 차트 3개
col1, col2, col3 = st.columns([2, 1.5, 2])

with col1:
    st.subheader('업종별 총 거래금액')
    업종별 = filtered.groupby('가맹점업종')['거래금액'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(업종별.index, 업종별.values, color='#2563EB')
    for bar, val in zip(bars, 업종별.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(업종별.values) * 0.01,
                f'{val/1e6:.1f}M', ha='center', va='bottom', fontsize=8)
    ax.set_ylabel('거래금액 (원)')
    ax.tick_params(axis='x', rotation=30)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}M'))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader('결제수단 비중')
    결제수단별 = filtered['결제수단'].value_counts()
    fig, ax = plt.subplots(figsize=(5, 4))
    colors = ['#2563EB', '#60A5FA', '#93C5FD', '#BFDBFE', '#DBEAFE']
    ax.pie(결제수단별.values, labels=결제수단별.index, autopct='%1.1f%%',
           colors=colors, wedgeprops=dict(width=0.5), startangle=90)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col3:
    st.subheader('월별 거래액 추이')
    월별 = filtered.groupby('월')['거래금액'].sum().sort_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(range(len(월별)), 월별.values, color='#2563EB', linewidth=2, marker='o', markersize=5)
    ax.fill_between(range(len(월별)), 월별.values, alpha=0.15, color='#2563EB')
    ax.set_xticks(range(len(월별)))
    ax.set_xticklabels(월별.index, rotation=45, ha='right', fontsize=7)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e8:.1f}억'))
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
