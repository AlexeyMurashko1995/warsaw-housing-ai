import requests


target_url = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36'
}

response = requests.get(target_url, headers=headers, timeout=10)
print(f'Response status code: {response.status_code}')