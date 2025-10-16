#!/usr/bin/env python3

import sqlite3
import sys

DB_PATH = 'project.db'

def edit_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM item WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    
    if not item:
        print(f"ID {item_id} not found")
        conn.close()
        return
    
    print(f"\033[36m---------- ID:{item_id} ----------\033[0m")
    columns = ["id", "date_added", "name", "size", "expiration_date", "percent_remaining"]
    for idx, col in enumerate(columns):
        value = item[idx]
        if value is None:
            value = "\033[33mNULL\033[0m"
        print(f"{value} \033[35m{col}\033[0m")
    
    updates = {}
    for col in columns:
        if col in ["id", "date_added"]:
            continue
            
        new_val = input(f"{col}: ").strip()
        if new_val:
            if col == "percent_remaining":
                try:
                    percent_val = float(new_val)
                    if not (0 <= percent_val <= 100):
                        print("Percent must be 0-100. Skipping.")
                        continue
                    updates[col] = percent_val
                except ValueError:
                    print("Invalid number. Skipping.")
                    continue
            elif new_val.lower() == "null":
                updates[col] = None
            else:
                updates[col] = new_val
    
    if updates:
        set_clause = ", ".join([f"{k} = ?" for k in updates])
        cursor.execute(f"UPDATE item SET {set_clause} WHERE id = ?", 
                      (*updates.values(), item_id))
        conn.commit()
    
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: edit.py <item_id>")
        sys.exit(1)
    
    try:
        item_id = sys.argv[1]
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print()
        if item_id == "0":
            cursor.execute("SELECT MAX(id) FROM item")
            max_id = cursor.fetchone()[0]
            if not max_id:
                print("No items found")
                conn.close()
                sys.exit(1)
            item_id = max_id
        else:
            item_id = int(item_id)
        conn.close()
        edit_item(item_id)
        print()        
    except ValueError:
        print("Invalid ID. Must be integer or 0.")
