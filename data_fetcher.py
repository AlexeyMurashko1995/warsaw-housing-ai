import csv
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
    # 1. Reset district for each iteration to avoid data ghosting
    district_value = 'Unknown'
    district_tag = listing.find(class_='css-oxb2ca e1cuc5p50')

    if district_tag:
        clean_district = district_tag.text
        # Logic: Extracting district from address string (e.g., 'Mokotów')
        try:
            district_value = clean_district.split(',')[-3].strip()
            print(f'District found: {district_value}')
        except IndexError:
            district_value = 'Unknown'

    # 2. Price Extraction & Validation
    price_tag = listing.find('span', class_='css-6t3bie')

    if price_tag and 'Zapytaj o cenę' not in price_tag.text:
        # Handling non-breaking spaces, currency symbols, and decimal commas
        clean_price = price_tag.text
        price_value = clean_price.replace('\xa0', '').replace('zł', '').replace(',', '.')

        # Convert string -> float -> int to handle decimal prices like '877471,34'
        final_price = int(float(price_value))

        # 3. Area Extraction
        area_tag = listing.find('dt', string='Cena за metr kwadratowy') # Note: 'Cena za...' is standard on site

        if area_tag:
            raw_area = area_tag.find_next_sibling('dd').text.strip()
            # Handling ranges (e.g., '50-60 m2') and splitting units
            clean_area = raw_area.split()[0].split('-')[0]

            try:
                area_value = float(clean_area.replace(',', '.'))
                # 4. Calculation: Price per Square Meter
                price_per_m2 = round(final_price / area_value, 0)

                # 5. Final Data Storage
                apartments.append({
                    'price': final_price,
                    'area': area_value,
                    'district': district_value,
                    'price_per_m2': price_per_m2
                })
            except ValueError:
                print(f'Warning: Could not convert area value: {clean_area}')

# --- Final Results Output ---
print('\n--- EXTRACTION COMPLETE ---')
print(f'Total apartments collected: {len(apartments)}')

# --- Data Persistence (CSV Export) ---
if apartments:
    filename = 'warsaw_apartments.csv'
    # Use keys from the first dictionary as CSV headers
    keys = apartments[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(apartments)

    print(f'Data successfully saved to: {filename}')
else:
    print('No data to save. The apartments list is empty.')