# O aplikaci / About application

**Česky:**
Tato aplikace je webová služba pro vyhledávání na Googlu. Uživatel může zadat klíčové slovní spojení
do formuláře na hlavní stránce, aplikace pak provede vyhledávání na Googlu a zobrazí přirozené výsledky
hledání na další stránce. Všechny výsledky se uloží jak do souboru ve formátu JSON, tak i do CSV souboru,
což umožňuje jejich strojové zpracování. Uživatel může přímo kliknout na odkazy ve výsledcích a navštívit
odpovídající stránky.

**English:**
This application is a web-based Google search service. The user can enter a keyword or phrase into the
form on the homepage, and the application will perform a Google search and display the natural search
results on the next page. All the results are saved in both a JSON file and a CSV file, allowing for
machine-readable processing. Users can click directly on the links in the results to visit the
corresponding pages.

**Jak aplikaci spustit / How to run the application:**

**1. Vytvoření virtuálního prostředí a instalace závislostí / Create a virtual environment and install dependencies:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Spuštění aplikace / Run the application:**
```bash
python search_app.py
```

**3. Přístup k aplikaci v prohlížeči / Access the application in your browser:
Otevřete prohlížeč a zadejte adresu: `http://127.0.0.1:5000`**


**Aplikaci můžete vyzkoušet online na/You can try the app online at
https://google-search-without-ads.onrender.com/**


