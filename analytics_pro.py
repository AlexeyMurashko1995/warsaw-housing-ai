import pandas as pd


df = pd.read_csv('warsaw_apartments.csv', encoding='utf-8-sig')

df.head()
df.info()

bialoleka_filtered = df[(df['district'] == 'Białołęka') & (df['price'] > 400000) & (df['price'] < 600000)]

best_deals = bialoleka_filtered.sort_values(by='price per meter 2', ascending=True)
best_deals = best_deals.reset_index(drop=True)

all_bialoleka = df[df['district'] == 'Białołęka']
average_price = all_bialoleka['price per meter 2'].mean()

print(f'Average price in Białołęka: {average_price:.2f} zł/m2')
print(f'Total suitable variants found: {len(best_deals)}')
print('Top 5 best deals:')
print(best_deals.head())