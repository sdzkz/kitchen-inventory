#!/usr/bin/env python3
import sqlite3

def initialize_database():
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS item (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_added TEXT DEFAULT CURRENT_TIMESTAMP,
        name TEXT NOT NULL,
        size TEXT,
        expiration_date TEXT,
        percent_remaining REAL
    )
    ''')
    
    # Add new column if it doesn't exist
    cursor.execute("PRAGMA table_info(item)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'percent_remaining' not in columns:
        cursor.execute("ALTER TABLE item ADD COLUMN percent_remaining REAL")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
