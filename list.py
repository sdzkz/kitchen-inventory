#!/usr/bin/env python3
import sqlite3
import sys

def list_items(show_deleted=False):
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()

    if show_deleted:
        cursor.execute("SELECT id, name, size, expiration_date, count FROM item ORDER BY id")
    else:
        cursor.execute("SELECT id, name, size, expiration_date, count FROM item WHERE count > 0 ORDER BY id")

    items = cursor.fetchall()
    conn.close()
    
    if not items:
        print("No items in inventory")
        return
    
    # Prepare data with placeholders for None values
    data = []
    for item in items:
        id, name, size, exp_date, count = item
        data.append((
            str(id),
            name or 'N/A',
            size or 'N/A',
            exp_date or 'N/A',
            str(count)
        ))
    
    # Find max widths for each column
    col_widths = [2, 4, 4, 15, 5]  # Min widths for ID, Name, Size, Exp Date, Count
    for row in data:
        for i, value in enumerate(row):
            if len(value) > col_widths[i]:
                col_widths[i] = len(value)
    
    # Create format string with dynamic widths
    fmt = (
        f"{{:<{col_widths[0]}}}  "
        f"{{:<{col_widths[1]}}}  "
        f"{{:<{col_widths[2]}}}  "
        f"{{:<{col_widths[3]}}}  "
        f"{{:<{col_widths[4]}}}"
    )
    
    # Print header
    print(fmt.format("ID", "Name", "Size", "Expiration Date", "Count"))
    print("-" * (sum(col_widths) + 8))  # 8 = 4 spaces between columns
    
    # Print rows
    for row in data:
        print(fmt.format(*row))

if __name__ == "__main__":
    show_deleted = '--show-deleted' in sys.argv
    list_items(show_deleted=show_deleted)
