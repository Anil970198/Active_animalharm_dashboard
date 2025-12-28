import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/violations.db")

def get_connection():
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Drop table to force schema update for prototype
    c.execute('DROP TABLE IF EXISTS violations')
    c.execute('''
        CREATE TABLE violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_name TEXT,
            violation_date TEXT,
            violation_type TEXT,
            location TEXT,
            summary TEXT,
            source_pdf TEXT,
            latitude REAL,
            longitude REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_violation(data):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO violations (facility_name, violation_date, violation_type, location, summary, source_pdf, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('facility_name', 'Unknown'),
        data.get('violation_date'),
        data.get('violation_type'),
        data.get('location'),
        data.get('summary'),
        data.get('source_pdf'),
        data.get('latitude'),
        data.get('longitude')
    ))
    conn.commit()
    conn.close()
    
def get_all_violations():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM violations ORDER BY violation_date DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]
