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

    # Chrome settings for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless mode (will not open the window)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # Initializing headless Chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://www.google.com/search?q={search_query}")

    # Explicit waiting for results to load
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tF2Cxc')))
    except Exception as e:
        print(f"No results found: {e}")

    # wait for next 2 sec for JS
    time.sleep(2)

    # Extracting results
    search_results = []
    results = driver.find_elements(By.CLASS_NAME, 'tF2Cxc')

    for result in results:
        try:
            title_element = result.find_element(By.CSS_SELECTOR, 'h3')
            # get title
            title = title_element.get_attribute('innerText') if title_element else 'No Title Found'
            print(f"Title found: {title}")  # check the title listing
            link = result.find_element(By.TAG_NAME, 'a').get_attribute('href') # get link
            search_results.append({'title': title, 'link': link})
        except Exception as e:
            print(f"Error in getting the result: {e}")
            continue

    # close browser
    driver.quit()

    # Saving to JSON file
    with open('sleneium_google_search_results.json', 'w', encoding='utf-8') as json_file:
        json.dump(search_results, json_file, ensure_ascii=False, indent=4)

    # Saving to CSV file
    with open('selenimum_google_search_results.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['title', 'link'])
        writer.writeheader()
        writer.writerows(search_results)

    return render_template('search_result.html', results=search_results)

if __name__ == '__main__':
    app.run(debug=True)
