import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
try:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    print("Testing embedding call...")
    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents="Hello world"
    )
    print(f"Response Type: {type(response)}")
    print(f"Response Dir: {dir(response)}")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")
