from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import csv
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']

    # Nastavení prohlížeče Chrome pro režim headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Režim headless (nebude otevírat okno)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # Inicializace headless prohlížeče Chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://www.google.com/search?q={search_query}")

    # Explicitní čekání na načtení výsledků
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tF2Cxc')))
    except Exception as e:
        print(f"Výsledky nebyly nalezeny: {e}")

    # Počkej další 2 sekundy pro případ, že se JavaScript ještě načítá
    time.sleep(2)

    # Vyhledání všech výsledků na první stránce
    search_results = []
    results = driver.find_elements(By.CLASS_NAME, 'tF2Cxc')

    for result in results:
        try:
            title_element = result.find_element(By.CSS_SELECTOR, 'h3')
            # Získání textu titulu
            title = title_element.get_attribute('innerText') if title_element else 'No Title Found'
            print(f"Title found: {title}")  # Pro kontrolu výpisu titulu
            # Získání odkazu
            link = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
            search_results.append({'title': title, 'link': link})
        except Exception as e:
            print(f"Chyba při získávání výsledku: {e}")
            continue

    # Zavři prohlížeč po dokončení
    driver.quit()

    # Uložení do JSON souboru
    with open('sleneium_google_search_results.json', 'w', encoding='utf-8') as json_file:
        json.dump(search_results, json_file, ensure_ascii=False, indent=4)

    # Uložení do CSV souboru
    with open('selenimum_google_search_results.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['title', 'link'])
        writer.writeheader()
        writer.writerows(search_results)

    # Zobraz výsledky uživateli
    return render_template('search_result.html', results=search_results)

if __name__ == '__main__':
    app.run(debug=True)
