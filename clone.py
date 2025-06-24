#!/usr/bin/env python3

import sqlite3
import sys

DB_PATH = 'project.db'

if len(sys.argv) != 2:
    print("Usage: clone_item.py <item_id>")
    sys.exit(1)

try:
    item_id = int(sys.argv[1])
except ValueError:
    print("Invalid ID. Must be integer.")
    sys.exit(1)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name, size FROM item WHERE id = ?", (item_id,))
item = cursor.fetchone()

if not item:
    print(f"Item ID {item_id} not found")
    conn.close()
    sys.exit(1)

name, size = item
expiration = input("expiration_date? ").strip() or None

cursor.execute('''
INSERT INTO item (name, size, expiration_date)
VALUES (?, ?, ?)
''', (name, size, expiration))
conn.commit()
print(":)")
conn.close()

