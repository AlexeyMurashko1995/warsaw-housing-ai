import requests
from bs4 import BeautifulSoup

def test_connection(url):
    print(f"--- Попытка подключиться к: {url} ---")

    # Заголовки, чтобы сайт думал, что мы человек, а не скрипт
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        # Делаем сам запрос
        response = requests.get(url, headers=headers, timeout=10)

        # Проверяем статус ответа
        if response.status_code == 200:
            print(f"✅ Успех! Сайт ответил кодом 200.")
            print(f"Длина полученных данных: {len(response.text)} символов.")
            return response.text
        else:
            print(f"❌ Ошибка: Сайт вернул код {response.status_code}")

    except Exception as e:
        print(f"⚠️ Произошла ошибка при подключении: {e}")

# Точка входа в программу (проверь двойные подчеркивания!)
if __name__ == "__main__":
    print("🚀 Скрипт запущен!")

    # Ссылка на раздел объявлений в Варшаве
    target_url = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa"

    # Запускаем проверку
    page_html = test_connection(target_url)

    if page_html:
        print("📡 Данные получены и готовы к обработке.")

    print("--- Работа скрипта завершена ---")