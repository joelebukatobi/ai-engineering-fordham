import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
try:
    print("Checking available models via google-genai SDK...")
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # List models
    # The iterator returns Model objects
    for m in client.models.list(config={'page_size': 100}):
        # Check if it supports embedding
        if 'embedContent' in (m.supported_generation_methods or []):
            print(f"FOUND EMBEDDING MODEL: {m.name}")
            
except Exception as e:
    print(f"Error listing models: {e}")
