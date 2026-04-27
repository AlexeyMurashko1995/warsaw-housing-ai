import time
import csv
import requests
from bs4 import BeautifulSoup


# --- Configuration ---
target_url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?limit=36&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36'
}

apartments = []

# --- Network Request ---
for page in range(1, 6):
    current_url = f'{target_url}&page={page}'
    response = requests.get(current_url, headers=headers, timeout=10)
    print(f'Response status code: {response.status_code}') # Fixed typo 'statud'

    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('div', class_='css-1lyza52 eqir0f90')

    # --- Data Extraction Loop ---
    for listing in listings:
        # 1. Reset district for each iteration
        district_value = 'Unknown'
        district_tag = listing.find(class_='css-oxb2ca e1cuc5p50')

        if district_tag:
            clean_district = district_tag.text
            try:
                district_value = clean_district.split(',')[-3].strip()
            except IndexError:
                district_value = 'Unknown'

        # 2. Price Extraction & Validation
        price_tag = listing.find('span', class_='css-6t3bie')

        if price_tag and 'Zapytaj o cenę' not in price_tag.text:
            clean_price = price_tag.text
            price_value = clean_price.replace('\xa0', '').replace('zł', '').replace(',', '.')

            # Convert string -> float -> int
            final_price = int(float(price_value))

            # 3. Area Extraction
            area_tag = listing.find('dt', string='Cena za metr kwadratowy')

            if area_tag:
                raw_area = area_tag.find_next_sibling('dd').text.strip()
                clean_area = raw_area.split()[0].split('-')[0]

                try:
                    area_value = float(clean_area.replace(',', '.'))
                    # 4. Calculation: Price per Square Meter
                    price_per_me2 = round(final_price / area_value, 0)

                    # 5. Final Data Storage
                    apartments.append({
                        'price': final_price,
                        'area': area_value,
                        'district': district_value,
                        'price per meter 2': price_per_me2
                    })
                except ValueError:
                    print(f'Could not convert area: {clean_area}')

    # --- FIXED INDENTATION ---
    # This now runs once per page, not once per listing
    print(f'Page {page} finished. Waiting 2 seconds...')
    time.sleep(2)

# --- Data Persistence (CSV Export) ---
if apartments:
    filename = 'warsaw_apartments.csv'
    keys = apartments[0].keys()

    average_price = sum(flat['price'] for flat in apartments) / len(apartments)
    average_area = round(sum(flat['area'] for flat in apartments) / len(apartments), 2)
    average_price_per_meter_2 = round(sum(flat['price per meter 2'] for flat in apartments) / len(apartments), 2)

    print(f'Average flat price: {average_price:,.2f}')
    print(f'Average local area: {average_area}')
    print(f'Average price for m2: {average_price_per_meter_2}')

    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(apartments)
        print(f'SUCCESS: Saved {len(apartments)} records to {filename}')
    except PermissionError:
        print(f'ERROR: Close Excel! Python cannot write to {filename} while it is open.')
    except Exception as e:
        print(f'ERROR: Something went wrong: {e}')
else:
    print('FAILURE: No data collected. The list is empty.')


