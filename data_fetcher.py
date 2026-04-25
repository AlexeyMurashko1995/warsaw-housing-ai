import requests
from bs4 import BeautifulSoup

# Configuration
target_url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?limit=36&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36'
}

# Network Request
response = requests.get(target_url, headers=headers, timeout=10)
print(f'Response status code: {response.status_code}')

soup = BeautifulSoup(response.text, 'html.parser')

# Scoped Extraction
listings = soup.find_all('div', class_='css-1lyza52 eqir0f90')
apartments = []

for listing in listings:
    price_tag = listing.find('span', class_='css-6t3bie')

    # Validation: Ensure price exists and isn't 'Zapytaj o cenę'
    if price_tag and 'Zapytaj o cenę' not in price_tag.text:
        clean_price = price_tag.text
        price_value = clean_price.replace('\xa0', '').replace('zł', '')
        final_price = int(price_value)

        # Search for area label within the specific listing
        # FIX: Using 'za' (Polish) and single quotes
        area_tag = listing.find('dt', string='Cena za metr kwadratowy')

        if area_tag:
            raw_area = area_tag.find_next_sibling('dd').text.strip()
            # Handling ranges and cleaning
            clean_area = raw_area.split()[0].split('-')[0]

            try:
                area_value = float(clean_area.replace(',', '.'))
                # Storing bound data
                apartments.append({
                    'price': final_price,
                    'area': area_value
                })
            except ValueError:
                print(f'Could not convert area: {clean_area}')

# Final Result
print(f'Total entries in apartments list: {len(apartments)}')


# css-6t3bie - class for price
# 'div', class_='css-1lyza52 eqir0f90' - родительский тег и класс