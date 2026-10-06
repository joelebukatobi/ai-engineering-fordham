import json
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

task3_src = [
    '# ==========================================',
    '# 3. EMBED THE CHUNKS (Robust & Rate Limited)',
    '# ==========================================',
    'import pickle',
    'import os',
    'import time',
    'from tqdm import tqdm',
    'from dotenv import load_dotenv',
    'from google import genai',
    '',
    'load_dotenv()',
    'client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))',
    '',
    'def get_embedding(text):',
    '    """Get embedding with rate limiting and retry logic."""',
    '    model_name = "models/gemini-embedding-001"',
    '    retries = 3',
    '    for attempt in range(retries):',
    '        try:',
    '            # Rate limiting: Sleep to stay under 100 RPM',
    '            time.sleep(1.0)',
    '            ',
    '            response = client.models.embed_content(',
    '                model=model_name,',
    '                contents=text',
    '            )',
    '            # Correct accessor for google-genai SDK',
    '            return response.embeddings[0].values',
    '            ',
    '        except Exception as e:',
    '            if "429" in str(e):',
    '                print(f"Rate limit hit. Sleeping for 30s... (Attempt {attempt+1}/{retries})")',
    '                time.sleep(30)',
    '                continue',
    '            print(f"Error embedding text: {e}")',
    '            return [0.0] * 768  # Fallback',
    '    return [0.0] * 768',
    '',
    'EMBEDDING_FILE = "../data/smart_embeddings.pkl"',
    '',
    'print("🚀 Starting Smart Embedding Process...")',
    'if "df" not in locals():',
    '    print("⚠️ DataFrame df not found. Please run previous cells.")',
    'else:',
    '    # 1. Chunking',
    '    all_chunks = []',
    '    print(f"Chunking {len(df)} documents...")',
    '    for _, row in tqdm(df.iterrows(), total=len(df)):',
    '        # Ensure content is string',
    '        content = str(row["content"]) if row["content"] else ""',
    '        if not content: continue',
    '            ',
    '        doc_chunks = chunk_document(content)',
    '        for chunk_text in doc_chunks:',
    '            if not chunk_text.strip(): continue',
    '            all_chunks.append({',
    '                "text": chunk_text,',
    '                "filename": row["filename"],',
    '                "url": row["url"]',
    '            })',
    '',
    '    print(f"Total Chunks: {len(all_chunks)}")',
    '',
    '    # 2. Embedding',
    '    print("Generating Embeddings (this may take a while due to rate limits)...")',
    '    vectors = []',
    '    # Batch processing could fail with rate limits, so we stick to single items with sleep',
    '    for i, chunk in enumerate(tqdm(all_chunks)):',
    '        v = get_embedding(chunk["text"])',
    '        vectors.append(v)',
    '',
    '    # 3. Save',
    '    with open(EMBEDDING_FILE, "wb") as f:',
    '        pickle.dump({"chunks": all_chunks, "vectors": vectors}, f)',
    '    print(f"✅ Saved embeddings to {EMBEDDING_FILE}")'
]

try:
    if os.path.exists(nb_path):
        with open(nb_path, 'r') as f:
            nb = json.load(f)
        
        # Update Task 3 (Index 7)
        if len(nb['cells']) > 7:
            nb['cells'][7]['source'] = [l + '\n' for l in task3_src]
            with open(nb_path, 'w') as f:
                json.dump(nb, f, indent=1)
            print("Successfully updated Task 3 with robust logic.")
        else:
             print("Notebook Error: Index 7 out of bounds.")
    else:
        print("Notebook not found.")
except Exception as e:
    print(f"Error: {e}")
