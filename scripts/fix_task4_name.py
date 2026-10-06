import json
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

task4_openai_src = [
    '# ==========================================',
    '# 4. PERFORM RELEVANCE SEARCH (OpenAI)',
    '# ==========================================',
    'import numpy as np',
    'import pandas as pd',
    'from sklearn.metrics.pairwise import cosine_similarity',
    '',
    'def retrieve(query, top_k=5):',
    '    """Retrieve relevant chunks for a query using OpenAI embeddings."""',
    '    # 1. Embed Query (OpenAI)',
    '    try:',
    '        q_response = client.embeddings.create(',
    '            input=query.replace("\\n", " "),',
    '            model="text-embedding-3-small"',
    '        )',
    '        query_vector = [q_response.data[0].embedding]',
    '    except Exception as e:',
    '        print(f"Error embedding query: {e}")',
    '        return pd.DataFrame()',
    '',
    '    # 2. Similarity',
    '    if not vectors: return pd.DataFrame()',
    '    ',
    '    # Convert list of lists to np array for efficiency',
    '    vec_matrix = np.array(vectors)',
    '    similarities = cosine_similarity(query_vector, vec_matrix)[0]',
    '',
    '    # 3. Sort',
    '    top_indices = np.argsort(similarities)[::-1][:top_k]',
    '    ',
    '    results = []',
    '    for idx in top_indices:',
    '        chunk_data = all_chunks[idx].copy()',
    '        chunk_data["score"] = similarities[idx]',
    '        chunk_data["chunk_text"] = chunk_data["text"]',
    '        results.append(chunk_data)',
    '    ',
    '    return pd.DataFrame(results)',
    '',
    'print("Testing Retrieve...")',
    'q = "What is the policy on academic integrity?"',
    'if "vectors" in locals() and len(vectors) > 0:',
    '    res_df = retrieve(q)',
    '    print(res_df[["filename", "score", "chunk_text"]].head())',
    'else:',
    '    print("⚠️ Vectors not loaded yet. Run previous cells!")'
]

try:
    if os.path.exists(nb_path):
        with open(nb_path, 'r') as f:
            nb = json.load(f)
        
        target_index = -1
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'markdown' and "# 4. Retrieve" in "".join(cell['source']):
                target_index = i + 1 
                break
        
        if target_index != -1 and target_index < len(nb['cells']):
             nb['cells'][target_index]['source'] = [l + '\n' for l in task4_openai_src]
             with open(nb_path, 'w') as f:
                json.dump(nb, f, indent=1)
             print(f"Successfully updated Task 4 (Cell {target_index}) to define 'retrieve'.")
        else:
             if len(nb['cells']) > 9:
                 nb['cells'][9]['source'] = [l + '\n' for l in task4_openai_src]
                 with open(nb_path, 'w') as f:
                    json.dump(nb, f, indent=1)
                 print("Updated Task 4 at index 9 (fallback).")
             else:
                 print("Could not find Task 4 cell.")

except Exception as e:
    print(f"Error: {e}")
