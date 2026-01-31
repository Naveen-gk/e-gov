from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import json
from sklearn.preprocessing import normalize

# Load your JSON knowledge
with open("data/tamilnadu_government_info.json", "r", encoding="utf-8") as f:
    data = json.load(f)

chunks = []

# Chief Ministers
for cm in data["chief_ministers"]:
    chunks.append(f"{cm['name']} was the Chief Minister during {cm['term']}.")

# Current Chief Minister
cm = data["current_chief_minister"]
chunks.append(f"{cm['name']} is the current Chief Minister of Tamil Nadu since {cm['assumed_office']}.")
chunks.append(f"The departments handled by {cm['name']} include: {', '.join(cm['departments'])}.")

# Governor
gov = data["governor"]
chunks.append(f"{gov['name']} is the Governor of Tamil Nadu since {gov['assumed_office']}, residing at {gov['residence']}.")

# Ministers
for minister in data["council_of_ministers"]:
    chunks.append(f"{minister['name']} is the {minister['position']} handling: {', '.join(minister['departments'])}.")

# Departments
for dept in data["departments"]["list"]:
    chunks.append(f"{dept['name']} department handles: {dept['functions']}.")
    for scheme in dept.get("initiatives", []):
        chunks.append(f"{dept['name']} runs the scheme: {scheme}.")

# Load fine-tuned model
model = SentenceTransformer("fine-tuned-tamilnadu-model")
embeddings = model.encode(chunks)
embeddings = normalize(embeddings)

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save artifacts
with open("data/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

np.save("data/embeddings.npy", embeddings)
faiss.write_index(index, "data/index.faiss")

print("✅ FAISS index and embeddings rebuilt successfully.")
