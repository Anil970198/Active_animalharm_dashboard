import requests

TARGET_URL = "https://www.fsis.usda.gov/inspection/compliance-enforcement/enforcement-actions/enforcement-reports"
CDX_API = "http://web.archive.org/cdx/search/cdx"

params = {
    "url": TARGET_URL,
    "output": "json",
    "limit": 1,
    "filter": "statuscode:200" # Only find successful captures
}

print(f"Finding latest snapshot for {TARGET_URL}...")
try:
    r = requests.get(CDX_API, params=params, timeout=15)
    data = r.json()
    
    if data and len(data) > 1:
        # data[0] is header, data[1] is the record
        # Format: [urlkey, timestamp, original, mimetype, statuscode, digest, length]
        timestamp = data[1][1]
        original = data[1][2]
        archive_url = f"https://web.archive.org/web/{timestamp}/{original}"
        print(f"\nFOUND SNAPSHOT: {archive_url}")
    else:
        print("No snapshot found.")
        
except Exception as e:
    print(f"Error: {e}")
