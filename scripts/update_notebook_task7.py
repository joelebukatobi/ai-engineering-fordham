import json
import re
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

# Implementation of Smart Chunker
source_lines = [
    'import re',
    '',
    'def chunk_markdown_smart(text, chunk_size=800, chunk_overlap=200):',
    '    # Regex to split by headers (H1-H3), capturing the header line',
    '    # Note: Regex capture group keeps the delimiter in the result list',
    '    sections = re.split(r"(^#{1,3} .*$)", text, flags=re.MULTILINE)',
    '    ',
    '    chunks = []',
    '    current_chunk = ""',
    '    current_header = ""',
    '    ',
    '    for part in sections:',
    '        part = part.strip()',
    '        if not part: continue',
    '        ',
    '        # If part matches a header pattern',
    '        if re.match(r"^#{1,3} ", part):',
    '            current_header = part',
    '            # Close previous chunk if exists',
    '            if current_chunk:',
    '                chunks.append(current_chunk.strip())',
    '            # Start new chunk with this header as context',
    '            current_chunk = current_header + "\\n"',
    '            continue',
    '            ',
    '        # It is body text. Append to current.',
    '        if len(current_chunk) + len(part) < chunk_size:',
    '            current_chunk += part + "\\n\\n"',
    '        else:',
    '            # Paragraph split for granular control',
    '            paras = part.split("\\n\\n")',
    '            for para in paras:',
    '                if len(current_chunk) + len(para) > chunk_size:',
    '                    chunks.append(current_chunk.strip())',
    '                    # Start fresh with context',
    '                    current_chunk = current_header + "\\n" + para + "\\n"',
    '                else:',
    '                    current_chunk += para + "\\n"',
    '    ',
    '    if current_chunk.strip():',
    '        chunks.append(current_chunk.strip())',
    '        ',
    '    return chunks',
    '',
    'print("Smart Chunker Defined.")',
    '',
    '# Demo on a sample file with dates/deadlines',
    'sample_md = """',
    '# Financial Aid Services',
    '',
    '## Important Dates',
    '- **October 1**: FAFSA Opens',
    '- **February 1**: Priority Deadline',
    '',
    '## Contact Us',
    'Email us at financialaid@fordham.edu',
    '"""',
    '',
    'print("\\n--- Demo: Context Awareness ---")',
    'chunks = chunk_markdown_smart(sample_md, chunk_size=100)',
    'for i, c in enumerate(chunks):',
    '    print(f"CHUNK {i}:\\n{c}\\n---")'
]

# Update Notebook
try:
    if os.path.exists(nb_path):
        with open(nb_path, 'r') as f:
            nb = json.load(f)
        
        target_idx = 16 # Task 7
        if len(nb['cells']) > target_idx:
            # We must add explicit newlines for the cell source list
            nb['cells'][target_idx]['source'] = [l + '\n' for l in source_lines]
            
            with open(nb_path, 'w') as f:
                json.dump(nb, f, indent=1)
            print(f"Success: Updated Task 7 code in {nb_path}")
        else:
            print(f"Error: Notebook has fewer cells than expected ({len(nb['cells'])} cells).")
    else:
        print(f"Notebook not found at {nb_path}")

except Exception as e:
    print(f"Error: {e}")
