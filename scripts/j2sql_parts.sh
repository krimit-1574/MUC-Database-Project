#!/bin/bash
# j2sql_parts.sh
# Creates the parts table and loads data from parts_100.json
# ─────────────────────────────────────────────────
USER="uxx"
PASS="[PASSWORD]"
DB="uxx"
# ─────────────────────────────────────────────────

# Ensure the script runs from its own directory
cd "$(dirname "$0")" || exit

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
