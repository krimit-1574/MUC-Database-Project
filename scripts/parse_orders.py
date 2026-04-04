#!/usr/bin/env python3
"""
parse_orders.py
Reads orders_4000.json (JSON Lines format) and generates orders.sql
with INSERT statements for the Orders and OrderPart tables.

Note: Some orders contain duplicate part_ids (e.g., the same part listed
      twice with different quantities). Each item is inserted as a
      separate row in OrderPart.
"""

from pathlib import Path

# Configuration — paths on the Linux server dbcourse.cs-smu.ca
SCRIPT_DIR = Path(_file_).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
JSON_PATH = BASE_DIR / "data" / "orders_4000.json"
SQL_OUTPUT = SCRIPT_DIR / "orders.sql"


def generate_sql():
    try:
        if not JSON_PATH.exists():
            raise FileNotFoundError(f"JSON file not found at {JSON_PATH}")

        SQL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

        # Read JSON Lines (one JSON object per line)
        with open(JSON_PATH, 'r') as f:
            orders = [json.loads(line) for line in f if line.strip()]

        # Validate structure
        for order in orders:
            if not all(k in order for k in ('when', 'supp_id', 'items')):
                raise ValueError(f"Missing required fields in order: {order}")
            for item in order['items']:
                if not all(k in item for k in ('part_id', 'qty')):
                    raise ValueError(f"Missing required fields in item: {item}")

        # Generate SQL INSERT statements
        with open(SQL_OUTPUT, 'w') as f:
            for order_id, order in enumerate(orders, start=1):
                # Insert the order
                f.write(
                    f"INSERT INTO Orders (order_id, when_date, supp_id) "
                    f"VALUES ({order_id}, '{order['when']}', {order['supp_id']});\n"
                )
                # Insert each order item (including duplicates — OrderPart has auto-increment PK)
                for item in order['items']:
                    f.write(
                        f"INSERT INTO OrderPart (order_id, part_id, qty) "
                        f"VALUES ({order_id}, {item['part_id']}, {item['qty']});\n"
                    )

        print(f"Successfully generated {SQL_OUTPUT} ({len(orders)} orders).")

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    generate_sql()
