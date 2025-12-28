import requests
import json

PACKAGE_ID = "fsis-quarterly-enforcement-reports"
API_URL = f"https://catalog.data.gov/api/3/action/package_show?id={PACKAGE_ID}"

try:
    print(f"Querying API: {API_URL}")
    r = requests.get(API_URL, timeout=10)
    data = r.json()
    
    if not data.get('success'):
        print("API call failed")
        exit()
        
    resources = data['result']['resources']
    print(f"\nFound {len(resources)} resources:")
    
    for res in resources:
        print(f"\nName: {res.get('name')}")
        print(f"Format: {res.get('format')}")
        print(f"URL: {res.get('url')}")
        
except Exception as e:
    print(f"Error: {e}")
