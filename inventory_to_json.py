#!/usr/bin/env python3
"""
inventory_to_json.py
Dump the `item` table to JSON.

By default the JSON is written to Inventory.json in the same directory.
Pass --print to emit the JSON to stdout instead.
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).with_name("project.db")
OUT_PATH = Path(__file__).with_name("Inventory.json")

def fetch_inventory() -> list[dict]:
    """Return the contents of the `item` table as a list of dicts."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM item")
        return [dict(row) for row in cur.fetchall()]

def main() -> None:
    parser = argparse.ArgumentParser(description="Export inventory to JSON.")
    parser.add_argument(
        "--print",
        action="store_true",
        help="Write JSON to stdout instead of Inventory.json",
    )
    args = parser.parse_args()

    inventory = fetch_inventory()
    json_blob = json.dumps(inventory, indent=2)

    print()

    if args.print:
        print(json_blob)
    else:
        OUT_PATH.write_text(json_blob, encoding="utf-8")
        print(f"Wrote {len(inventory)} items to {OUT_PATH}", file=sys.stderr)
    
    print()
if __name__ == "__main__":
    main()

