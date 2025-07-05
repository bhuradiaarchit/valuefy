import os
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from collections import OrderedDict
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

class YahooFinanceAPI:
    def __init__(self):

        db_config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'), 
            'dbname': os.getenv('DB_NAME')
        }
        encoded_password = quote_plus(db_config['password'])
        db_url = f"postgresql://{db_config['user']}:{encoded_password}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
        self.engine = create_engine(db_url)

    def call_symbols_from_postgres(self):
        query = """
        SELECT symbol FROM bulk_data 
        WHERE date = (SELECT MAX(date) FROM bulk_data)
        """

        try:
            with self.engine.connect() as conn:
                print(conn)
                df_bulk_data = pd.read_sql_query(query, conn)
        except Exception as e:
            print(f"Error fetching data from PostgreSQL: {e}")
            return []

        return list(df_bulk_data["symbol"].unique())

    def compare_with_latest_prices(self):
        symbols = self.call_symbols_from_postgres()
        symbols = [symbol + ".NS" for symbol in symbols]
        
        print(symbols)
        
        end_date = pd.Timestamp.today().date()
        start_date = end_date - pd.Timedelta(days=7)

        df = yf.download(symbols, start=start_date, end=end_date)

        #print(df)
        df.to_csv('data.csv')

        pct_change_data = df['Close'].pct_change().iloc[len(df) - 1] * 100
        pct_change_sorted = pct_change_data.sort_values(ascending=False).dropna()

        pct_change_data = pct_change_data.head(10)
        
        result = []
        for symbol, value in pct_change_data.items():
            if value is not None:
                result.append((symbol, value))

        result.sort(key=lambda x: x[1])
        result.reverse()
        return result
    

class HighVolumers:
    def __init__(self):
        db_config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'), 
            'dbname': os.getenv('DB_NAME')
        }
        encoded_password = quote_plus(db_config['password'])
        db_url = f"postgresql://{db_config['user']}:{encoded_password}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
        self.engine = create_engine(db_url)

    def top_10_volume_gainers(self):
        query = """
        SELECT symbol, 
               SUM(quantity_traded * trade_price) AS total_volume
        FROM bulk_data
        GROUP BY symbol
        ORDER BY total_volume DESC
        LIMIT 10;
        """

        try:
            with self.engine.connect() as conn:
                volume_table = pd.read_sql_query(query, conn)
        except Exception as e:
            print(f"Error fetching volume data from PostgreSQL: {e}")
            return pd.DataFrame()
        
        return volume_table.to_dict()

    def execution_flow(self):
        return self.top_10_volume_gainers()
