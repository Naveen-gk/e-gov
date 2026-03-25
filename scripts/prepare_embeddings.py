import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import os

# =========================
# Path Setup
# =========================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "tamilnadu_government_info.json")
MODEL_PATH = os.path.join(PROJECT_ROOT, "fine-tuned-tamilnadu-model")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

CHUNKS_PATH = os.path.join(MODELS_DIR, "chunks.pkl")
EMBEDDINGS_PATH = os.path.join(MODELS_DIR, "embeddings.npy")
FAISS_PATH = os.path.join(MODELS_DIR, "index.faiss")

# =========================
# Load JSON
# =========================
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

chunks = []

# Build atomic chunks (same logic as before)
gov = data["governor"]
chunks.append(f"{gov['name']} is the Governor of Tamil Nadu since {gov['assumed_office']}.")

for cm in data["chief_ministers"]:
    chunks.append(f"{cm['name']} served as the Chief Minister during {cm['term']}.")

cm = data["current_chief_minister"]
chunks.append(f"{cm['name']} is the current Chief Minister since {cm['assumed_office']}.")

for dept in cm["departments"]:
    chunks.append(f"{dept} department is handled by Chief Minister {cm['name']}.")

for minister in data["council_of_ministers"]:
    chunks.append(f"{minister['name']} is the {minister['position']} of Tamil Nadu.")
    for dept in minister["departments"]:
        chunks.append(f"{dept} department is handled by {minister['name']}.")

for dept in data["departments"]["list"]:
    chunks.append(f"The {dept['name']} department handles {dept['functions']}.")
    for scheme in dept.get("initiatives", []):
        chunks.append(f"{scheme} is a scheme under the {dept['name']} department.")

# =========================
# Embeddings
# =========================
model = SentenceTransformer(MODEL_PATH)
embeddings = normalize(model.encode(chunks))

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

# =========================
# Save to models/
# =========================
with open(CHUNKS_PATH, "wb") as f:
    pickle.dump(chunks, f)

np.save(EMBEDDINGS_PATH, embeddings)
faiss.write_index(index, FAISS_PATH)

print("Embeddings & FAISS index saved to models/")