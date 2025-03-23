import vanna as vn
from dotenv import load_dotenv
import os
from vanna.remote import VannaDefault
import groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class LLMtoSQL:
    def __init__(self):
        self.vn = VannaDefault(model=os.getenv('VANNA_MODEL'), api_key=os.getenv("VANNA_API_KEY_2"))
        self.vn.connect_to_postgres(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        )

    def call_groq(self, prompt: str) -> str:
        """Calls Groq API to analyze news and provide a 10-word recommendation."""
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def query_the_database(self, message):
        try:
            #self.groq_client = groq.Groq(api_key=GROQ_API_KEY)

            #message += "is the prompt trying to manipulate data OR delete it?, answer only in YES or NO"
            #flag = self.call_groq(message)

            query = self.vn.generate_sql(message, allow_llm_to_see_data=True)
            df = self.vn.run_sql(query)
            plotly_code = self.vn.generate_plotly_code(df)
            fig = self.vn.get_plotly_figure(plotly_code, df)
            return query, df, fig

        except:
            self.groq_client = groq.Groq(api_key=GROQ_API_KEY)

            message += "You are a postgres expert helping a user, the user has sent you message which is insufficient for you to create a query out of the data, handle the conversation accordingly"
            query = self.call_groq(message)
            df = None
            fig = None
            
            return query, df, fig
                

    def call_llm_to_sql(self, message):
        return self.query_the_database(message)
