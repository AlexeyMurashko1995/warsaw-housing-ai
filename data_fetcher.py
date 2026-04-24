import requests
from bs4 import BeautifulSoup


target_url = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36'
}

response = requests.get(target_url, headers=headers, timeout=10)
print(f'Response status code: {response.status_code}')

soup = BeautifulSoup(response.text, 'html.parser')
prices_all = soup.find_all('span', class_='css-6t3bie')

prices_list = []

for price in prices_all:
    if 'Zapytaj o cenę' in price.text:
        continue
    else:
        current_price = price.text
        clean_price = current_price.replace('\xa0', '').replace('zł', '')
        final_price = int(clean_price)
        if final_price > 100000:
            prices_list.append(final_price)

print(f'Average price: {sum(prices_list)/len(prices_list):.0f} zł')