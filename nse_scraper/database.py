import mysql.connector
import csv
from config import DB_CONFIG  
from datetime import datetime

def initialize_database():
    """Initialize MySQL database and create the required table."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = conn.cursor()
        
        # Create database if it does not exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"✅ Database '{DB_CONFIG['database']}' created or already exists.")
        
        # Connect to the specific database
        conn.database = DB_CONFIG["database"]

        # Create table
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
        print("✅ Table 'large' created or already exists.")

        conn.commit()
        cursor.close()
        conn.close()
    
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")

def convert_date_format(date_str):
    """Convert date from DD-MMM-YYYY (e.g., 11-FEB-2025) to YYYY-MM-DD (2025-02-11)."""
    try:
        return datetime.strptime(date_str, "%d-%b-%Y").strftime("%Y-%m-%d")
    except ValueError:
        print(f"⚠️ Invalid date format: {date_str}")
        return None

def store_csv_in_db(csv_filename):
    """Insert CSV data into the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        with open(csv_filename, "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Read the header row
            print("🔍 CSV Headers Detected:", headers)

            query = """
                INSERT INTO bulk_data(date, symbol, security_name, client_name, buy_sell, quantity_traded, trade_price, remarks) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            for row in csv_reader:
                if len(row) != 8:  # Ensure correct number of columns
                    print(f"⚠️ Skipping invalid row: {row}")
                    continue
                
                # Convert date format
                row[0] = convert_date_format(row[0])
                if row[0] is None:
                    print(f"⚠️ Skipping row due to invalid date: {row}")
                    continue

                try:
                    cursor.execute(query, row)
                except mysql.connector.Error as e:
                    print(f"❌ Skipping row {row} due to error: {e}")

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ CSV data successfully inserted into MySQL database.")
    
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
    except FileNotFoundError:
        print("❌ CSV file not found.")

if __name__ == "__main__":
    initialize_database()
