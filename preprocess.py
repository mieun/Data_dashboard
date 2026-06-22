# -*- coding: utf-8 -*-
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('C:/Users/KOSTA/Desktop/claude-test/01_핀테크결제_dirty.csv')
before = len(df)
print(f'처리 전 행 수: {before}')

# 1) 완전 중복 행 제거
df = df.drop_duplicates()
print(f'1) 중복 제거 후: {len(df)}행 (제거: {before - len(df)}건)')

# 2) '연령대','지역','결제수단' 결측치 최빈값으로 채우기
for col in ['연령대', '지역', '결제수단']:
    mode_val = df[col].mode()[0]
    missing_cnt = df[col].isnull().sum()
    df[col] = df[col].fillna(mode_val)
    print(f'2) {col} 결측치 {missing_cnt}건 → 최빈값({mode_val})으로 대체')

# 3) 거래금액이 비었거나 음수인 행 제거
before_step3 = len(df)
df = df[df['거래금액'].notna() & (df['거래금액'] >= 0)]
print(f'3) 거래금액 결측/음수 제거 후: {len(df)}행 (제거: {before_step3 - len(df)}건)')

# 4) '결제수단' 앞뒤 공백 제거
df['결제수단'] = df['결제수단'].str.strip()
print(f'4) 결제수단 공백 제거 완료')

# 5) 거래일시 날짜 형식 통일 (YYYY-MM-DD HH:MM:SS)
df['거래일시'] = pd.to_datetime(df['거래일시'], format='mixed', dayfirst=False)
df['거래일시'] = df['거래일시'].dt.strftime('%Y-%m-%d %H:%M:%S')
print(f'5) 거래일시 형식 통일 완료')

# 저장
df.to_csv('C:/Users/KOSTA/Desktop/claude-test/핀테크_정제완료.csv', index=False, encoding='utf-8-sig')

after = len(df)
print()
print('=== 처리 결과 요약 ===')
print(f'처리 전 행 수: {before}')
print(f'처리 후 행 수: {after}')
print(f'총 제거된 행: {before - after}건')
print()
print('=== 남은 결측치 ===')
remaining = df.isnull().sum()
print(remaining[remaining > 0].to_string() if remaining.sum() > 0 else '결측치 없음')
