# Animal Welfare Dashboard (India)

A transparency tool that monitors and visualizes animal welfare violations across India.
It scrapes data from the **Animal Welfare Board of India (AWBI)** and maps cruelty cases (illegal slaughter, neglect, etc.) to their respective cities.

![Dashboard Preview](frontend/public/map_preview.png)

## Features
*   **Real-time Scraping**: Fetches the latest cruelty status reports from `awbi.gov.in`.
*   **Interactive Map**: Visualizes violations across major Indian cities (Delhi, Mumbai, Ghaziabad, etc.).
*   **Cluster Jitter**: Intelligently scatters stacked data points to show the true volume of cases in a single city.
*   **Tech Stack**: Next.js (Frontend), Python FastAPI (Backend), SQLite (Database).

## Setup & Running

### 1. Backend (Python)
```bash
cd backend
# Create virtual env (if not exists)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn server:app --reload
```
API runs at: `http://127.0.0.1:8000`

### 2. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
Dashboard runs at: `http://localhost:3000`

## Data Sources
*   **Primary**: [Animal Welfare Board of India (AWBI)](https://awbi.gov.in/view/index/cruelty-cases)
*   **Visualization**: OpenStreetMap / Leaflet

## License
MIT
