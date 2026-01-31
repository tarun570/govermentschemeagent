from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_PATH = BASE_DIR / "schemes.index"
META_PATH = BASE_DIR / "faiss_meta.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")


# -------------------------------------------------
# Word-safe chunking
# -------------------------------------------------
def chunk_text(text, chunk_size=300, overlap_words=20):

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start
        length = 0

        while end < len(words) and length < chunk_size:
            length += len(words[end]) + 1
            end += 1

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start = max(end - overlap_words, start + 1)

    return chunks


# -------------------------------------------------
# Build FAISS index from DB schemes
# -------------------------------------------------
def build_faiss_index(schemes):

    texts = []
    meta = []

    for s in schemes:

        full_text = (
            f"Scheme Name: {s.name}\n"
            f"Eligibility: {s.eligibility}\n"
            f"Benefits: {s.benefits}"
        )

        chunks = chunk_text(full_text)

        for ch in chunks:
            texts.append(ch)

            meta.append({
                "id": s.id,
                "name": s.name,
                "eligibility": s.eligibility,
                "benefits": s.benefits
            })

    if not texts:
        return

    embeddings = model.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))

    with open(META_PATH, "wb") as f:
        pickle.dump(meta, f)


# -------------------------------------------------
# Semantic search
# -------------------------------------------------
def search(query, k=5):

    if not INDEX_PATH.exists():
        return []

    index = faiss.read_index(str(INDEX_PATH))

    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)

    q_vec = model.encode([query])
    q_vec = np.array(q_vec).astype("float32")

    _, ids = index.search(q_vec, k)

    results = []
    seen = set()

    for i in ids[0]:

        item = meta[i]

        if item["id"] not in seen:
            seen.add(item["id"])
            results.append(item)

    return results
