import os
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL configurations fetched from environment variables
mysql_database_host = os.getenv('MYSQL_DATABASE_HOST')
mysql_database_user = os.getenv('MYSQL_DATABASE_USER')
mysql_database_password = os.getenv('MYSQL_DATABASE_PASSWORD')
mysql_database_db = os.getenv('MYSQL_DATABASE_DB')

print(f"Configured MySQL with Host: {mysql_database_host}, User: {mysql_database_user}, Database: {mysql_database_db}")

# Establish MySQL connection
def get_db_connection():
    print(f"Attempting to connect to MySQL at {mysql_database_host} as {mysql_database_user}")
    try:
        conn = mysql.connector.connect(
            host=mysql_database_host,
            user=mysql_database_user,
            password=mysql_database_password,
            database=mysql_database_db
        )
        if conn.is_connected():
            print("Connection to MySQL successful")
        return conn
    except Error as e:
        print(f"Error: Could not connect to MySQL at {mysql_database_host}. Error: {e}")
        return None

@app.route("/")
def main():
    return "Welcome to the Employee Database API!"

@app.route('/how_are_you')
def hello():
    return 'I am good, how about you?'

@app.route('/read_from_database', methods=['GET'])
def read():
    print("Processing request: /read_from_database")
    conn = get_db_connection()

    if conn is None:
        print("Failed to establish a connection with the database")
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        cursor = conn.cursor()
        print("Executing query: SELECT name FROM employees")
        cursor.execute("SELECT name FROM employees")
        rows = cursor.fetchall()

        if not rows:
            print("Query result: No employees found")
            result = {"message": "No employees found"}
        else:
            print(f"Query result: {len(rows)} employees found")
            result = {"employees": [row[0] for row in rows]}

        cursor.close()
        conn.close()
        print("Connection closed after query")
        return jsonify(result)

    except Error as e:
        print(f"Database query failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    name = data.get('name')
    position = data.get('position')
    salary = data.get('salary')

    if not name or not position or not salary:
        print("Invalid input data")
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db_connection()

    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        cursor = conn.cursor(prepared=True)
        query = "INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, position, salary))
        conn.commit()

        cursor.close()
        conn.close()
        print("Employee added successfully")
        return jsonify({"message": "Employee added successfully"})

    except Error as e:
        print(f"Failed to add employee: {e}")
        return jsonify({"error": str(e)}), 500
