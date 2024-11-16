import time
from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import json
import csv

# Creates a Flask instance for our application
app = Flask(__name__)


@app.route('/')
def index():
    """
    homepage, defines the URL witch will be displayed by GET method
    :return: base.html
    """
    return render_template('base.html')


@app.route('/search', methods=['POST'])
def search():
    """
    search processing by POST method
    :return: Extracts the title <h3> and link <a> for each result and adds them to the list of results (search_results).
    """
    search_query = request.form['search_query']
    google_url = f"https://www.google.com/search?q={search_query}"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

    response = requests.get(google_url, headers=headers)
    time.sleep(2)
    google_response = BeautifulSoup(response.text, 'html.parser')

    # Google blocking check
    if "captcha" in response.text.lower() or "please verify" in response.text.lower() or "Pokud nebude během pár sekund přesměrováni, klikněte prosím" in response.text.lower():
        print("Google may have blocked your request with a CAPTCHA or other block.")
    else:
        print("No CAPTCHA or other block detected, proceeding with normal parsing.")

    # Extracting results
    search_results = [] # list
    for search_reslut in google_response.find_all('div', class_='tF2Cxc'): # tF2Cxc is class element witch google use for organic searching result
        try:
            title = search_reslut.find('h3').text if search_reslut.find('h3') else 'No Title Found'
            link = search_reslut.find('a')['href'] if search_reslut.find('a') else 'No Link Found'
            search_results.append({'title': title, 'link': link}) # save as dictionary
        except AttributeError as e:
            print(f"Chyba při extrakci výsledku: {e}")
            continue

    save_results_to_files(search_results, 'soup_google_search_results.json', 'soup_google_search_results.csv')

    return render_template('search_result.html', results=search_results)


def save_results_to_files(results, json_filename, csv_filename):
    """
    Saves search results to both a JSON and a CSV file.

    :param results: List of dictionaries containing search results. Each dictionary should have keys 'title' and 'link'.
    :param json_filename: soup_google_search_results.json
    :param csv_filename: soup_google_search_results.csv
    :return: None. This function does not return anything, it only saves results to files.
    """
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    # Uložení do CSV souboru
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['title', 'link'])
        writer.writeheader()
        writer.writerows(results)


if __name__ == '__main__':
    app.run(debug=True)
