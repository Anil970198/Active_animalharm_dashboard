import requests
from bs4 import BeautifulSoup

URL = "https://catalog.data.gov/dataset/fsis-quarterly-enforcement-reports"

try:
    print(f"Fetching {URL}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    print("\n--- EXTERNAL LINKS ---")
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith("http"):
            print(f"{href}")
            
except Exception as e:
    print(f"Error: {e}")
