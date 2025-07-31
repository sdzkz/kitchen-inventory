#!/usr/bin/env python3

import sqlite3
import sys

DB_PATH = 'project.db'

def delete_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get current count
    cursor.execute('SELECT name, count FROM item WHERE id = ?', (item_id,))
    result = cursor.fetchone()
    
    if not result:
        print(f"Item with id {item_id} not found")
        conn.close()
        return
    
    name, current_count = result
    new_count = current_count - 1
    
    # If count would be 0 or less, ask for confirmation
    if new_count <= 0:
        response = input(f"purge? ").strip().lower()
        if response == 'y':
            cursor.execute('DELETE FROM item WHERE id = ?', (item_id,))
            print(f"{name} deleted")
        else:
            cursor.execute('UPDATE item SET count = 0 WHERE id = ?', (item_id,))
    else:
        # Just reduce count by 1
        cursor.execute('UPDATE item SET count = ? WHERE id = ?', (new_count, item_id))
        print(f"{new_count} left")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./delete.py <item_id>")
        sys.exit(1)
    
    try:
        item_id = int(sys.argv[1])
        delete_item(item_id)
    except ValueError:
        print("Error: Item ID must be a number")
        sys.exit(1)
