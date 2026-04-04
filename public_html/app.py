import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

# ── Flask Application ──────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-secret-key")

# ── MySQL Configuration ────────────────────────────────────────
DB_CONFIG = {
    'user': 'uxx',
    'password': '[PASSWORD]',
    'host': 'localhost',
    'database': 'uxx',
    'connection_timeout': 5
}

# Whitelist of allowed table names (prevents SQL injection)
ALLOWED_TABLES = ['parts', 'supplier', 'SupplierPhone', 'Orders', 'OrderPart']


# ── Helper Functions ───────────────────────────────────────────
def get_db_connection():
    """Create and return a MySQL database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None


@app.context_processor
def inject_now():
    """Make current datetime available in all templates."""
    return {'now': datetime.now()}


# ── Error Handler ──────────────────────────────────────────────
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# ── Routes ─────────────────────────────────────────────────────

@app.route('/')
def index():
    """Home page with navigation to all operations."""
    return render_template('index.html')


# ─── OPERATION 1: Show Table ──────────────────────────────────
@app.route('/show_table', methods=['GET', 'POST'])
def show_table():
    """User enters a table name and the app displays its contents."""
    if request.method == 'POST':
        table_name = request.form.get('table_name', '').strip()

        if table_name not in ALLOWED_TABLES:
            flash(f"Table '{table_name}' is not allowed or does not exist. "
                  f"Allowed tables: {', '.join(ALLOWED_TABLES)}", "error")
            return redirect(url_for('show_table'))

        conn = get_db_connection()
        if not conn:
            flash("Failed to connect to the database.", "error")
            return redirect(url_for('show_table'))

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM {table_name}")
            table_data = cursor.fetchall()

            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [col['Field'] for col in cursor.fetchall()]

            cursor.close()
            conn.close()

            return render_template('show_table.html',
                                   table_name=table_name,
                                   columns=columns,
                                   table_data=table_data,
                                   allowed_tables=ALLOWED_TABLES)
        except mysql.connector.Error as e:
            flash(f"Error fetching table data: {e}", "error")
            conn.close()

    return render_template('show_table.html', allowed_tables=ALLOWED_TABLES)


# ─── OPERATION 2: Add New Supplier ────────────────────────────
@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    """User enters supplier attributes and the app inserts them."""
    if request.method == 'POST':
        supplier_id = request.form.get('supplier_id', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone_numbers = request.form.getlist('phone_number')

        # Validate required fields
        if not supplier_id or not name or not email:
            flash("Supplier ID, Name, and Email are required.", "error")
            return redirect(url_for('add_supplier'))

        # Validate supplier ID is numeric
        try:
            supplier_id = int(supplier_id)
        except ValueError:
            flash("Supplier ID must be a number.", "error")
            return redirect(url_for('add_supplier'))

        # Filter out empty phone numbers
        phone_numbers = [p.strip() for p in phone_numbers if p.strip()]
        if not phone_numbers:
            flash("At least one phone number is required.", "error")
            return redirect(url_for('add_supplier'))

        conn = get_db_connection()
        if not conn:
            flash("Failed to connect to the database.", "error")
            return redirect(url_for('add_supplier'))

        try:
            cursor = conn.cursor()
            conn.start_transaction()

            # Insert supplier
            cursor.execute(
                "INSERT INTO supplier (_id, name, email) VALUES (%s, %s, %s)",
                (supplier_id, name, email)
            )

            # Insert phone numbers
            for phone in phone_numbers:
                cursor.execute(
                    "INSERT INTO SupplierPhone (phone_number, supp_id) VALUES (%s, %s)",
                    (phone, supplier_id)
                )

            conn.commit()
            flash(f"Supplier '{name}' (ID: {supplier_id}) added successfully!", "success")
            return redirect(url_for('supplier_details', supplier_id=supplier_id))

        except mysql.connector.IntegrityError as e:
            conn.rollback()
            if 'Duplicate entry' in str(e):
                flash(f"Cannot insert: A supplier with ID {supplier_id} already exists, "
                      f"or a phone number is already in use.", "error")
            else:
                flash(f"Integrity error: {e}", "error")
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f"Error adding supplier: {e}", "error")
        finally:
            cursor.close()
            conn.close()

    return render_template('add_supplier.html')


@app.route('/supplier/<supplier_id>')
def supplier_details(supplier_id):
    """Display details of a specific supplier."""
    conn = get_db_connection()
    if not conn:
        flash("Failed to connect to the database.", "error")
        return redirect(url_for('add_supplier'))

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM supplier WHERE _id = %s", (supplier_id,))
        supplier = cursor.fetchone()

        if not supplier:
            flash("Supplier not found.", "error")
            return redirect(url_for('add_supplier'))

        cursor.execute("SELECT * FROM SupplierPhone WHERE supp_id = %s", (supplier_id,))
        phone_numbers = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('supplier_details.html',
                               supplier=supplier,
                               phone_numbers=phone_numbers)
    except mysql.connector.Error as e:
        conn.close()
        flash(f"Error retrieving supplier: {e}", "error")
        return redirect(url_for('add_supplier'))


# ─── OPERATION 3: Annual Expenses for Parts ───────────────────
@app.route('/annual_expenses', methods=['GET', 'POST'])
def annual_expenses():
    """User enters start/end year, app shows total money paid for parts each year."""
    if request.method == 'POST':
        start_year = request.form.get('start_year', '').strip()
        end_year = request.form.get('end_year', '').strip()

        try:
            start_year = int(start_year)
            end_year = int(end_year)
            if start_year > end_year:
                flash("Start year must be ≤ end year.", "error")
                return redirect(url_for('annual_expenses'))
        except ValueError:
            flash("Years must be valid integers.", "error")
            return redirect(url_for('annual_expenses'))

        conn = get_db_connection()
        if not conn:
            flash("Failed to connect to the database.", "error")
            return redirect(url_for('annual_expenses'))

        try:
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT
                    YEAR(o.when_date) AS year,
                    SUM(op.qty * p.price) AS total_expense
                FROM Orders o
                JOIN OrderPart op ON o.order_id = op.order_id
                JOIN parts p ON op.part_id = p._id
                WHERE YEAR(o.when_date) BETWEEN %s AND %s
                GROUP BY YEAR(o.when_date)
                ORDER BY year
            """

            cursor.execute(query, (start_year, end_year))
            expenses_data = cursor.fetchall()

            total = sum(row['total_expense'] for row in expenses_data) if expenses_data else 0

            cursor.close()
            conn.close()

            return render_template('annual_expenses.html',
                                   expenses_data=expenses_data,
                                   start_year=start_year,
                                   end_year=end_year,
                                   total_expense=total)

        except mysql.connector.Error as e:
            flash(f"Error fetching expenses: {e}", "error")
            conn.close()

    return render_template('annual_expenses.html')


# ─── OPERATION 4: Budget Projection ──────────────────────────
@app.route('/budget_projection', methods=['GET', 'POST'])
def budget_projection():
    """User enters N years and inflation rate, app shows projected spending."""
    if request.method == 'POST':
        years_str = request.form.get('years', '').strip()
        rate_str = request.form.get('inflation_rate', '').strip()

        try:
            years = int(years_str)
            inflation_rate = float(rate_str)
            if years <= 0:
                flash("Number of years must be positive.", "error")
                return redirect(url_for('budget_projection'))
            if inflation_rate < 0:
                flash("Inflation rate must be non-negative.", "error")
                return redirect(url_for('budget_projection'))
        except ValueError:
            flash("Please enter valid numbers.", "error")
            return redirect(url_for('budget_projection'))

        conn = get_db_connection()
        if not conn:
            flash("Failed to connect to the database.", "error")
            return redirect(url_for('budget_projection'))

        try:
            cursor = conn.cursor(dictionary=True)

            # The most recent full year is 2022 per the project instructions
            base_year = 2022

            # Get total expenses for 2022
            query = """
                SELECT SUM(op.qty * p.price) AS total_expense
                FROM Orders o
                JOIN OrderPart op ON o.order_id = op.order_id
                JOIN parts p ON op.part_id = p._id
                WHERE YEAR(o.when_date) = %s
            """
            cursor.execute(query, (base_year,))
            result = cursor.fetchone()
            base_expense = Decimal(str(result['total_expense'])) if result and result['total_expense'] else Decimal('0')

            # Calculate projections with inflation
            rate = Decimal(str(inflation_rate))
            projections = []
            for i in range(1, years + 1):
                projection_year = base_year + i
                projected = base_expense * ((Decimal('1') + rate / Decimal('100')) ** i)
                projections.append({
                    'year': projection_year,
                    'expense': round(float(projected), 2)
                })

            cursor.close()
            conn.close()

            return render_template('budget_projection.html',
                                   base_year=base_year,
                                   base_expense=float(base_expense),
                                   projections=projections,
                                   years=years,
                                   inflation_rate=inflation_rate)

        except mysql.connector.Error as e:
            flash(f"Error calculating projection: {e}", "error")
            conn.close()

    return render_template('budget_projection.html')


# ── Run Application ────────────────────────────────────────────
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)
