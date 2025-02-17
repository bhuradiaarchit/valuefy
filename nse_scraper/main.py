import os
import requests
import time
from database import initialize_database, store_csv_in_db


CSV_URL = "https://archives.nseindia.com/content/equities/bulk.csv"
CSV_FILE_PATH = "large_deals.csv"


def download_csv():
    try:
        print(" Downloading NSE Large Deals CSV file...")
        response = requests.get(CSV_URL, timeout=15)

        if response.status_code == 200:
            with open(CSV_FILE_PATH, "wb") as file:
                file.write(response.content)
            print(f" CSV downloaded successfully: {CSV_FILE_PATH}")
            return True
        else:
            print(f" Failed to download CSV. Status Code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f" Error downloading CSV: {e}")
        return False

# **Main Execution**
if __name__ == "__main__":
    print(" Initializing Database...")
    initialize_database()

    if download_csv():
        print(" Storing CSV data into database...")
        store_csv_in_db(CSV_FILE_PATH)
    else:
        print(" Skipping database insertion due to CSV download failure.")
