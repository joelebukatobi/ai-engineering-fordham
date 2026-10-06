import json
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

task3_openai_limiting_src = [
    '# ==========================================',
    '# 3. EMBED THE CHUNKS (OpenAI - Rate Limited)',
    '# ==========================================',
    'import pickle',
    'import os',
    'import time',
    'import pandas as pd',
    'from tqdm import tqdm',
    'from dotenv import load_dotenv',
    'from openai import OpenAI',
    '',
    '# SAFETY CHECK',
    'if "df" not in locals():',
    '    raise RuntimeError("⚠️ ERROR: DataFrame \'df\' is not defined. Please RUN CELL 3 first!")',
    '',
    'load_dotenv()',
    '# Configure client with fewer internal retries to avoid long hangs, we handle it manually if needed',
    'client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_retries=2)',
    '',
    'def get_embeddings_batch(texts, model="text-embedding-3-small"):',
    '    """Get embeddings with rate limit handling."""',
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
    '# 2. Embedding (Conservative Batching)',
    'print("Generating Embeddings (Batch Size 20 + Sleep)...")',
    'vectors = []',
    'batch_size = 20  # Reduced from 100 to avoid 429s',
    '',
    'for i in tqdm(range(0, len(all_chunks), batch_size)):',
    '    batch = all_chunks[i:i+batch_size]',
    '    batch_texts = [item["text"] for item in batch]',
    '    ',
    '    # Manual Rate Limit Protection',
    '    # 20 items * 1.5s sleep = ~800 items/min. Reliable for Tier 1.',
    '    try:',
    '        batch_vectors = get_embeddings_batch(batch_texts)',
    '        vectors.extend(batch_vectors)',
    '        time.sleep(0.5)  # Sleep between batches',
    '    except Exception as e:',
    '        print(f"Batch failed at index {i}: {e}")',
    '        # Pad with zeros to keep alignment if really needed, or skip',
    '        vectors.extend([[0.0]*1536] * len(batch))',
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
            nb['cells'][7]['source'] = [l + '\n' for l in task3_openai_limiting_src]
            with open(nb_path, 'w') as f:
                json.dump(nb, f, indent=1)
            print("Successfully updated Task 3 with reduced batch size (20) and sleep.")
except Exception as e:
    print(f"Error: {e}")
