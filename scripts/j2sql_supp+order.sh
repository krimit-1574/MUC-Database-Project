#!/bin/bash
# j2sql_supp+order.sh
# Creates supplier/order tables and loads data from JSON files.
# Requires: parts table must already exist (run j2sql_parts.sh first).
# ─────────────────────────────────────────────────
USER="u60"
PASS="PASSWD"
DB="u60" 
# ─────────────────────────────────────────────────

# Ensure the script runs from its own directory
cd "$(dirname "$0")" || exit

# Step 1: Create supplier and order tables
mysql -u "$USER" -p"$PASS" "$DB" < ./make_tables.sql

# Step 2: Generate SQL files from JSON using Python scripts
python3 ./parse_suppliers.py
python3 ./parse_orders.py

# Check if SQL files were generated
if [ ! -f ./suppliers.sql ]; then
    echo "Error: suppliers.sql not generated. Check parse_suppliers.py."
    exit 1
fi

if [ ! -f ./orders.sql ]; then
    echo "Error: orders.sql not generated. Check parse_orders.py."
    exit 1
fi

# Step 3: Import data into MySQL (suppliers first due to FK constraints, then orders)
mysql -u "$USER" -p"$PASS" "$DB" < ./suppliers.sql
mysql -u "$USER" -p"$PASS" "$DB" < ./orders.sql

# Clean up temporary SQL files
rm -f ./suppliers.sql ./orders.sql

echo "Suppliers and Orders data import complete!"
