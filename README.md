# MUC Database System

**CSCI 3461 — Group Project**
Database management system for MUC Used Cars.

---

## Prerequisites

- Python 3.x
- MySQL (available on `dbcourse.cs-smu.ca`)
- `pip` (Python package manager)

## Setup & Deployment

### 1. Clone / Upload to the Server

```bash
# Option A: Clone from Git
git clone <your-repo-url> ~/MUC-Database-System
cd ~/MUC-Database-System

# Option B: Upload via SCP
scp -r Project/ youruser@dbcourse.cs-smu.ca:~/MUC-Database-System/
ssh youruser@dbcourse.cs-smu.ca
cd ~/MUC-Database-System
```

### 2. Update Credentials

Edit the following files and replace `uXX` / `password` with your actual MySQL credentials:

```bash
# Bash scripts (lines 6-8)
nano scripts/j2sql_parts.sh
nano scripts/j2sql_supp+order.sh

# Flask app (lines 17-20)
nano public_html/app.py
```

### 3. Create Tables & Load Data

```bash
cd ~/MUC-Database-System/scripts

# Step 1: Create and populate the parts table
bash j2sql_parts.sh

# Step 2: Create and populate supplier + order tables
bash j2sql_supp+order.sh
```

> **Note:** Run `j2sql_parts.sh` first — the order tables have foreign keys referencing `parts`.

### 4. Run the Web Application

```bash
cd ~/MUC-Database-System/public_html
pip install -r requirements.txt
python3 app.py
```

The app will be available at **http://localhost:5010**

## Project Structure

```
MUC-Database-System/
├── README.md
├── report.md                       # Project report
├── .gitignore                      # Git ignore file
├── scripts_8.zip                   # Archived scripts backup
├── data/                           # JSON data files
│   ├── parts_100.json
│   ├── suppliers_100.json
│   └── orders_4000.json
├── scripts/                        # Database scripts
│   ├── parts_table.sql             # CREATE TABLE parts
│   ├── make_tables.sql             # CREATE TABLE supplier, SupplierPhone, Orders, OrderPart
│   ├── j2sql_parts.sh              # Load parts data
│   ├── j2sql_supp+order.sh         # Load supplier & order data
│   ├── parse_parts.py              # JSON → SQL for parts
│   ├── parse_suppliers.py          # JSON → SQL for suppliers
│   └── parse_orders.py             # JSON → SQL for orders
└── public_html/                    # Flask web application
    ├── app.py                      # Main app (all 4 operations)
    ├── requirements.txt
    ├── .env
    ├── venv/                       # Python virtual environment
    ├── static/style.css
    └── templates/                  # HTML templates (8 files)
```

## Web Application Operations

| # | Operation | Description |
|---|-----------|-------------|
| 1 | **Show Table** | Select a table name → view all its contents |
| 2 | **Add Supplier** | Enter supplier info + phone numbers → insert into DB |
| 3 | **Annual Expenses** | Enter year range → total money spent on parts per year |
| 4 | **Budget Projection** | Enter N years + inflation rate → projected spending from 2022 |

## Database Tables

| Table | Description |
|-------|-------------|
| `parts` | Part ID, price, description |
| `supplier` | Supplier ID, name, email |
| `SupplierPhone` | Phone numbers linked to suppliers |
| `Orders` | Order ID, date, supplier ID |
| `OrderPart` | Order-part relationship with quantity |
