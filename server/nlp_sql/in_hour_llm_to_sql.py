import vanna as vn
from dotenv import load_dotenv
import os
from vanna.remote import VannaDefault

load_dotenv()


class LLMtoSQL:
    def __init__(self):
        self.vn = VannaDefault(model="valuefy-model", api_key=os.getenv("VANNA_API_KEY_2"))
        self.vn.connect_to_postgres(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        )

    def query_the_database(self, message):
        query = self.vn.generate_sql(message, allow_llm_to_see_data=True)
        df = self.vn.run_sql(query)
        plotly_code = self.vn.generate_plotly_code(df)
        fig = self.vn.get_plotly_figure(plotly_code, df)
        return query, df, fig

    def call_llm_to_sql(self, message):
        return self.query_the_database(message)
