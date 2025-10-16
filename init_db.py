#!/usr/bin/env python3

import sqlite3
import sys

DB_PATH = 'project.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Step 1: Try to create the table with all columns (safe for new DBs)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size TEXT,
            expiration_date DATE,
            percent_remaining REAL,
            count INTEGER NOT NULL DEFAULT 1
        )
    """)

    # Step 2: Check existing columns
    cursor.execute("PRAGMA table_info(item)")
    columns = [info[1] for info in cursor.fetchall()]

    # Step 3: Add missing columns if needed
    if 'percent_remaining' not in columns:
        print("Adding 'percent_remaining' column...")
        cursor.execute("ALTER TABLE item ADD COLUMN percent_remaining REAL")

    if 'count' not in columns:
        print("Adding 'count' column...")
        cursor.execute("ALTER TABLE item ADD COLUMN count INTEGER NOT NULL DEFAULT 1")

    # Add audited column if it doesn't exist
    if 'audited' not in columns:
        print("Adding 'audited' column...")
        cursor.execute("ALTER TABLE item ADD COLUMN audited BOOLEAN DEFAULT FALSE")

    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()

