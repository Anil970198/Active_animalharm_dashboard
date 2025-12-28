import requests

SEARCH_URL = "https://catalog.data.gov/api/3/action/package_search"
PARAMS = {
    "q": "FSIS",
    "rows": 50
}

try:
    print(f"Searching data.gov for FSIS datasets...")
    r = requests.get(SEARCH_URL, params=PARAMS, timeout=15)
    data = r.json()
    
    results = data['result']['results']
    print(f"Found {len(results)} datasets. Checking for non-blocked URLs...\n")
    
    found_good = False
    for ds in results:
        for res in ds['resources']:
            url = res.get('url', '')
            # We are looking for URLs that do NOT start with the blocked domain
            if "fsis.usda.gov" not in url:
                print(f"Dataset: {ds['title']}")
                print(f"Resource: {res['name']}")
                print(f"Format: {res['format']}")
                print(f"URL: {url}")
                print("-" * 40)
                found_good = True
                
    if not found_good:
        print("No resources found outside fsis.usda.gov domain.")
        
except Exception as e:
    print(f"Error: {e}")
