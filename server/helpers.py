import os
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from collections import OrderedDict

# Load environment variables
load_dotenv()

class YahooFinanceAPI:
    def __init__(self):
        self.db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@" \
                      f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        self.engine = create_engine(self.db_url)

    def call_symbols_from_postgres(self):
        query = """
        SELECT symbol FROM bulk_data 
        WHERE date = (SELECT MAX(date) FROM bulk_data)
        """

        try:
            with self.engine.connect() as conn:
                df_bulk_data = pd.read_sql_query(query, conn)
        except Exception as e:
            print(f"Error fetching data from PostgreSQL: {e}")
            return []

        return list(df_bulk_data["symbol"].unique())

    def compare_with_latest_prices(self):
        symbols = self.call_symbols_from_postgres()
        symbols = [symbol + ".NS" for symbol in symbols]
        
        end_date = pd.Timestamp.today().date()
        start_date = end_date - pd.Timedelta(days=7)

        df = yf.download(symbols, start=start_date, end=end_date)
        #df.to_csv('data.csv')

        pct_change_data = df['Close'].pct_change().iloc[len(df) - 1] * 100
        pct_change_sorted = pct_change_data.sort_values(ascending=False)

        print(pct_change_sorted)
        
        return list(pct_change_sorted.items())
    

class HighVolumers:
    def __init__(self):
        self.db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@" \
                      f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        self.engine = create_engine(self.db_url)

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
