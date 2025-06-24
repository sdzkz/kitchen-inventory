#!/usr/bin/env python3

import sqlite3
import json

DB_PATH = 'project.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM item")
items = cursor.fetchall()

columns = [col[0] for col in cursor.description]
inventory = [dict(zip(columns, item)) for item in items]

print(json.dumps(inventory, indent=2))
conn.close()
