

import logging
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

class DataToPostgres():

    def dataframe_to_postgres(self, db_config, df, table_name, operation):
        encoded_password = quote_plus(db_config['password'])

        try:
            db_url = f"postgresql://{db_config['user']}:{encoded_password}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"

            engine = create_engine(db_url)

            with engine.begin() as connection:  
                df.to_sql(table_name, connection, if_exists=operation, index=False)

            engine.dispose()

            rows = len(df)
            logger.info(f"Successfully {operation} {rows} rows to {table_name} table in postgres")
        
        except Exception as e:
            logger.error(f"There was an error while appending the dataframe: {e}")

        finally:
            connection.close()
            engine.dispose()

    
    def delete_file(self, path_of_file):
        if os.path.exists(path_of_file):
            os.remove(path_of_file)
            logger.info(f"Deleted: {path_of_file}")
        else:
            logger.error(f"File not found: {path_of_file}")

    
    def rename_columns(self, df):

        df.rename(columns = {
            'Date':'date',
            'Symbol': 'symbol',
            'Security Name': 'security_name',
            'Client Name': 'client_name',
            'Buy/Sell': 'buy_sell',
            'Quantity Traded': 'quantity_traded',
            'Trade Price / Wght. Avg. Price': 'trade_price',
            'Remarks': 'remarks'
        }, inplace = True)

        return df


    def execution_flow(self):

        df = pd.read_csv(os.getenv('CSV_FILE_PATH'))
        df = self.rename_columns(df)

        db_config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'), 
            'dbname': os.getenv('DB_NAME')
        }

        self.dataframe_to_postgres(db_config, df, 'bulk_data', 'append')
        self.delete_file(os.getenv('CSV_FILE_PATH'))