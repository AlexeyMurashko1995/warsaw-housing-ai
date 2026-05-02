import pandas as pd


df = pd.read_csv('warsaw_apartments.csv', encoding='utf-8-sig')
df.head()
df.info()

print(df.head())
print(df.info())