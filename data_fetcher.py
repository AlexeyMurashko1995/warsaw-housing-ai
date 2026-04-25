import requests
from bs4 import BeautifulSoup

# --- Configuration ---
target_url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?limit=36&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36'
}

# --- Network Request ---
response = requests.get(target_url, headers=headers, timeout=10)
print(f'Response status code: {response.status_code}')

soup = BeautifulSoup(response.text, 'html.parser')
listings = soup.find_all('div', class_='css-1lyza52 eqir0f90')
apartments = []

# --- Data Extraction Loop ---
for listing in listings:
    # 1. Reset district for each iteration
    district_value = 'Unknown'
    district_tag = listing.find(class_='css-oxb2ca e1cuc5p50')

    if district_tag:
        clean_district = district_tag.text
        # Logic: Extracting district from address string
        district_value = clean_district.split(',')[-3].strip()
        print(f'District found: {district_value}')

    # 2. Price Extraction & Validation
    price_tag = listing.find('span', class_='css-6t3bie')

    if price_tag and 'Zapytaj o cenę' not in price_tag.text:
        clean_price = price_tag.text
        price_value = clean_price.replace('\xa0', '').replace('zł', '')
        final_price = int(price_value)

        # 3. Area Extraction
        area_tag = listing.find('dt', string='Cena za metr kwadratowy')

        if area_tag:
            raw_area = area_tag.find_next_sibling('dd').text.strip()
            # Logic: Handling numeric ranges and splitting units
            clean_area = raw_area.split()[0].split('-')[0]

            try:
                area_value = float(clean_area.replace(',', '.'))
                # 4. Final Data Storage
                apartments.append({
                    'price': final_price,
                    'area': area_value,
                    'district': district_value
                })
            except ValueError:
                print(f'Could not convert area: {clean_area}')

# --- Output ---
print('--- FINAL RESULTS ---')
print(apartments)
print(f'Total apartments collected: {len(apartments)}')