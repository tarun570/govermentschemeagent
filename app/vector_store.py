from sentence_transformers import SentenceTransformer
import faiss
import pickle

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_faiss_index(schemes):
    texts = []

    for s in schemes:
        txt = f"{s.name}. Eligibility: {s.eligibility}. Benefits: {s.benefits}"
        texts.append(txt)

    embeddings = model.encode(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "schemes.index")

    with open("faiss_meta.pkl", "wb") as f:
        pickle.dump(texts, f)


def search(query, k=3):
    index = faiss.read_index("schemes.index")

    with open("faiss_meta.pkl", "rb") as f:
        texts = pickle.load(f)

    q = model.encode([query])
    _, ids = index.search(q, k)

    return [texts[i] for i in ids[0]]
