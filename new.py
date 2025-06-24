#!/usr/bin/env python3

import sqlite3
import sys

DB_PATH = 'project.db'

if '--quick' in sys.argv:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    count = 1
    while True:
        name = input(f"item {count}: ").strip()
        if name == 'exit':
            break
        if not name:
            continue
        cursor.execute('INSERT INTO item (name) VALUES (?)', (name,))
        conn.commit()
        count += 1
    conn.close()
else:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    name = input("name? ").strip()
    if not name:
        sys.exit(0)
    size = input("size? ").strip() or None
    expiration = input("expiration_date? ").strip() or None
    cursor.execute('''
    INSERT INTO item (name, size, expiration_date)
    VALUES (?, ?, ?)
    ''', (name, size, expiration))
    conn.commit()
    print(":)")
    conn.close()

