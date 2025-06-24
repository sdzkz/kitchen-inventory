#!/usr/bin/env python3
import sqlite3

def list_items():
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, size, expiration_date FROM item ORDER BY id")
    items = cursor.fetchall()
    conn.close()
    
    if not items:
        print("No items in inventory")
        return
    
    # Prepare data with placeholders for None values
    data = []
    for item in items:
        id, name, size, exp_date = item
        data.append((
            str(id),
            name or 'N/A',
            size or 'N/A',
            exp_date or 'N/A'
        ))
    
    # Find max widths for each column
    col_widths = [2, 4, 4, 15]  # Min widths for ID, Name, Size, Exp Date
    for row in data:
        for i, value in enumerate(row):
            if len(value) > col_widths[i]:
                col_widths[i] = len(value)
    
    # Create format string with dynamic widths
    fmt = (
        f"{{:<{col_widths[0]}}}  "
        f"{{:<{col_widths[1]}}}  "
        f"{{:<{col_widths[2]}}}  "
        f"{{:<{col_widths[3]}}}"
    )
    
    # Print header
    print(fmt.format("ID", "Name", "Size", "Expiration Date"))
    print("-" * (sum(col_widths) + 6))  # 6 = 3 spaces between columns
    
    # Print rows
    for row in data:
        print(fmt.format(*row))

if __name__ == "__main__":
    list_items()

