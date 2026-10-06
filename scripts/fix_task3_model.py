import json
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

task3_src = [
    '# ==========================================',
    '# 3. EMBED THE CHUNKS (Updated)',
    '# ==========================================',
    '# We use "models/gemini-embedding-001" which is available for this API key.',
    '# ==========================================',
    '',
    'import pickle',
    'import os',
    'from tqdm import tqdm',
    'from dotenv import load_dotenv',
    'from google import genai',
    '',
    'load_dotenv()',
    'try:',
    '    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))',
    'except ValueError:',
    '    print("⚠️ Warning: GEMINI_API_KEY not found in environment. Please set it in .env file.")',
    '    client = None',
    '',
    'def get_embedding(text):',
    '    """Get embedding using Google GenAI (gemini-embedding-001)."""',
    '    if not client: return [0.0] * 768',
    '    try:',
    '        result = client.models.embed_content(',
    '            model="models/gemini-embedding-001",',
    '            contents=text',
    '        )',
    '        return result.embedding',
    '    except Exception as e:',
    '        print(f"Error embedding text: {e}")',
    '        return [0.0] * 768  # Fallback',
    '',
    'EMBEDDING_FILE = "../data/smart_embeddings.pkl"',
    '',
    'print("🚀 Starting Smart Embedding Process...")',
    '',
    'all_chunks = []',
    'print(f"Chunking {len(df)} documents...")',
    'for _, row in tqdm(df.iterrows(), total=len(df)):',
    '    doc_chunks = chunk_document(row["content"])',
    '    for chunk_text in doc_chunks:',
    '        all_chunks.append({',
    '            "text": chunk_text,',
    '            "filename": row["filename"],',
    '            "url": row["url"]',
    '        })',
    '',
    'print(f"Total Chunks: {len(all_chunks)}")',
    '',
    'print("Generating Embeddings...")',
    'vectors = []',
    'for chunk in tqdm(all_chunks):',
    '    v = get_embedding(chunk["text"])',
    '    vectors.append(v)',
    '',
    'with open(EMBEDDING_FILE, "wb") as f:',
    '    pickle.dump({"chunks": all_chunks, "vectors": vectors}, f)',
    'print(f"✅ Saved embeddings to {EMBEDDING_FILE}")'
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
            print("Successfully updated Task 3 with correct model name.")
        else:
             print("Notebook Error: Index 7 out of bounds.")
    else:
        print("Notebook not found.")
except Exception as e:
    print(f"Error: {e}")
