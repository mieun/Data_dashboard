# -*- coding: utf-8 -*-
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('C:/Users/KOSTA/Desktop/claude-test/01_핀테크결제_dirty.csv')

print('=== 기본 정보 ===')
print(f'총 행 수: {len(df)}')
print(f'컬럼: {list(df.columns)}')

print()
print('=== 결측치 ===')
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({'결측치 수': missing, '결측치 비율(%)': missing_pct})
print(missing_df[missing_df['결측치 수'] > 0].to_string())

print()
print('=== 완전 중복 행 ===')
print(f'중복 행 수: {df.duplicated().sum()}')

print()
print('=== 거래금액 이상치 ===')
print(df['거래금액'].describe().to_string())
print(f'음수 거래금액: {(df["거래금액"] < 0).sum()}건')
print(f'결측 거래금액: {df["거래금액"].isnull().sum()}건')

print()
print('=== 거래일시 형식 ===')
slash = df['거래일시'].str.contains('/').sum()
hyphen = df['거래일시'].str.contains('-').fillna(False).sum()
print(f'슬래시(/) 형식: {slash}건')
print(f'하이픈(-) 형식: {hyphen}건')
