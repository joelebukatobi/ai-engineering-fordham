import json
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

# --- Task 3: Embed (Force Rebuild) ---
task3_source = [
    '# ==========================================',
    '# 3. EMBED THE CHUNKS (Updated for Smart Chunking)',
    '# ==========================================',
    '# Since we updated cur chunking strategy in Task 2 (My Evolution), we must RE-GENERATE the embeddings.',
    '# We cannot load old embeddings from disk because they use the "naive" chunks.',
    '#',
    '# This cell will:',
    '# 1. Take all loaded documents (from Task 1).',
    '# 2. Re-chunk them using our new smart chunker.',
    '# 3. Create fresh embeddings for each chunk.',
    '# 4. Save to a NEW file: "smart_embeddings.pkl".',
    '# ==========================================',
    '',
    'import pickle',
    'import os',
    'from tqdm import tqdm',
    '',
    '# Define path for new embeddings',
    'EMBEDDING_FILE = "../data/smart_embeddings.pkl"',
    '',
    '# Force Re-Build Logic',
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
    '    # Helper function from earlier cells',
    '    v = get_embedding(chunk["text"])',
    '    vectors.append(v)',
    '',
    '# 3. Save',
    'with open(EMBEDDING_FILE, "wb") as f:',
    '    pickle.dump({"chunks": all_chunks, "vectors": vectors}, f)',
    '',
    'print(f"✅ Saved {len(vectors)} smart embeddings to {EMBEDDING_FILE}")'
]

# --- Task 4: Retrieve (Update Loader) ---
# We just need to update the file path in Task 4 (usually Cell 9)
# to point to "smart_embeddings.pkl"

try:
    if os.path.exists(nb_path):
        with open(nb_path, 'r') as f:
            nb = json.load(f)
        
        # Update Task 3 (Index 7)
        if len(nb['cells']) > 7:
            nb['cells'][7]['source'] = [l + '\n' for l in task3_source]
            print("Updated Task 3 to force rebuild.")
        
        # Update Task 4 (Index 9) - Retrieve
        if len(nb['cells']) > 9:
            task4_src = "".join(nb['cells'][9]['source'])
            # Replace old filename with new one
            if "chunk_embeddings.pkl" in task4_src:
                new_task4 = task4_src.replace("chunk_embeddings.pkl", "smart_embeddings.pkl")
                nb['cells'][9]['source'] = [l + '\n' for l in new_task4.splitlines()]
                print("Updated Task 4 source to use 'smart_embeddings.pkl'.")
            elif "smart_embeddings.pkl" in task4_src:
                print("Task 4 already using smart embeddings.")
            else:
                # If neither found, just prepend the variable definition
                nb['cells'][9]['source'].insert(0, 'EMBEDDING_FILE = "../data/smart_embeddings.pkl"\n')
                print("Injected filename into Task 4.")

        with open(nb_path, 'w') as f:
            json.dump(nb, f, indent=1)
        print("Notebook updated successfully.")
    else:
        print("Notebook not found.")

except Exception as e:
    print(f"Error: {e}")
