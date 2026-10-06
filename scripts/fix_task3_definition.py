import json
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

# New source for Task 3: Include definition + rebuild loop
# Using Google GenAI as standard
task3_src = [
    '# ==========================================',
    '# 3. EMBED THE CHUNKS (Updated)',
    '# ==========================================',
    '# We need to define `get_embedding` before using it.',
    '# Then we run the full embedding loop with our new Smart Chunker.',
    '# ==========================================',
    '',
    'import pickle',
    'import os',
    'from tqdm import tqdm',
    'from dotenv import load_dotenv',
    'from google import genai',
    '',
    '# Load environment variables',
    'load_dotenv()',
    '',
    '# Initialize Google Gemini Client',
    'client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))',
    '',
    'def get_embedding(text):',
    '    """Get embedding using Google GenAI (text-embedding-004)."""',
    '    try:',
    '        result = client.models.embed_content(',
    '            model="text-embedding-004",',
    '            contents=text',
    '        )',
    '        return result.embedding',
    '    except Exception as e:',
    '        print(f"Error embedding text: {e}")',
    '        return [0.0] * 768  # Return zero vector on failure',
    '',
    '# Define path for new embeddings',
    'EMBEDDING_FILE = "../data/smart_embeddings.pkl"',
    '',
    'print("🚀 Starting Smart Embedding Process...")',
    '',
    'all_chunks = []',
    '',
    '# 1. Re-Chunk All Documents',
    'print(f"Chunking {len(df)} documents with Smart Markdown Chunker...")',
    'for _, row in tqdm(df.iterrows(), total=len(df)):',
    '    # Use our new smart function defined in Task 2',
    '    doc_chunks = chunk_document(row["content"])',
    '    for chunk_text in doc_chunks:',
    '        all_chunks.append({',
    '            "text": chunk_text,',
    '            "filename": row["filename"],',
    '            "url": row["url"]',
    '        })',
    '',
    'print(f"Total Smart Chunks Generated: {len(all_chunks)}")',
    '',
    '# 2. Create Embeddings',
    'print("Generating Embeddings (this may take time)...")',
    'vectors = []',
    '# Simple loop to be safe',
    'for chunk in tqdm(all_chunks):',
    '    v = get_embedding(chunk["text"])',
    '    vectors.append(v)',
    '',
    '# 3. Save',
    'with open(EMBEDDING_FILE, "wb") as f:',
    '    pickle.dump({"chunks": all_chunks, "vectors": vectors}, f)',
    '',
    'print(f"✅ Saved {len(vectors)} smart embeddings to {EMBEDDING_FILE}")'
]

try:
    if os.path.exists(nb_path):
        with open(nb_path, 'r') as f:
            nb = json.load(f)
        
        # Update Task 3 (Index 7 based on previous analysis)
        # This replaces the entire cell content with imports + definition + loop
        if len(nb['cells']) > 7:
            nb['cells'][7]['source'] = [l + '\n' for l in task3_src]
            
            with open(nb_path, 'w') as f:
                json.dump(nb, f, indent=1)
            print("Successfully restored `get_embedding` definition to Task 3.")
        else:
            print("Notebook error: Index 7 out of bounds.")
    else:
        print("Notebook not found.")

except Exception as e:
    print(f"Error: {e}")
