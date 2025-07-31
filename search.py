#!/usr/bin/env python3

import sqlite3
import sys

DB_PATH = 'project.db'

def main():
    if len(sys.argv) < 2:
        print("Error: Search term required", file=sys.stderr)
        print(f"Usage: {sys.argv[0]} <search_term>", file=sys.stderr)
        sys.exit(1)
    
    # Combine all arguments into single search string
    search_term = ' '.join(sys.argv[1:])
    search_pattern = f'%{search_term}%'

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Case-insensitive substring search in name column
        query = """
            SELECT id, name, size, expiration_date, percent_remaining, count
            FROM item
            WHERE name LIKE ? COLLATE NOCASE
            ORDER BY id
        """
        cursor.execute(query, (search_pattern,))
        results = cursor.fetchall()
        
        # Define column headers matching list.py format
        headers = ['ID', 'Name', 'Size', 'Expiration Date', 'Percent Remaining', 'Count']
        
        # Process and format results
        if results:
            # Convert results to display format with proper null handling
            display_rows = []
            for row in results:
                display_rows.append([
                    str(row[0]),  # ID
                    row[1] or '',  # Name
                    row[2] or '',  # Size
                    row[3] or '',  # Expiration Date
                    f"{row[4]:.1f}%" if row[4] is not None else 'N/A',  # Percent Remaining
                    str(row[5])    # Count
                ])
            
            # Calculate column widths (including headers)
            col_widths = [
                max(len(str(headers[i])), max((len(r[i]) for r in display_rows), default=0))
                for i in range(len(headers))
            ]
            
            # Print header with proper alignment
            header_str = "  ".join(
                headers[i].ljust(col_widths[i]) 
                for i in range(len(headers))
            )
            print(header_str)
            print("-" * len(header_str))
            
            # Print each result row
            for row in display_rows:
                print("  ".join(
                    row[i].ljust(col_widths[i]) 
                    for i in range(len(row))
                ))
        else:
            print(f"No items found matching '{search_term}'")
            
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
