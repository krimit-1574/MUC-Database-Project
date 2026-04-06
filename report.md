# Web Application Structure Report

## Overview
Our web application is built using Python, the Flask web framework, and a MySQL database. We designed the project so that the backend logic (our Python code) is kept separate from the frontend (our HTML and CSS). 

## Main Application Files

### 1. `public_html/app.py` (The Backend)
This is the main Python file that runs the server. It handles our connection to the MySQL database and manages what happens when a user visits a link or submits a form. Inside, it has different "routes" for each of the four main operations:
- **Database Connection:** We use `mysql.connector` to securely log into our database before running any queries.
- **Show Table:** It receives the table name, checks to make sure the user isn't just typing random stuff, and runs a `SELECT *` query to display the table.
- **Add New Supplier:** It takes the data from the form, tries to run the `INSERT` SQL queries into the supplier and phone tables, and catches errors if the supplier ID already exists. 
- **Annual Expenses:** It runs a report using `JOIN` statements and grouping to calculate the total spent on parts across different years.
- **Budget Projection:** It retrieves our base expenses from 2022 and calculates future costs using a little bit of math for the inflation rate.

### 2. `public_html/templates/` (The Frontend HTML)
This folder holds all the HTML files the user actually sees on their screen. We used Jinja (Flask's template system) so we didn't have to rewrite the same HTML over and over again.
- **`base.html`:** This is our main layout file. It has the navigation bar at the top and the basic structure of the website. 
- **The specific pages (`index.html`, `show_table.html`, etc.):** These files simply "extend" our base layout. When `app.py` gets data back from the database, it sends it to these files, and we use loops inside the HTML to create tables and lists on the screen.

### 3. `public_html/static/style.css` (The Styling)
We put all of our CSS inside this file. It makes our web application look presentable by styling our tables, form inputs, buttons, and navigation bar so that everything looks consistent.

### 4. Database Setup (`scripts/`)
We also have a folder for our database setup files. This includes our python scripts (`parse_orders.py`, `parse_suppliers.py`) and bash scripts (`j2sql_parts.sh`, `j2sql_supp+order.sh`). We used these to parse the provided JSON files and quickly generate all our `INSERT` SQL statements so the app would have test data to display.

## How it All Works Together
When a user clicks a button or fills out a form on the webpage, that request is sent to `app.py`. The `app.py` file looks at what the user wants, safely builds the SQL query, and asks MySQL for the data. Once the database sends the data back, `app.py` passes the results to one of the HTML templates in the `templates/` folder. The template formats the data nicely and sends the finished webpage back to the user's browser.
