import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AI:
    client = None

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_TOKEN")
        )

    def query(self, query):
        return self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ],
            model="gpt-3.5-turbo"
        ).choices[0].message.content
