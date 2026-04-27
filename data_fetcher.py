import time
import csv
import requests
from bs4 import BeautifulSoup


def extract_apartment_info(listing) -> dict:
    """Extracts data from a single apartment listing."""
    district_value = 'Unknown'
    district_tag = listing.find(class_='css-oxb2ca e1cuc5p50')

    if district_tag:
        clean_district = district_tag.text
        try:
            # Extract district from the address string
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

        # 3. Area Extraction via Sibling
        area_tag = listing.find('dt', string='Cena за метр kwadratowy')
        # If the tag above doesn't match exactly, we use the logic for area extraction
        # Note: In your specific case, you were searching for m2 price to get area.
        # Keeping your logic but cleaning variable names.

        area_tag = listing.find('dt', string='Cena za метр kwadratowy') or \
                   listing.find('dt', string='Cena za metr kwadratowy')

        if area_tag:
            raw_area = area_tag.find_next_sibling('dd').text.strip()
            clean_area = raw_area.split()[0].split('-')[0]

            try:
                area_value = float(clean_area.replace(',', '.'))
                # 4. Calculation: Price per Square Meter
                price_per_m2 = round(final_price / area_value, 0)

                # 5. Final Data Structure
                return {
                    'price': final_price,
                    'area': area_value,
                    'district': district_value,
                    'price per meter 2': price_per_m2
                }

            except ValueError:
                print(f'Could not convert area: {clean_area}')

    return None


def save_as_csv(data: list, filename: str):
    """Saves a list of dictionaries to a CSV file."""
    if not data:
        return

    keys = data[0].keys()
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print(f'SUCCESS: Saved {len(data)} records to {filename}')
    except PermissionError:
        print(f'ERROR: Close Excel! Cannot write to {filename} while it is open.')
    except Exception as e:
        print(f'ERROR: Unexpected error during saving: {e}')


# --- Configuration ---
target_url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?limit=36&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36'
}

apartments = []

# --- Network Request Loop ---
for page in range(1, 6):
    current_url = f'{target_url}&page={page}'
    response = requests.get(current_url, headers=headers, timeout=10)
    print(f'Response status code for Page {page}: {response.status_code}')

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all('div', class_='css-1lyza52 eqir0f90')

        # Process each listing on the current page
        for listing in listings:
            result = extract_apartment_info(listing)
            if result:
                apartments.append(result)
                print(result)

    print(f'Page {page} finished. Waiting 2 seconds...')
    time.sleep(2)

# --- Post-Processing & Analytics ---
if apartments:
    file_path = 'warsaw_apartments.csv'
    save_as_csv(apartments, file_path)

    # Calculate Market Averages
    avg_price = sum(flat['price'] for flat in apartments) / len(apartments)
    avg_area = round(sum(flat['area'] for flat in apartments) / len(apartments), 2)
    avg_price_m2 = round(sum(flat['price per meter 2'] for flat in apartments) / len(apartments), 2)

    print('\n' + '='*40)
    print('WARSAW REAL ESTATE REPORT')
    print('='*40)
    print(f'Average Price:{avg_price:,.2f} PLN')
    print(f'Average Area:{avg_area} m2')
    print(f'Average Price/m2:{avg_price_m2} PLN')
    print('='*40)
else:
    print('FAILURE: No data collected.')