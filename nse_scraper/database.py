import mysql.connector
import csv
import time
from config import get_db_connection  
from datetime import datetime
from config import DB_CONFIG

def initialize_database():
    """Ensures the database and required tables exist."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"Database '{DB_CONFIG['database']}' created or already exists.")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bulk_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE,
                symbol VARCHAR(50),
                security_name VARCHAR(100),
                client_name VARCHAR(100),
                buy_sell VARCHAR(10),
                quantity_traded BIGINT,
                trade_price DECIMAL(10,2),
                remarks TEXT
            )
        """)
        print("Table 'bulk_data' created or already exists.")

        conn.commit()
        cursor.close()
        conn.close()
    
    except Exception as e:
        print(f"Database initialization failed: {e}")

def convert_date_format(date_str):
    """Convert date from DD-MMM-YYYY (e.g., 11-FEB-2025) to YYYY-MM-DD (2025-02-11)."""
    try:
        return datetime.strptime(date_str, "%d-%b-%Y").strftime("%Y-%m-%d")
    except ValueError:
        print(f"Invalid date format: {date_str}")
        return None

def store_csv_in_db(csv_filename):
    """Insert CSV data into the MySQL database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        with open(csv_filename, "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  
            print("CSV Headers Detected:", headers)

            query = """
                INSERT INTO bulk_data(date, symbol, security_name, client_name, buy_sell, quantity_traded, trade_price, remarks) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            for row in csv_reader:
                if len(row) != 8:  
                    print(f"Skipping invalid row: {row}")
                    continue
                
                row[0] = convert_date_format(row[0])
                if row[0] is None:
                    print(f"Skipping row due to invalid date: {row}")
                    continue

                try:
                    cursor.execute(query, row)
                except mysql.connector.Error as e:
                    print(f"Skipping row {row} due to error: {e}")

        conn.commit()
        cursor.close()
        conn.close()
        print("CSV data successfully inserted into MySQL database.")
    
    except Exception as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print("CSV file not found.")

if __name__ == "__main__":
    initialize_database()
