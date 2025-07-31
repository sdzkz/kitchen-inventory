#!/usr/bin/env python3

import sqlite3
import sys

DB_PATH = 'project.db'


def search_and_display(term: str) -> list[tuple]:
    """
    Replicate search.py logic: return list of matching rows
    and print them in the same tabular format.
    """
    search_pattern = f'%{term}%'

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT id, name, size, expiration_date, percent_remaining, count
        FROM item
        WHERE name LIKE ? COLLATE NOCASE
        ORDER BY id
    """
    cursor.execute(query, (search_pattern,))
    results = cursor.fetchall()

    headers = ['ID', 'Name', 'Size', 'Expiration Date', 'Percent Remaining', 'Count']

    if results:
        display_rows = []
        for row in results:
            display_rows.append([
                str(row[0]),
                row[1] or '',
                row[2] or '',
                row[3] or '',
                f"{row[4]:.1f}%" if row[4] is not None else 'N/A',
                str(row[5])
            ])

        col_widths = [
            max(len(headers[i]), max((len(r[i]) for r in display_rows), default=0))
            for i in range(len(headers))
        ]

        header_str = "  ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers)))
        print(header_str)
        print("-" * len(header_str))

        for row in display_rows:
            print("  ".join(row[i].ljust(col_widths[i]) for i in range(len(row))))

    conn.close()
    return results


def increment_count(item_id: int) -> None:
    """Add 1 to the count of the item with the given id."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE item SET count = count + 1 WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


def main() -> None:
    print()
    # 1. If arguments were supplied, treat them as a search term
    if len(sys.argv) > 1:
        search_term = ' '.join(sys.argv[1:])
        results = search_and_display(search_term)

        # 2. Prompt for an ID
        try:
            user_input = input(": ").strip()
            if user_input:
                item_id = int(user_input)
                # Validate that the id exists in the returned results
                if any(r[0] == item_id for r in results):
                    increment_count(item_id)
                    print("")
                    sys.exit(0)
                else:
                    print("ID not found in search results; continuing to new-item flow.")
        except ValueError:
            # Non-numeric input → fall through to normal flow
            pass

    # 3. Normal new-item flow (existing logic)
    if '--quick' in sys.argv:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        count = 1
        while True:
            name = input(f"item {count}: ").strip()
            if name == 'exit':
                break
            if not name:
                continue
            cursor.execute('INSERT INTO item (name, count) VALUES (?, 1)', (name,))
            conn.commit()
            count += 1
        conn.close()
    else:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        name = input("(name) ").strip()
        if not name:
            print()
            sys.exit(0)
        size = input("(size) ").strip() or None
        expiration = input("(expiration date) ").strip() or None
        count_str = input("(count) ").strip()
        try:
            count = int(count_str) if count_str else 1
        except ValueError:
            count = 1
        cursor.execute('''
        INSERT INTO item (name, size, expiration_date, count)
        VALUES (?, ?, ?, ?)
        ''', (name, size, expiration, count))
        conn.commit()
        print()
        conn.close()


if __name__ == "__main__":
    main()

