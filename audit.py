#!/usr/bin/env python3

import sqlite3

DB_PATH = 'project.db'

def audit_inventory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get all items that haven't been audited
        cursor.execute("SELECT id, name, count FROM item WHERE audited = FALSE OR audited IS NULL")
        items = cursor.fetchall()
        
        if not items:
            print("All items audited!")
            return
        
        print(f"\n{len(items)} items to audit.")
        print("-" * 50)
        
        for item_id, name, current_count in items:
            print(f"({current_count}) - {name}")
            
            while True:
                try:
                    user_input = input(": ").strip()
                    
                    if user_input.lower() == 'exit':
                        return
                    
                    if user_input == '':
                        break
                    
                    new_count = int(user_input)
                    if new_count < 0:
                        print("Quantity cannot be negative.")
                        continue
                    
                    cursor.execute("UPDATE item SET count = ? WHERE id = ?", (new_count, item_id))
                    break
                    
                except ValueError:
                    print("Invalid input.")
            
            # Mark as audited regardless of whether quantity was changed
            cursor.execute("UPDATE item SET audited = TRUE WHERE id = ?", (item_id,))
            conn.commit()
            print("-" * 30)
        
        print("Audit completed!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    except KeyboardInterrupt:
        print("\nAudit interrupted by user.")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    audit_inventory()

