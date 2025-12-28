import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://www.fsis.usda.gov/inspection/compliance-enforcement/enforcement-actions/enforcement-reports"
HOMEPAGE = "https://www.fsis.usda.gov"

def test_url(name, url, headers=None):
    print(f"\nTesting {name}...")
    try:
        s = requests.Session()
        s.headers.update(headers or {})
        response = s.get(url, timeout=10, verify=False)
        print(f"Status: {response.status_code}")
        print(f"Content-Length: {len(response.content)}")
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False

# 1. Test Homepage (often easier to hit)
test_url("Homepage (Standard UA)", HOMEPAGE, {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

# 2. Test Deep Link with current headers
test_url("Report Page (Standard UA)", URL, {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
})

# 3. Test as Googlebot (sometimes whitelisted)
test_url("Report Page (Googlebot)", URL, {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
})

# 4. Test as bare python (sometimes 'User-Agent' header presence triggers blocks if it looks fake)
test_url("Report Page (No UA)", URL, {})
