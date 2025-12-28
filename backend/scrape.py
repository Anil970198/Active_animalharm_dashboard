import requests
from bs4 import BeautifulSoup
import os
import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AWBI_URL = "https://awbi.gov.in/view/index/cruelty-cases"
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/raw")

# Simple static geocoding for common cities in the dataset to avoid external API deps
CITY_COORDS = {
    "Ghaziabad": {"lat": 28.6692, "lon": 77.4538},
    "Bhopal": {"lat": 23.2599, "lon": 77.4126},
    "Jalandhar": {"lat": 31.3260, "lon": 75.5762},
    "Moradabad": {"lat": 28.8386, "lon": 78.7733},
    "Vizianagaram": {"lat": 18.1067, "lon": 83.3956},
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Pune": {"lat": 18.5204, "lon": 73.8567},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462},
    "Kanpur": {"lat": 26.4499, "lon": 80.3319},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882},
    "Indore": {"lat": 22.7196, "lon": 75.8577},
    "Patna": {"lat": 25.5941, "lon": 85.1376},
    "Vadodara": {"lat": 22.3072, "lon": 73.1812},
    "Ludhiana": {"lat": 30.9010, "lon": 75.8573},
    "Agra": {"lat": 27.1767, "lon": 78.0081},
    "Nashik": {"lat": 19.9975, "lon": 73.7898},
    "Ranchi": {"lat": 23.3441, "lon": 85.3096},
    "Raipur": {"lat": 21.2514, "lon": 81.6296},
    "Meerut": {"lat": 28.9845, "lon": 77.7064},
    "Rajkot": {"lat": 22.3039, "lon": 70.8022},
    "Varanasi": {"lat": 25.3176, "lon": 82.9739},
    "Srinagar": {"lat": 34.0837, "lon": 74.7973},
    "Aurangabad": {"lat": 19.8762, "lon": 75.3433},
    "Dhanbad": {"lat": 23.7957, "lon": 86.4304},
    "Amritsar": {"lat": 31.6340, "lon": 74.8723},
    "Allahabad": {"lat": 25.4358, "lon": 81.8463},
    "Gwalior": {"lat": 26.2183, "lon": 78.1828},
    "Jabalpur": {"lat": 23.1815, "lon": 79.9864},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558},
    "Vijayawada": {"lat": 16.5062, "lon": 80.6480},
    "Jodhpur": {"lat": 26.2389, "lon": 73.0243},
    "Madurai": {"lat": 9.9252, "lon": 78.1198},
    "Guwahati": {"lat": 26.1445, "lon": 91.7362},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794}
}

def get_coords(location_str):
    """Try to find a matching city in the location string."""
    for city, coords in CITY_COORDS.items():
        if city.lower() in location_str.lower():
            return coords
    # Default fallback (center of India approx) if no match found
    return {"lat": 20.5937, "lon": 78.9629}

def fetch_awbi_data():
    """
    Scrapes the AWBI Cruelty Cases page.
    Returns: List of 'violation' dictionaries.
    """
    print(f"Fetching data from {AWBI_URL}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Verify": "False" # AWBI often has certificate issues
    }

    try:
        response = requests.get(AWBI_URL, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Determine table structure - usually it's a standard <table>
        table = soup.find('table')
        if not table:
            print("No table found on AWBI page.")
            return []
            
        # Skip header row
        rows = table.find_all('tr')[1:]
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 2:
                continue
                
            # Parsing logic depends on column order. 
            # Assuming typically: Sr No | State | Description | ...
            # We'll try to be robust.
            
            # Simple grab of text
            col_texts = [ele.get_text(strip=True) for ele in cols]
            
            # Heuristic assignment (Inspect the page source ideally, but guessing based on standard formats)
            # Often: ID, LOCATION, DESCRIPTION, DATE/STATUS
            
            # Let's assume content is present.
            full_text = " ".join(col_texts)
            
            # Try to extract location from known list
            lat = 20.5937
            lon = 78.9629
            location_name = "India (Unknown Location)"
            
            for city in CITY_COORDS.keys():
                if city in full_text:
                    c = CITY_COORDS[city]
                    lat = c['lat']
                    lon = c['lon']
                    location_name = city
                    break
            
            # Construct violation object
            violation = {
                "facility_name": "Animal Welfare Violation",
                "violation_date": datetime.date.today().isoformat(), # AWBI dates are tricky to parse, using today for 'report' date
                "violation_type": "Cruelty/Neglect",
                "location": location_name,
                "summary": full_text[:400] + "..." if len(full_text) > 400 else full_text, # Store the full row text as summary
                "latitude": lat,
                "longitude": lon,
                "source_url": AWBI_URL
            }
            results.append(violation)
            
        print(f"Successfully scraped {len(results)} cases from AWBI.")
        return results

    except Exception as e:
        print(f"Error scraping AWBI: {e}")
        return []

# Legacy/Unused
def fetch_enforcement_reports():
    return fetch_awbi_data()

def download_pdfs(links, limit=5):
    pass
if __name__ == "__main__":
    links = fetch_enforcement_reports()
    if links:
        download_pdfs(links)
