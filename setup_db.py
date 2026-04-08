import os
import subprocess
import mysql.connector
from dotenv import load_dotenv

# Load configuration from .env file (if exists, fallback to default)
load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = os.getenv('DB_NAME', 'muc_cars_db')

def create_database():
    """Create the database if it does not exist."""
    print(f"Connecting to MySQL server at {DB_HOST}...")
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        print(f"Database '{DB_NAME}' is ready.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL or creating database: {err}")
        print("Please ensure MySQL is running and credentials in your .env file are correct.")
        exit(1)

def run_sql_file(conn, filename):
    """Execute a .sql file."""
    print(f"Executing {filename}...")
    if not os.path.exists(filename):
         print(f"Error: {filename} not found.")
         return False

    with open(filename, 'r') as f:
        sql = f.read()

    cursor = conn.cursor()
    try:
        # multi=True allows execution of multiple statements separated by ';'
        for result in cursor.execute(sql, multi=True):
            pass
        conn.commit()
        print(f"Success executing {filename}")
        return True
    except mysql.connector.Error as err:
        print(f"Error executing {filename}: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def generate_sql_from_json():
    """Run the python scripts to generate SQL INSERTfiles from JSON data."""
    scripts = [
        'scripts/parse_parts.py',
        'scripts/parse_suppliers.py',
        'scripts/parse_orders.py'
    ]
    for script in scripts:
        print(f"Running {script}...")
        try:
            result = subprocess.run(['python', script], check=True, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"Error generating SQL with {script}:")
            print(e.stderr)
            exit(1)

def main():
    print("=== MUC Database Setup Script ===")
    
    # 1. Create DB
    create_database()

    # Connect to the specific database
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

    # 2. Re-create tables (Note: these scripts drop existing tables)
    if not run_sql_file(conn, 'scripts/parts_table.sql'):
         exit(1)
    if not run_sql_file(conn, 'scripts/make_tables.sql'):
         exit(1)

    # 3. Generate SQL insert statements from JSON files
    generate_sql_from_json()

    # 4. Insert data using generated SQL scripts
    if not run_sql_file(conn, 'scripts/parts.sql'):
         exit(1)
    if not run_sql_file(conn, 'scripts/suppliers.sql'):
         exit(1)
    if not run_sql_file(conn, 'scripts/orders.sql'):
         exit(1)

    # Clean up generated .sql files to avoid keeping redundant copies
    for temp_sql in ['scripts/parts.sql', 'scripts/suppliers.sql', 'scripts/orders.sql']:
        if os.path.exists(temp_sql):
            os.remove(temp_sql)

    conn.close()
    print("Database setup completed successfully!")

if __name__ == '__main__':
    main()
