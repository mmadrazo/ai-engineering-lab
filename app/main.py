import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv(override=True)

#Create client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

#Request
response = client.responses.create(
    model="gpt-4o-mini",
    input="What is the capital of France?"
)

#Print response
print(response.output_text)