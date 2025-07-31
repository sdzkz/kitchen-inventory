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

    # Prepare data with formatted count column
    data = []
    for item in items:
        id_, name, size, exp_date, count = item

        # Format the count column
        if count == 0:
            count_str = "-"
        elif count == 1:
            count_str = ""
        else:
            count_str = f"{count}x"

        data.append((
            str(id_),
            count_str,
            name or 'N/A',
            size or 'N/A',
            exp_date or 'N/A',
        ))

    # Find max widths for each column
    col_widths = [2, 2, 4, 4, 15]  # Min widths for ID, Count, Name, Size, Exp Date
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
    print(fmt.format("ID", "", "Name", "Size", "Expiration Date"))
    print("-" * (sum(col_widths) + 8))  # 8 = 4 spaces between columns

    # Print rows
    for row in data:
        print(fmt.format(*row))

if __name__ == "__main__":
    print()
    show_deleted = '--show-deleted' in sys.argv
    list_items(show_deleted=show_deleted)
    print()

