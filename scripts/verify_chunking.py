import zipfile
import re
import os

# 1. Define the Smart Chunker (Same as in Notebook)
def chunk_markdown_smart(text, chunk_size=800):
    # Regex to split by headers (H1-H3), capturing the header line
    sections = re.split(r"(^#{1,3} .*$)", text, flags=re.MULTILINE)
    
    chunks = []
    current_chunk = ""
    current_header = ""
    
    for part in sections:
        part = part.strip()
        if not part: continue
        
        # If it's a header
        if re.match(r"^#{1,3} ", part):
            current_header = part
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = current_header + "\n"
            continue
            
        # Body logic
        if len(current_chunk) + len(part) < chunk_size:
            current_chunk += part + "\n\n"
        else:
            paras = part.split("\n\n")
            for para in paras:
                if len(current_chunk) + len(para) > chunk_size:
                    chunks.append(current_chunk.strip())
                    current_chunk = current_header + "\n" + para + "\n"
                else:
                    current_chunk += para + "\n"
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks

# 2. Run on Real Data
zip_path = "data/fordham-website.zip"
print(f"Loading real data from {zip_path}...")

docs_tested = 0
chunks_generated = 0
chunks_with_headers = 0

if os.path.exists(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Filter for files that likely have structure
        names = [n for n in zf.namelist() if n.endswith('.md')]
        
        # We'll test on 5 files that HAVE headers
        for name in names:
            content = zf.read(name).decode('utf-8', errors='ignore')
            if "## " in content:
                docs_tested += 1
                chunks = chunk_markdown_smart(content)
                chunks_generated += len(chunks)
                
                # Check how many chunks start with a header (#)
                header_starts = sum(1 for c in chunks if c.strip().startswith('#'))
                chunks_with_headers += header_starts
                
                print(f"\nExample from: {os.path.basename(name)}")
                for i, c in enumerate(chunks[:2]): # Show first 2 chunks
                    print(f"  Chunk {i} start: {c.splitlines()[0][:50]}...")
                
                if docs_tested >= 5:
                    break

print("\n" + "="*40)
print(f"VERIFICATION RESULTS")
print(f"Documents Tested: {docs_tested}")
print(f"Total Chunks: {chunks_generated}")
print(f"Chunks preserving Header Context: {chunks_with_headers} ({chunks_with_headers/chunks_generated*100:.1f}%)")
print("="*40)

if chunks_with_headers > 0:
    print("SUCCESS: The logic works! Headers are sticking to chunks.")
else:
    print("FAILURE: Context was lost.")
