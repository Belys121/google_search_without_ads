document.getElementById('searchForm').addEventListener('submit', function() {
            // Zobrazí zprávu o načítání
            document.getElementById('loadingMessage').style.display = 'block';
            // Deaktivuje tlačítko "Search"
            document.getElementById('searchButton').disabled = true;
        });