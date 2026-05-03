import pandas as pd

df = pd.read_csv('warsaw_apartments.csv', encoding='utf-8-sig')

df['price_usd'] = df['price'] * 0.25
df = df.drop('price_usd', axis=1)

df = df.rename(columns={
    'district': 'area_name',
    'price per meter 2': 'price_m2'
})

min_price = df['price'].min()
result = df[df['price'] == min_price]

low_price_mokotów = df[(df['area_name'] == 'Mokotów') & (df['area'] <= 35) & (df['price'] < 700000)].reset_index(drop=True)
only_mokotów = df[df['area_name'] == 'Mokotów']
max_area_mokotów = only_mokotów['area'].max()

mean_price_warsaw = df['price_m2'].mean()
median_price_warsaw = df['price_m2'].median()
price_diff = mean_price_warsaw - median_price_warsaw

print(f'Lowest prices for apartments in Mokotów:\n{low_price_mokotów}')
print(f'The biggest apartment in Mokotów:\n{max_area_mokotów} m2')
print(f'Lowest price in Warsaw:\n{min_price} zł')
print(f'Mean price in Warsaw:\n{mean_price_warsaw:.2f} zł')
print(f'Median price in Warsaw:\n{median_price_warsaw:.2f} zł')
print(f'The gap between mean price and median price:\n{price_diff:.2f} zł')
