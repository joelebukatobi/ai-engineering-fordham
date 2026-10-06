import json
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

task_eval_src = [
    '# ==========================================',
    '# 7. EVALUATE & IMPROVE (Synthetic Evaluation)',
    '# ==========================================',
    '# To know if our RAG system works, we need to measure it.',
    '# We will use an LLM to generate "Ground Truth" questions for random chunks,',
    '# and then see if our system can find those chunks again.',
    '# ==========================================',
    '',
    'import random',
    'import pandas as pd',
    '',
    'def generate_test_set(n=5):',
    '    """',
    '    Pick N random chunks and ask an LLM to write a question for each.',
    '    This creates a (Question, TargetChunk) test set.',
    '    """',
    '    test_set = []',
    '    if len(all_chunks) < n: n = len(all_chunks)',
    '    # Pick random chunks',
    '    indices = random.sample(range(len(all_chunks)), n)',
    '    ',
    '    print(f"Generating {n} test questions...")',
    '    for idx in indices:',
    '        chunk = all_chunks[idx]',
    '        text = chunk["text"]',
    '        ',
    '        # Ask LLM to generate a question',
    '        try:',
    '            prompt = (',
    '                "Given the following text from Fordham University\'s website, "',
    '                "write a specific question that can be answered using ONLY this text. "',
    '                "Return ONLY the question.\\n\\n"',
    '                f"Text:\\n{text}"',
    '            )',
    '            response = client.chat.completions.create(',
    '                model="gpt-4o-mini",',
    '                messages=[{"role": "user", "content": prompt}],',
    '                temperature=0.7',
    '            )',
    '            question = response.choices[0].message.content.strip()',
    '            ',
    '            test_set.append({',
    '                "question": question,',
    '                "target_filename": chunk["filename"],',
    '                "target_text_signature": text[:50] # Check first 50 chars match',
    '            })',
    '        except Exception as e:',
    '            print(f"Error generating question: {e}")',
    '            ',
    '    return test_set',
    '',
    'def evaluate_system(test_set, top_k=5):',
    '    """',
    '    Run the RAG retrieval for each test question and check if the target chunk',
    '    appears in the top K results.',
    '    """',
    '    score = 0',
    '    print(f"\\nEvaluating on {len(test_set)} questions...")',
    '    ',
    '    for i, item in enumerate(test_set):',
    '        q = item["question"]',
    '        target_sig = item["target_text_signature"]',
    '        ',
    '        # Run Retrieval',
    '        results_df = retrieve(q, top_k=top_k)',
    '        ',
    '        # Check if target is in results',
    '        found = False',
    '        for _, row in results_df.iterrows():',
    '            # We compare the start of the text to identify the chunk',
    '            if row["text"][:50] == target_sig:',
    '                found = True',
    '                break',
    '        ',
    '        if found:',
    '            score += 1',
    '            print(f"✅ Q{i+1}: Found")',
    '        else:',
    '            print(f"❌ Q{i+1}: Missed")',
    '            print(f"   Question: {q}")',
    '            if not results_df.empty:',
    '                print(f"   Top Result: {results_df.iloc[0][\'text\'][:100]}...")',
    '',
    '    recall = score / len(test_set) if len(test_set) > 0 else 0',
    '    print(f"\\nFinal Recall@{top_k}: {recall:.1%} ({score}/{len(test_set)})")',
    '    return recall',
    '',
    '# Run the Evaluation',
    'if "all_chunks" in locals() and len(all_chunks) > 0:',
    '    test_data = generate_test_set(n=5)  # Generate 5 questions',
    '    evaluate_system(test_data)',
    'else:',
    '    print("⚠️ chunks not loaded. Run previous cells.")'
]

try:
    if os.path.exists(nb_path):
        with open(nb_path, 'r') as f:
            nb = json.load(f)
        
        target_index = -1
        # Look for the cell after "# 7. Evaluate"
        found_header = False
        for i, cell in enumerate(nb['cells']):
            src = "".join(cell['source'])
            if "# 7. Evaluate" in src:
                found_header = True
            elif found_header and cell['cell_type'] == 'code':
                target_index = i
                break
        
        if target_index == -1: target_index = 16 # Fallback
        
        if target_index < len(nb['cells']):
             nb['cells'][target_index]['source'] = [l + '\n' for l in task_eval_src]
             with open(nb_path, 'w') as f:
                json.dump(nb, f, indent=1)
             print(f"Successfully updated Task 7 Evaluation logic at Cell {target_index}.")
except Exception as e:
    print(f"Error: {e}")
