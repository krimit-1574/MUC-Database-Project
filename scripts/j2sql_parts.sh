#!/bin/bash
# j2sql_parts.sh
# Creates the parts table and loads data from parts_100.json
# ─────────────────────────────────────────────────
USER="u60"
PASS="PASSWD"
DB="u60"
# ─────────────────────────────────────────────────

# Stop script if any command fails
set -e

# Ensure the script runs from its own directory
cd "$(dirname "$0")" || exit

# Step 0: Clean ALL tables (handle dependencies)
mysql -u "$USER" -p"$PASS" "$DB" -e "
DROP TABLE IF EXISTS OrderPart;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS SupplierPhone;
DROP TABLE IF EXISTS supplier;
DROP TABLE IF EXISTS parts;
"

# Step 1: Create the parts table
mysql -u "$USER" -p"$PASS" "$DB" < ./parts_table.sql

# Step 2: Generate SQL INSERT statements from JSON
python3 ./parse_parts.py

# Check if SQL file was generated
if [ ! -f ./parts.sql ]; then
    echo "Error: parts.sql not generated. Check parse_parts.py."
    exit 1
fi

# Step 3: Import parts data into MySQL
mysql -u "$USER" -p"$PASS" "$DB" < ./parts.sql

# Clean up temporary SQL file
rm -f ./parts.sql

echo "Parts data import complete!"
