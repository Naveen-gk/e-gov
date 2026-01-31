import pickle
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import faiss

def extract_texts_from_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    collection = client["tngov"]["officials"]
    texts = []
    for doc in collection.find():
        if "governor" in doc and isinstance(doc["governor"], dict):
            desc = doc["governor"].get("description", "")
            if isinstance(desc, str) and len(desc.strip()) > 30:
                texts.append(desc.strip())

            details = doc["governor"].get("details", [])
            if isinstance(details, list):
                texts += [d.strip() for d in details if isinstance(d, str) and len(d.strip()) > 30]
    return texts

def chunk_text(text, max_len=512):
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]

texts = extract_texts_from_mongo()
chunks = []
for t in texts:
    chunks.extend(chunk_text(t))

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = normalize(model.encode(chunks), axis=1)

# Save embeddings + chunks
np.save("embeddings.npy", embeddings)
with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

# Save FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)
faiss.write_index(index, "index.faiss")

print("✅ Preprocessing done. Files saved: embeddings.npy, chunks.pkl, index.faiss")
