import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "tamilnadu_government_info.json")
MODEL_PATH = os.path.join(PROJECT_ROOT, "fine-tuned-tamilnadu-model")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

CHUNKS_PATH = os.path.join(MODELS_DIR, "chunks.pkl")
EMBEDDINGS_PATH = os.path.join(MODELS_DIR, "embeddings.npy")
FAISS_PATH = os.path.join(MODELS_DIR, "index.faiss")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

chunks = []

# Same logic (kept concise)
for cm in data["chief_ministers"]:
    chunks.append(f"{cm['name']} was the Chief Minister during {cm['term']}.")

cm = data["current_chief_minister"]
chunks.append(f"{cm['name']} is the current Chief Minister since {cm['assumed_office']}.")

gov = data["governor"]
chunks.append(f"{gov['name']} is the Governor since {gov['assumed_office']}.")

model = SentenceTransformer(MODEL_PATH)
embeddings = normalize(model.encode(chunks))

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

with open(CHUNKS_PATH, "wb") as f:
    pickle.dump(chunks, f)

np.save(EMBEDDINGS_PATH, embeddings)
faiss.write_index(index, FAISS_PATH)

print("FAISS index rebuilt in models/")