# MUC Database System

**CSCI 3461 — Group Project**
Database management system for MUC Used Cars.

---

## Prerequisites

- Python 3.x
- MySQL (available on `dbcourse.cs-smu.ca` or your Local Windows Setup)
- `pip` (Python package manager)

## Setup & Deployment

### 1. Clone / Upload to the Server

```bash
# Option A: Clone from Git
git clone <your-repo-url> MUC-Database-System
cd MUC-Database-System

# Option B: Upload via SCP (to a school server)
scp -r Project/ youruser@dbcourse.cs-smu.ca:~/MUC-Database-System/
ssh youruser@dbcourse.cs-smu.ca
cd ~/MUC-Database-System
```

### 2. Configure Credentials (Secure for GitHub)

To avoid leaking your database credentials when pushing code to a public GitHub repository, this project uses an environment variable file (`.env`). **This file is ignored by Git.**

1. Create a `.env` file by copying the provided example:
   ```bash
   cp .env.example .env
   ```
   *(On Windows Command Prompt, use: `copy .env.example .env`)*

2. Open the `.env` file and update it with your actual MySQL credentials and database name:
   ```ini
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASS=your_password
   DB_NAME=your_database_name
   FLASK_SECRET_KEY=put_some_random_secret_here
   ```

### 3. Install Dependencies
Install all required Python packages before proceeding. Make sure you run this from the project root!
```bash
# The requirements.txt is located under public_html/
pip install -r public_html/requirements.txt
```

### 4. Create Tables & Load Data (Cross-Platform)

We have provided a unified Python script (`setup_db.py`) that handles connecting to your database, creating all tables, processing the local JSON files, and generating the necessary SQL inserts. This script works perfectly on both Windows and Linux!

```bash
# Run the setup script from the root of the project
python setup_db.py
```
*(If you are on Linux or macOS, you might need to use `python3 setup_db.py`)*

### 5. Run the Web Application

```bash
cd public_html
python app.py
```

The app will be available at **http://localhost:5010**

> **Note on Legacy Scripts**: The old bash scripts (`scripts/j2sql_parts.sh` and `scripts/j2sql_supp+order.sh`) are still present but `setup_db.py` is the recommended, secure, and cross-platform way to build the database.

## Project Structure

```
MUC-Database-System/
├── README.md
├── report.md                       # Project report
├── .gitignore                      # Git ignore file (safeguards .env)
├── .env.example                    # Sample required env variables
├── setup_db.py                     # Universal Database Initialization Script
├── data/                           # JSON data files
│   ├── parts_100.json
│   ├── suppliers_100.json
│   └── orders_4000.json
├── scripts/                        # Database scripts & queries
│   ├── parts_table.sql             # CREATE TABLE parts
│   ├── make_tables.sql             # Creates other relations
│   ├── parse_parts.py              # JSON → SQL for parts
│   ├── parse_suppliers.py          # JSON → SQL for suppliers
│   └── parse_orders.py             # JSON → SQL for orders
└── public_html/                    # Flask web application
    ├── app.py                      # Main app (all 4 operations)
    ├── requirements.txt
    ├── static/style.css
    └── templates/                  # HTML templates
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
