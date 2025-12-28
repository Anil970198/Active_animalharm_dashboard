from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import scrape, parse, db, mock_data

# ... (omitted code)

import os

app = FastAPI(title="Transparency Dashboard API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    db.init_db()

@app.get("/")
def read_root():
    return {"message": "Transparency Dashboard API is running"}

@app.get("/api/violations")
def get_violations():
    """
    Get all processed violations from the database.
    """
    return db.get_all_violations()

from fastapi import BackgroundTasks

@app.post("/api/trigger-scrape")
def trigger_scrape(background_tasks: BackgroundTasks, limit: int = 3):
    """
    Triggers data pipeline in background.
    """
    background_tasks.add_task(run_pipeline, limit)
    return {"message": "Scraping started in background. Refresh in a minute."}

def run_pipeline(limit: int):
    try:
        # 1. Scrape (Returns list of violation dicts directly)
        try:
            violations = scrape.fetch_enforcement_reports()
        except Exception as e:
            print(f"Scrape failed: {e}")
            violations = []

        if not violations:
            print("No violations found.")
            return

        # 2. Save directly
        count = 0
        for v in violations:
            db.save_violation(v)
            count += 1
            
        print(f"Pipeline complete. Saved {count} records.")

    except Exception as e:
        print(f"Pipeline error: {e}")
