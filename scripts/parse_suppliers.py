#!/usr/bin/env python3
"""
parse_suppliers.py
Reads suppliers_100.json (single JSON array) and generates suppliers.sql
with INSERT statements for the supplier and SupplierPhone tables.
"""
import json
from pathlib import Path

# Configuration — paths on the Linux server dbcourse.cs-smu.ca
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
JSON_PATH = BASE_DIR / "data" / "suppliers_100.json"
SQL_OUTPUT = SCRIPT_DIR / "suppliers.sql"


def generate_sql():
    try:
        if not JSON_PATH.exists():
            raise FileNotFoundError(f"JSON file not found at {JSON_PATH}")

        SQL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

        # Read JSON array
        with open(JSON_PATH, 'r') as f:
            suppliers = json.load(f)

        # Generate SQL INSERT statements
        with open(SQL_OUTPUT, 'w') as f:
            for s in suppliers:
                name = s["name"].replace("'", "''")
                email = s["email"].replace("'", "''")
                f.write(
                    f"INSERT INTO supplier (_id, name, email) "
                    f"VALUES ({s['_id']}, '{name}', '{email}');\n"
                )
                for phone in s["tel"]:
                    number = phone["number"].replace("'", "''")
                    f.write(
                        f"INSERT INTO SupplierPhone (phone_number, supp_id) "
                        f"VALUES ('{number}', {s['_id']});\n"
                    )

        print(f"Successfully generated {SQL_OUTPUT} ({len(suppliers)} suppliers).")

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    generate_sql()
