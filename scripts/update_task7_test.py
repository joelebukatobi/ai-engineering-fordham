import json
import re
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

source_lines = [
    '# Test Comparison: Standard vs Smart Chunking',
    'import re',
    '',
    '# 1. Define Smart Chunker',
    'def chunk_markdown_smart(text, chunk_size=800):',
    '    # Split by headers (H1-H3), capturing the header line',
    '    sections = re.split(r"(^#{1,3} .*$)", text, flags=re.MULTILINE)',
    '    chunks = []',
    '    current_chunk = ""',
    '    current_header = ""',
    '    ',
    '    for part in sections:',
    '        part = part.strip()',
    '        if not part: continue',
    '        ',
    '        if re.match(r"^#{1,3} ", part):',
    '            current_header = part',
    '            if current_chunk:',
    '                chunks.append(current_chunk.strip())',
    '            current_chunk = current_header + "\\n"',
    '            continue',
    '            ',
    '        # Body Text',
    '        if len(current_chunk) + len(part) < chunk_size:',
    '            current_chunk += part + "\\n\\n"',
    '        else:',
    '            paras = part.split("\\n\\n")',
    '            for para in paras:',
    '                if len(current_chunk) + len(para) > chunk_size:',
    '                    chunks.append(current_chunk.strip())',
    '                    current_chunk = current_header + "\\n" + para + "\\n"',
    '                else:',
    '                    current_chunk += para + "\\n"',
    '    ',
    '    if current_chunk.strip():',
    '        chunks.append(current_chunk.strip())',
    '    return chunks',
    '',
    '# 2. Get Sample Document for Comparison',
    'try:',
    '    mask = df["content"].str.contains("## ", na=False) & df["content"].str.contains("deadline", case=False, na=False)',
    '    if mask.any():',
    '        sample_idx = df[mask].index[0]',
    '        sample_text = df.iloc[sample_idx]["content"]',
    '        print(f"Using REAL document: {df.iloc[sample_idx][\'filename\']}")',
    '    else:',
    '        raise ValueError("No matching document found in DF")',
    'except NameError:',
    '    print("DF not loaded (kernel restart?), using FALLBACK text.")',
    '    sample_text = """# Financial Aid Services\\n\\n## Important Dates\\n- **October 1**: FAFSA Opens\\n- **February 1**: Priority Deadline\\n\\n## Contact Us\\nEmail use at financialaid@fordham.edu"""',
    'except Exception as e:',
    '    print(f"Error finding doc: {e}, using FALLBACK.")',
    '    sample_text = """# Header 1\\nContent A.\\n\\n## Header 2\\nContent B."""',
    '',
    '# 3. Compare Outputs',
    'print(f"\\n--- STANDARD CHUNKING (Old) ---")',
    'try:',
    '    std_chunks = chunk_document(sample_text)',
    'except NameError:',
    '    std_chunks = ["chunk_document not defined, skipping."]',
    '',
    'for i, c in enumerate(std_chunks[:3]):',
    '    print(f"[Old Chunk {i}]\\n{c[:80].replace(chr(10), " ")}...")',
    '',
    'print(f"\\n--- SMART CHUNKING (New) ---")',
    'smart_chunks = chunk_markdown_smart(sample_text)',
    'for i, c in enumerate(smart_chunks[:3]):',
    '    print(f"[New Chunk {i}]\\n{c.replace(chr(10), " ")}...")',
]

try:
    if os.path.exists(nb_path):
        with open(nb_path, 'r') as f:
            nb = json.load(f)
        
        target_idx = 16 
        if len(nb['cells']) > target_idx:
            nb['cells'][target_idx]['source'] = [l + '\n' for l in source_lines]
            with open(nb_path, 'w') as f:
                json.dump(nb, f, indent=1)
            print("Successfully updated Task 7 test script.")
        else:
             print("Notebook Error: Index 16 out of bounds.")
    else:
        print("Notebook not found.")
except Exception as e:
    print(f"Error: {e}")
