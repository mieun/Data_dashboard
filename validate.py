# -*- coding: utf-8 -*-
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('C:/Users/KOSTA/Desktop/claude-test/핀테크_정제완료.csv')

print('=== 거래금액 통계 (describe) ===')
print(df['거래금액'].describe().to_string())

print()
print('=== 결제수단 value_counts ===')
print(df['결제수단'].value_counts().to_string())

print()
print('=== 이상값 점검 ===')
print(f'음수 거래금액: {(df["거래금액"] < 0).sum()}건')
print(f'0원 거래금액: {(df["거래금액"] == 0).sum()}건')
print(f'거래금액 상위 5건:')
print(df.nlargest(5, '거래금액')[['거래일시', '가맹점업종', '거래금액', '결제수단']].to_string(index=False))

print()
print('=== 결측치 최종 확인 ===')
missing = df.isnull().sum()
print(missing[missing > 0].to_string() if missing.sum() > 0 else '결측치 없음')

print()
print('=== 결제수단 고유값 (공백 잔여 확인) ===')
print(df['결제수단'].unique())

print()
print('=== 거래일시 형식 샘플 ===')
print(df['거래일시'].head(5).to_string())
