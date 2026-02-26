import streamlit as st
import numpy as np
import pickle
import faiss
import os
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Fordham AI Assistant",
    page_icon="🐏",
    layout="centered",
)

st.title("🐏 Fordham University AI Assistant")
st.markdown("Ask any question about Fordham University — admissions, programs, campus life, and more.")

# ─────────────────────────────────────────────
# 1. Load data & build FAISS index (cached — only runs once per session)
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading knowledge base...")
def load_resources():
    """Load chunks, embeddings, build FAISS index, and set up clients."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, None, None, None, "OPENAI_API_KEY not found in .env file."

    client = OpenAI(api_key=api_key)

    # Resolve paths relative to this script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")

    chunks_path = os.path.join(data_dir, "chunks.pkl")
    embeddings_path = os.path.join(data_dir, "embeddings_local.pkl")

    # Validate files exist
    missing = []
    if not os.path.exists(chunks_path):
        missing.append(f"`data/chunks.pkl`")
    if not os.path.exists(embeddings_path):
        missing.append(f"`data/embeddings_local.pkl`")
    if missing:
        return None, None, None, None, (
            f"Missing files: {', '.join(missing)}. "
            "Please run **homework-5.ipynb** top-to-bottom first to generate them."
        )

    # Load chunks
    with open(chunks_path, "rb") as f:
        all_chunks = pickle.load(f)

    # Load vectors
    with open(embeddings_path, "rb") as f:
        data = pickle.load(f)
    vectors = np.array(data["vectors"], dtype="float32")

    # Build FAISS index
    faiss.normalize_L2(vectors)
    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    # Load local embedding model for query encoding
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    return client, all_chunks, index, embed_model, None  # None = no error


client, all_chunks, faiss_index, embed_model, load_error = load_resources()

if load_error:
    st.error(load_error)
    st.stop()

st.success(f"✅ Knowledge base loaded — {len(all_chunks):,} chunks indexed and ready.")

# ─────────────────────────────────────────────
# 2. Retrieval
# ─────────────────────────────────────────────
def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Encode the query with the local model and search FAISS."""
    q_vec = embed_model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(q_vec)
    scores, indices = faiss_index.search(q_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        chunk = all_chunks[idx].copy()
        chunk["score"] = float(score)
        results.append(chunk)

    return results


# ─────────────────────────────────────────────
# 3. Generation
# ─────────────────────────────────────────────
def generate(question: str, context_chunks: list[dict]) -> str:
    """Build a grounded prompt and call GPT-4o-mini."""
    context_parts = [
        f"[Source: {c['url']}]\n{c['text']}"
        for c in context_chunks
    ]
    context = "\n\n---\n\n".join(context_parts)

    system_prompt = (
        "You are a helpful assistant for Fordham University. "
        "Answer the question using ONLY the provided context. "
        "If the answer is not in the context, say so honestly. "
        "Cite the source URLs when relevant. "
        "Keep your answer concise and professional."
    )

    user_prompt = f"Context:\n{context}\n\n---\n\nQuestion: {question}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error during generation: {e}"


# ─────────────────────────────────────────────
# 4. UI
# ─────────────────────────────────────────────
st.divider()

top_k = st.slider("Number of sources to retrieve", min_value=1, max_value=10, value=5)
query = st.text_input("Your Question:", placeholder="e.g., When is the deadline for early action?")

if st.button("Ask", use_container_width=True) and query.strip():
    with st.spinner("Searching Fordham's knowledge base..."):
        chunks = retrieve(query, top_k=top_k)

    if not chunks:
        st.error("No documents found.")
    else:
        with st.spinner("Generating answer..."):
            answer = generate(query, chunks)

        st.markdown("### 💬 Answer")
        st.write(answer)

        with st.expander(f"📚 View {len(chunks)} Source Documents"):
            for c in chunks:
                st.markdown(
                    f"**Score:** `{c['score']:.4f}` | "
                    f"**Source:** [{c['filename']}]({c['url']})"
                )
                st.caption(c["text"][:300] + ("..." if len(c["text"]) > 300 else ""))
                st.divider()
