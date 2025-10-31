#!/usr/bin/env python3
"""
inventory_to_natural_language.py
Dump the `item` table to a human-friendly shopping-list style report.

By default the report is written to Inventory.txt in the same directory.
Pass --print to emit the report to stdout instead.
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict

DB_PATH   = Path(__file__).with_name("project.db")
OUT_PATH  = Path(__file__).with_name("Inventory.txt")

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def fetch_inventory() -> List[Dict]:
    """Return the contents of the `item` table as a list of dicts."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM item ORDER BY name")
        return [dict(row) for row in cur.fetchall()]

def qty_desc(item: Dict) -> str:
    """Return a concise quantity / remaining description."""
    cnt = item["count"]
    pct = item["percent_remaining"]
    exp = item["expiration_date"]

    parts = []
    if cnt is not None and cnt != 0:
        parts.append(f"×{cnt}")
    if pct is not None and pct != 0:
        parts.append(f"{int(pct)} % left")
    if exp:
        parts.append(f"exp {exp}")
    return "  " + ", ".join(parts) if parts else ""

def build_report(inventory: List[Dict]) -> str:
    """Convert inventory rows into a natural-language list."""
    lines = [
        f"Kitchen inventory ({len(inventory)} items, last audit {datetime.now():%Y-%m-%d})",
        ""
    ]

    # Group into rough categories by keyword
    categories = {
        "Spices & herbs": [
            "allspice", "bay", "cayenne", "chili", "cinnamon", "cloves", "coriander",
            "cumin", "curry", "fennel", "garlic", "ginger", "italian", "mustard",
            "onion", "oregano", "paprika", "pepper", "salt", "smoked", "thyme",
            "turmeric", "tumeric"
        ],
        "Canned & jarred": ["beans", "corn", "tomato", "tuna", "anchov", "sauce", "paste"],
        "Grains & dry goods": ["rice", "quinoa", "oats", "lentils", "seasoning"],
        "Produce": ["apple", "avocado", "banana", "blueberr", "carrot", "celery",
                    "garlic", "grape", "lime", "lemon", "mango", "onion", "orange",
                    "papaya", "pineapple", "potato", "radish", "romaine", "strawberr",
                    "tomato", "lettuce", "pepper", "serrano"],
        "Dairy & eggs": ["butter", "cheese", "cottage", "egg", "milk", "yogurt"],
        "Freezer / prepared": ["freezer", "chicken", "salmon", "bacon", "lamb", "brat",
                               "turkey", "tilapia", "burger"],
        "Liquids & condiments": ["oil", "vinegar", "ketchup", "mustard", "a1", "juice",
                                 "broth", "water", "sauce"],
        "Sweeteners & baking": ["sugar", "cocoa", "vanilla", "applesauce"],
    }

    grouped = {cat: [] for cat in categories}
    misc = []

    for it in inventory:
        name = it["name"].lower()
        placed = False
        for cat, keys in categories.items():
            if any(k in name for k in keys):
                grouped[cat].append(it)
                placed = True
                break
        if not placed:
            misc.append(it)

    # Render each section
    for cat, items in grouped.items():
        if not items:
            continue
        lines.append(cat)
        for it in items:
            suffix = qty_desc(it)
            lines.append(f"  - {it['name']}{suffix}")
        lines.append("")

    if misc:
        lines.append("Miscellaneous")
        for it in misc:
            suffix = qty_desc(it)
            lines.append(f"  - {it['name']}{suffix}")
        lines.append("")

    # Quick summary of “count = 0” items
    zero = [it["name"] for it in inventory if it["count"] == 0]
    if zero:
        lines.append(f"Currently out of stock ({len(zero)} items)")
        lines.append(", ".join(zero))
        lines.append("")

    return "\n".join(lines)

# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Export inventory to a natural-language list.")
    parser.add_argument(
        "--print",
        action="store_true",
        help="Write report to stdout instead of Inventory.txt",
    )
    args = parser.parse_args()

    inventory = fetch_inventory()
    report = build_report(inventory)

    if args.print:
        print(report)
    else:
        OUT_PATH.write_text(report, encoding="utf-8")
        print(f"Wrote {len(inventory)} items to {OUT_PATH}", file=sys.stderr)

if __name__ == "__main__":
    main()

