import json
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

task3_openai_src = [
    '# ==========================================',
    '# 3. EMBED THE CHUNKS (OpenAI - Batched)',
    '# ==========================================',
    'import pickle',
    'import os',
    'import pandas as pd',
    'from tqdm import tqdm',
    'from dotenv import load_dotenv',
    'from openai import OpenAI',
    '',
    '# SAFETY CHECK: Ensure data is loaded',
    'if "df" not in locals():',
    '    raise RuntimeError("⚠️ ERROR: DataFrame \'df\' is not defined. Please RUN CELL 3 (Data Loading) first!")',
    '',
    'load_dotenv()',
    'client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))',
    '',
    'def get_embeddings_batch(texts, model="text-embedding-3-small"):',
    '    """Get embeddings for a list of texts using OpenAI."""',
    '    if not texts: return []',
    '    try:',
    '        texts = [t.replace("\\n", " ") for t in texts]',
    '        response = client.embeddings.create(input=texts, model=model)',
    '        return [data.embedding for data in response.data]',
    '    except Exception as e:',
    '        print(f"Error embedding batch: {e}")',
    '        return [[0.0] * 1536] * len(texts)',
    '',
    'EMBEDDING_FILE = "../data/smart_embeddings_openai.pkl"',
    '',
    'print("🚀 Starting OpenAI Embedding Process...")',
    '',
    '# 1. Chunking',
    'all_chunks = []',
    'print(f"Chunking {len(df)} documents...")',
    'for _, row in tqdm(df.iterrows(), total=len(df)):',
    '    content = str(row["content"]) if row["content"] else ""',
    '    if not content: continue',
    '    doc_chunks = chunk_document(content)',
    '    for chunk_text in doc_chunks:',
    '        if not chunk_text.strip(): continue',
    '        all_chunks.append({',
    '            "text": chunk_text,',
    '            "filename": row["filename"],',
    '            "url": row["url"]',
    '        })',
    '',
    'print(f"Total Chunks: {len(all_chunks)}")',
    '',
    '# 2. Embedding (Batched)',
    'print("Generating Embeddings in Batches...")',
    'vectors = []',
    'batch_size = 100',
    '',
    'for i in tqdm(range(0, len(all_chunks), batch_size)):',
    '    batch = all_chunks[i:i+batch_size]',
    '    batch_texts = [item["text"] for item in batch]',
    '    batch_vectors = get_embeddings_batch(batch_texts)',
    '    vectors.extend(batch_vectors)',
    '',
    '# 3. Save',
    'with open(EMBEDDING_FILE, "wb") as f:',
    '    pickle.dump({"chunks": all_chunks, "vectors": vectors}, f)',
    'print(f"✅ Saved OpenAI embeddings to {EMBEDDING_FILE}")'
]

try:
    if os.path.exists(nb_path):
        with open(nb_path, 'r') as f:
            nb = json.load(f)
        if len(nb['cells']) > 7:
            nb['cells'][7]['source'] = [l + '\n' for l in task3_openai_src]
            with open(nb_path, 'w') as f:
                json.dump(nb, f, indent=1)
            print("Added safety check to Task 3.")
except Exception as e:
    print(f"Error: {e}")
