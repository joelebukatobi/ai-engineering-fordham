import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
try:
    print("Inspecting models via google-genai SDK...")
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # List first 10 models
    # It generally returns an iterable that yields objects
    count = 0
    for m in client.models.list(config={'page_size': 50}):
        name = m.name
        if "embed" in name.lower():
            print(f"FOUND: {name}")
            print(f"  {m}")
            count += 1
            if count >= 5: break
            
except Exception as e:
    print(f"Error: {e}")
