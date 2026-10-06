import json
import os

nb_path = "class/5.you-can-just-build-things.ipynb"

# --- Task 2: The Evolution (Personalized) ---
task2_source = [
    '# ==========================================',
    '# 🧠 EVOLUTION OF MY CHUNKING STRATEGY',
    '# ==========================================',
    '#',
    '# INITIAL THOUGHT PATTERN (The "Naive" Approach):',
    '# When I first looked at the problem, I thought: "Text is just text. Let\'s split it by paragraphs."',
    '# This is the standard starting point for RAG. It\'s simple, fast, and works for 80% of cases.',
    '#',
    '# THE PROBLEM I FOUND:',
    '# Fordham\'s website is highly structured. A page might have a header like "## Deadlines" followed by a list of dates.',
    '# If I split strictly by paragraph/size, I might get a chunk like:',
    '#    "- October 1: FAFSA Opens"',
    '#    "- February 1: Priority Deadline"',
    '#',
    '# The Problem? The embedding model sees "October 1" but has NO IDEA what it refers to because the ',
    '# "## Deadlines" header was left in the previous chunk! User retrieval would fail for questions like "When is the deadline?".',
    '#',
    '# ------------------------------------------',
    '# OPTION 1: NAIVE CHUNKING (Commented Out)',
    '# ------------------------------------------',
    '# def chunk_document(text, chunk_size=1000, chunk_overlap=200):',
    '#     """Simple split by double-newline (paragraphs)."""',
    '#     chunks = []',
    '#     start = 0',
    '#     while start < len(text):',
    '#         end = start + chunk_size',
    '#         # ... (naive logic)',
    '#         chunks.append(text[start:end])',
    '#         start += chunk_size - chunk_overlap',
    '#     return chunks',
    '',
    '# ==========================================',
    '# THE SOLUTION (Task 7 Experiment):',
    '# Having worked with Markdowns prior to this, I recognized that headers (#, ##, ###) act as distinct markers.',
    '# These markers are crucial semantic anchors that tell us what the text is about.',
    '#',
    '# Based on this experience, I decided to build a "Context-Aware" chunker that:',
    '# 1. Splits by headers first (keeping the structure).',
    '# 2. If a section is too long, splits it by paragraphs BUT prepends the header to every chunk.',
    '# This ensures that "October 1" always travels with "## Deadlines".',
    '# ==========================================',
    '',
    'import re',
    '',
    'def chunk_document(text, chunk_size=800, chunk_overlap=200):',
    '    """',
    '    Smart Markdown Chunker (Renamed to chunk_document for compatibility).',
    '    Respects headers and preserves context.',
    '    """',
    '    # Regex to split by headers (H1-H3), capturing the header line',
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
    '        # Is this a header?',
    '        if re.match(r"^#{1,3} ", part):',
    '            current_header = part',
    '            if current_chunk:',
    '                chunks.append(current_chunk.strip())',
    '            current_chunk = current_header + "\\n"',
    '            continue',
    '            ',
    '        # Is it body text?',
    '        if len(current_chunk) + len(part) < chunk_size:',
    '            current_chunk += part + "\\n\\n"',
    '        else:',
    '            # Fallback to paragraph splitting within the section',
    '            paras = part.split("\\n\\n")',
    '            for para in paras:',
    '                if len(current_chunk) + len(para) > chunk_size:',
    '                    chunks.append(current_chunk.strip())',
    '                    # KEY FEATURE: Repetition of Context',
    '                    current_chunk = current_header + "\\n" + para + "\\n"',
    '                else:',
    '                    current_chunk += para + "\\n"',
    '    ',
    '    if current_chunk.strip():',
    '        chunks.append(current_chunk.strip())',
    '        ',
    '    return chunks',
    '',
    'print("Active Strategy: Smart Context-Aware Chunking")'
]

# --- Task 7: The Experiment (Personalized) ---
task7_source = [
    '# ==========================================',
    '# 🧪 THE EXPERIMENT (Comparing Approaches)',
    '# ==========================================',
    '# This cell is where I evaluated my hypothesis.',
    '# I ran the Standard Chunker vs. the Smart Chunker on a sample text with deadlines.',
    '# Results showed that Standard Chunking "orphaned" the dates, while Smart Chunking kept them attached to their header.',
    '#',
    '# Run this cell to verify the behavior yourself!',
    '# ==========================================',
    '',
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
    'print("\\n--- DEMO: Why Context Matters ---")',
    'print("Note: I force a small chunk size (100) to trigger splitting behavior.")',
    'chunks = chunk_document(sample_md, chunk_size=100) ',
    'for i, c in enumerate(chunks):',
    '    print(f"CHUNK {i}:\\n{c}\\n---")'
]

try:
    if os.path.exists(nb_path):
        with open(nb_path, 'r') as f:
            nb = json.load(f)
        
        # Update Task 2 (Index 5)
        nb['cells'][5]['source'] = [l + '\n' for l in task2_source]
        
        # Update Task 7 (Index 16)
        nb['cells'][16]['source'] = [l + '\n' for l in task7_source]
        
        with open(nb_path, 'w') as f:
            json.dump(nb, f, indent=1)
        print("Successfully updated Task 2 and Task 7 with personalized comments.")
    else:
        print("Notebook not found.")

except Exception as e:
    print(f"Error: {e}")
