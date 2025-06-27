import os.path
import sqlite3
from datetime import datetime
from pathlib import Path

# Create or connect to a DB file
db_path = os.path.join(str(Path.cwd()), "orangehrm_automation.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# Create a table for test results
cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_name TEXT,
        module TEXT,
        status TEXT,
        start_time TEXT,
        end_time TEXT,
        error_message TEXT,
        screenshot_path TEXT,
        browser TEXT,
        environment TEXT
    )
''')

conn.commit()

def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_name TEXT UNIQUE,
            run_status TEXT DEFAULT 'Not Run',
            result_status TEXT DEFAULT 'None'
        )
    ''')
    conn.commit()

create_table()

def log_test_result(test_name, module, status, start_time, end_time, error_message="", screenshot_path="", browser="chrome", environment="QA"):
    cursor.execute('''
        INSERT INTO test_results (
            test_name, module, status, start_time, end_time,
            error_message, screenshot_path, browser, environment
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (test_name, module, status, start_time, end_time,
          error_message, screenshot_path, browser, environment))

    conn.commit()
