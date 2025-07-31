#!/usr/bin/env python3

import sqlite3
import sys

def delete_item(item_id):
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM item WHERE id = ?", (item_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./delete.py ID")
        sys.exit(1)
    
    try:
        item_id = int(sys.argv[1])
        deleted = delete_item(item_id)
        print(f"{item_id} deleted" if deleted else "No item found with that ID")
    except ValueError:
        print("ID must be an integer")
        sys.exit(1)
