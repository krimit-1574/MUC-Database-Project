#!/usr/bin/env python3
"""
parse_parts.py
Reads parts_100.json (JSON Lines format) and generates parts.sql
with INSERT statements for the parts table.
"""
import json
import os
from pathlib import Path

current_user = os.getenv('USER')

# Configuration — paths on the Linux server dbcourse.cs-smu.ca
BASE_DIR = Path(f"/home/course/{current_user}/MUC-Database-System")
JSON_PATH = BASE_DIR / "data" / "parts_100.json"
SQL_OUTPUT = BASE_DIR / "scripts" / "parts.sql"


def generate_sql():
    try:
        if not JSON_PATH.exists():
            raise FileNotFoundError(f"JSON file not found at {JSON_PATH}")

        SQL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

        # Read JSON Lines (one JSON object per line)
        parts = []
        with open(JSON_PATH, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts.append(json.loads(line))

        # Generate SQL INSERT statements
        with open(SQL_OUTPUT, 'w') as f:
            for part in parts:
                desc = part['description'].replace("'", "''")
                f.write(
                    f"INSERT INTO parts (_id, price, description) "
                    f"VALUES ({part['_id']}, {part['price']}, '{desc}');\n"
                )

        print(f"Successfully generated {SQL_OUTPUT} ({len(parts)} rows).")

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    generate_sql()
