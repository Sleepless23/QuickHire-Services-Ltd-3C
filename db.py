import sqlite3
from datetime import datetime

DB_FILE = "quickhire.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_connection()
    cur = conn.cursor()

    #employees table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        role TEXT,
        department TEXT,
        hourly_rate REAL DEFAULT 0,
        contact TEXT
    )
    """)

    #attendance table: time_in stored as ISO string, time_out as ISO when signed out
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        date TEXT NOT NULL,            -- YYYY-MM-DD
        time_in TEXT NOT NULL,         -- ISO timestamp
        time_out TEXT,                 -- ISO timestamp or NULL
        hours_worked REAL DEFAULT 0,
        corrected INTEGER DEFAULT 0,
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    )
    """)

    #payroll table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS payroll (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        month INTEGER NOT NULL,     -- 1..12
        year INTEGER NOT NULL,
        hours_worked REAL,
        overtime_hours REAL,
        gross_pay REAL,
        deductions REAL,
        allowances REAL,
        net_pay REAL,
        created_at TEXT,
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    )
    """)

    conn.commit()
    conn.close()

#initialize DB on import
if __name__ == "__main__":
    initialize_db()
