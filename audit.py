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
            print("All items have already been audited!")
            return
        
        print(f"Found {len(items)} items to audit.")
        print("Enter new quantity for each item (press Enter to keep current, type 'exit' to quit):")
        print("-" * 50)
        
        for item_id, name, current_count in items:
            print(f"Item: {name}")
            print(f"Current quantity: {current_count}")
            
            while True:
                try:
                    user_input = input("New quantity: ").strip()
                    
                    if user_input.lower() == 'exit':
                        print("Audit aborted by user.")
                        return
                    
                    if user_input == '':
                        # Keep current quantity
                        print(f"Keeping quantity: {current_count}")
                        break
                    
                    # Try to convert to integer
                    new_count = int(user_input)
                    if new_count < 0:
                        print("Quantity cannot be negative. Please enter a valid number.")
                        continue
                    
                    # Update the quantity
                    cursor.execute("UPDATE item SET count = ? WHERE id = ?", (new_count, item_id))
                    print(f"Updated quantity to: {new_count}")
                    break
                    
                except ValueError:
                    print("Invalid input. Please enter a number, press Enter to keep current, or type 'exit' to quit.")
            
            # Mark as audited regardless of whether quantity was changed
            cursor.execute("UPDATE item SET audited = TRUE WHERE id = ?", (item_id,))
            conn.commit()
            print("-" * 30)
        
        print("Audit completed successfully!")
        
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

