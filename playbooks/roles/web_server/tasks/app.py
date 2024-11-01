import os
from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Load MySQL configurations from environment variables
mysql_database_host = os.getenv('MYSQL_DATABASE_HOST')
mysql_database_user = os.getenv('MYSQL_DATABASE_USER')
mysql_database_password = os.getenv('MYSQL_DATABASE_PASSWORD')
mysql_database_db = os.getenv('MYSQL_DATABASE_DB')

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=mysql_database_host,
            user=mysql_database_user,
            password=mysql_database_password,
            database=mysql_database_db
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route("/")
def main():
    return "Welcome to the Employee Database API!"

@app.route('/how_are_you')
def hello():
    return 'I am good, how about you?'

@app.route('/read_from_database')
def read():
    conn = get_db_connection()
    if conn is None:
        return 'Failed to connect to the database', 500

    try:
        cursor = conn.cursor()
        query = "SELECT name FROM employees"
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            result = "No employees found"
        else:
            result = [row[0] for row in rows]

        cursor.close()
        conn.close()
        return jsonify(result)

    except Error as e:
        return f"Failed to query database: {e}", 500
