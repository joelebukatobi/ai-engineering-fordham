import json
import os
import zipfile
import random
import re

# 1. Notebook Status
nb_path = "class/5.you-can-just-build-things.ipynb"
print(f"--- Notebook Status ({nb_path}) ---")
if os.path.exists(nb_path):
    try:
        with open(nb_path) as f:
            nb = json.load(f)
        
        # Check Task 6 (Rag wiring)
        has_task6 = any("def rag(" in "".join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')
        if has_task6:
            print("Status: Task 6 (Wire everything) is IMPLEMENTED.")
        else:
            print("Status: Task 6 is NOT implemented.")
            
        # Check Task 7 (Evaluate)
        # Task 7 is usually the last code cell or near the end
        task7_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
        if task7_cells:
            last_cell_src = "".join(task7_cells[-1]['source'])
            if "def " in last_cell_src or "import " in last_cell_src:
                print("Status: Task 7 (Evaluate) seems to have code.")
            else:
                print("Status: Task 7 (Evaluate) appears to be a placeholder.")
    except Exception as e:
        print(f"Error reading notebook: {e}")
else:
    print("Notebook not found at", nb_path)

# 2. Data Structure
zip_path = "data/fordham-website.zip"
unzipped_path = os.path.expanduser("~/data/fordham-website")
print("\n--- Data Structure Analysis ---")

texts = []
source_msg = ""

if os.path.exists(unzipped_path):
    print(f"Found unzipped data at {unzipped_path}")
    source_msg = "unzipped directory"
    all_files = [os.path.join(unzipped_path, f) for f in os.listdir(unzipped_path) if f.endswith('.md')]
    if all_files:
        sample_files = random.sample(all_files, min(20, len(all_files)))
        for fpath in sample_files:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                texts.append(f.read())
elif os.path.exists(zip_path):
    print(f"Found zip data at {zip_path}")
    source_msg = "zip file"
    with zipfile.ZipFile(zip_path, 'r') as zf:
        all_names = [n for n in zf.namelist() if n.endswith('.md')]
        if all_names:
            sample_names = random.sample(all_names, min(20, len(all_names)))
            for name in sample_names:
                texts.append(zf.read(name).decode('utf-8', errors='ignore'))
else:
    print("No data found (neither ~/data/fordham-website nor data/fordham-website.zip)")

# 3. Analyze Structure
if texts:
    print(f"Analyzed {len(texts)} random files from {source_msg}.")
    
    counts = {"h1": 0, "h2": 0, "h3": 0, "bold": 0, "list": 0, "table": 0, "divider": 0}
    for text in texts:
        if re.search(r'^# ', text, re.M): counts["h1"] += 1
        if re.search(r'^## ', text, re.M): counts["h2"] += 1
        if re.search(r'^### ', text, re.M): counts["h3"] += 1
        if "**" in text: counts["bold"] += 1
        if re.search(r'^- ', text, re.M): counts["list"] += 1
        if "|" in text and "---" in text: counts["table"] += 1
        if re.search(r'^---', text, re.M): counts["divider"] += 1

    print("Feature occurrences (in tested files):")
    for k, v in counts.items():
        print(f"  {k}: {v}/{len(texts)}")

    # Print a sample snippet with good structure
    print("\n--- Sample File Content (first 500 chars) ---")
    # Pick a file with headers
    structured_texts = [t for t in texts if "##" in t]
    sample = structured_texts[0] if structured_texts else texts[0]
    print(sample[:500])
