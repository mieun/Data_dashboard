# -*- coding: utf-8 -*-
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

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
선택_지역 = st.sidebar.multiselect('지역', sorted(df['지역'].unique()), default=sorted(df['지역'].unique()))
선택_업종 = st.sidebar.multiselect('업종', sorted(df['가맹점업종'].unique()), default=sorted(df['가맹점업종'].unique()))

filtered = df[df['지역'].isin(선택_지역) & df['가맹점업종'].isin(선택_업종)]

# KPI 카드
st.subheader('핵심 지표')
c1, c2, c3, c4 = st.columns(4)
c1.metric('총 거래액', f"{filtered['거래금액'].sum():,.0f}원")
c2.metric('총 거래건수', f"{len(filtered):,}건")
c3.metric('평균 거래액', f"{filtered['거래금액'].mean():,.0f}원")
c4.metric('고객 수', f"{filtered['사용자ID'].nunique():,}명")

st.divider()

col1, col2, col3 = st.columns([2, 1.5, 2])

with col1:
    st.subheader('업종별 총 거래금액')
    업종별 = filtered.groupby('가맹점업종')['거래금액'].sum().reset_index().sort_values('거래금액', ascending=False)
    fig = px.bar(업종별, x='가맹점업종', y='거래금액', text_auto='.2s', color_discrete_sequence=['#2563EB'])
    fig.update_layout(showlegend=False, xaxis_title='', yaxis_title='거래금액(원)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader('결제수단 비중')
    결제수단별 = filtered['결제수단'].value_counts().reset_index()
    결제수단별.columns = ['결제수단', '건수']
    fig = go.Figure(go.Pie(
        labels=결제수단별['결제수단'], values=결제수단별['건수'],
        hole=0.5, marker_colors=['#2563EB','#60A5FA','#93C5FD','#BFDBFE','#DBEAFE']
    ))
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.subheader('월별 거래액 추이')
    월별 = filtered.groupby('월')['거래금액'].sum().reset_index().sort_values('월')
    fig = px.line(월별, x='월', y='거래금액', markers=True, color_discrete_sequence=['#2563EB'])
    fig.update_layout(xaxis_title='', yaxis_title='거래금액(원)')
    st.plotly_chart(fig, use_container_width=True)
