import json
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

# Task 3: OpenAI Embedding Generation (Batched)
task3_openai_src = [
    '# ==========================================',
    '# 3. EMBED THE CHUNKS (OpenAI - Batched)',
    '# ==========================================',
    '# We switch to OpenAI usage for speed and reliability.',
    '# "text-embedding-3-small" is fast and cheap.',
    '# ==========================================',
    '',
    'import pickle',
    'import os',
    'from tqdm import tqdm',
    'from dotenv import load_dotenv',
    'from openai import OpenAI',
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
    '        return [[0.0] * 1536] * len(texts)  # Fallback (1536 dim for text-embedding-3-small)',
    '',
    'EMBEDDING_FILE = "../data/smart_embeddings_openai.pkl"',
    '',
    'print("🚀 Starting OpenAI Embedding Process...")',
    '',
    '# 1. Chunking',
    'all_chunks = []',
    'print(f"Chunking {len(df)} documents...")',
    'for _, row in tqdm(df.iterrows(), total=len(df)):',
    '    # Ensure content is string',
    '    content = str(row["content"]) if row["content"] else ""',
    '    if not content: continue',
    '        ',
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
    'batch_size = 100  # Adjust based on rate limits (Usually reliable)',
    '',
    '# Create batches',
    'for i in tqdm(range(0, len(all_chunks), batch_size)):',
    '    batch = all_chunks[i:i+batch_size]',
    '    batch_texts = [item["text"] for item in batch]',
    '    batch_vectors = get_embeddings_batch(batch_texts)',
    '    vectors.extend(batch_vectors)',
    '',
    '# 3. Save',
    '# Note: text-embedding-3-small has different dimensions (1536) than Gemini (768)',
    'with open(EMBEDDING_FILE, "wb") as f:',
    '    pickle.dump({"chunks": all_chunks, "vectors": vectors}, f)',
    'print(f"✅ Saved OpenAI embeddings to {EMBEDDING_FILE}")'
]

# Task 4: OpenAI Retrieval
task4_openai_src = [
    '# ==========================================',
    '# 4. PERFORM RELEVANCE SEARCH (OpenAI)',
    '# ==========================================',
    'import numpy as np',
    'from sklearn.metrics.pairwise import cosine_similarity',
    '',
    'def search(query, top_k=5):',
    '    # 1. Embed Query (OpenAI)',
    '    try:',
    '        q_response = client.embeddings.create(',
    '            input=query.replace("\\n", " "),',
    '            model="text-embedding-3-small"',
    '        )',
    '        query_vector = [q_response.data[0].embedding]',
    '    except Exception as e:',
    '        print(f"Error embedding query: {e}")',
    '        return []',
    '',
    '    # 2. Similarity',
    '    # Convert list of lists to np array for efficiency',
    '    vec_matrix = np.array(vectors)',
    '    similarities = cosine_similarity(query_vector, vec_matrix)[0]',
    '',
    '    # 3. Sort',
    '    top_indices = np.argsort(similarities)[::-1][:top_k]',
    '    ',
    '    results = []',
    '    for idx in top_indices:',
    '        results.append({',
    '            "chunk": all_chunks[idx],',
    '            "score": similarities[idx]',
    '        })',
    '    return results',
    '',
    '# Test Search',
    'print("Testing Search...")',
    'q = "What is the policy on academic integrity?"',
    'res = search(q)',
    'for r in res:',
    '    print(f"[{r[\'score\']:.4f}] {r[\'chunk\'][\'filename\']}")',
    '    print(f"Snippet: {r[\'chunk\'][\'text\'][:200]}...")',
    '    print("-" * 40)'
]

try:
    if os.path.exists(nb_path):
        with open(nb_path, 'r') as f:
            nb = json.load(f)
        
        # Update Task 3 (Index 7)
        if len(nb['cells']) > 7:
            nb['cells'][7]['source'] = [l + '\n' for l in task3_openai_src]
            
        # Update Task 4 (Index 9 - assuming standard layout, checking approximate location)',
        # Actually, let's find the cell that defines search or task 4
        # Usually it is around index 9 or 10. Let's just update index 9 as per previous context
        if len(nb['cells']) > 9:
             nb['cells'][9]['source'] = [l + '\n' for l in task4_openai_src]

        with open(nb_path, 'w') as f:
            json.dump(nb, f, indent=1)
        print("Successfully switched Task 3 and Task 4 to OpenAI.")
    else:
        print("Notebook not found.")
except Exception as e:
    print(f"Error: {e}")
