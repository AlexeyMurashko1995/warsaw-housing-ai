import pandas as pd

df = pd.read_csv('apartments_lab.csv', encoding='utf-8-sig')

df.head()
df.info()

df['price_usd'] = df['price'] * 0.25
df = df.drop('price_usd', axis=1)

df = df.rename(columns={
    'district': 'area_name',
    'price per meter 2': 'price_m2'
})

expensive_m2 = df.groupby('area_name')['price_m2'].mean()
expensive_m2 = expensive_m2.sort_values(ascending=False)

print(expensive_m2)