import pandas as pd

# Load the dataset
df = pd.read_csv('warsaw-apartments.csv', encoding='utf-8-sig')

# Data cleaning: calculate and drop temporary column, rename districts
df['price_usd'] = df['price'] * 0.25
df = df.drop('price_usd', axis=1)

df = df.rename(columns={
    'district': 'area_name',
    'price per meter 2': 'price_m2'
})

# General statistics for the Warsaw market
min_price = df['price'].min()
mean_price_warsaw = df['price_m2'].mean()
median_price_warsaw = df['price_m2'].median()
price_diff = mean_price_warsaw - median_price_warsaw

# Specific analysis for Mokotów district
low_price_mokotów = df[(df['area_name'] == 'Mokotów') & (df['area'] <= 35) & (df['price'] < 700000)].reset_index(drop=True)
only_mokotów = df[df['area_name'] == 'Mokotów']
max_area_mokotów = only_mokotów['area'].max()

# Grouping by district to find price boundaries and average
grouped = df.groupby('area_name')
result_stats = grouped['price_m2'].agg(['min', 'max', 'mean'])

# Identifying expensive districts with mean price above 20,000 PLN
filtered_result = result_stats[result_stats['mean'] > 20000]

# Feature Engineering: Creating apartment size categories
df['size_category'] = pd.cut(df['area'],
                             bins=[0, 35, 65, 1000],
                             labels=['Small', 'Medium', 'Large'])

# Advanced grouping by both District and Size Category
grouped_2 = df.groupby(['area_name', 'size_category'])
price_mean_by_size = grouped_2['price'].mean()

# Printing results using single quotes for f-strings
print('--- Warsaw General Statistics ---')
print(f'Mean Price: {mean_price_warsaw:.2f} zł')
print(f'Median Price: {median_price_warsaw:.2f} zł')
print(f'Price Gap: {price_diff:.2f} zł\n')

print('--- Mokotów Insights ---')
print(f'The biggest apartment in Mokotów: {max_area_mokotów} m2')
print(f'Cheapest Mokotów listings:\n{low_price_mokotów.head()}\n')

print('--- High-end Districts (>20k mean) ---')
print(filtered_result)

print('\n--- Price Mean by Size Category ---')
print(price_mean_by_size.head(10))