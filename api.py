from flask import Flask, request, jsonify
from flask_cors import CORS
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import re
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Load model and FAISS index
model = SentenceTransformer("fine-tuned-tamilnadu-model")
index = faiss.read_index("index.faiss")

with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

embeddings = np.load("embeddings.npy")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["tnegov"]
officials_collection = db["officials"]

# Detect intent
def detect_intent(query):
    query = query.lower()
    if "list" in query and "department" in query:
        return "list_departments"
    elif "schemes" in query or "initiatives" in query:
        return "schemes"
    elif "ministers" in query or "chief minister" in query or "governor" in query:
        return "leaders"
    else:
        return "general"

# Extract departments from text
def extract_departments(texts):
    department_names = set()
    for text in texts:
        matches = re.findall(r'\b([A-Z][a-zA-Z\s&]+Department)\b', text)
        for match in matches:
            department_names.add(match.strip())
    return sorted(department_names)

# Query MongoDB collection
def mongo_lookup(intent, query):
    if intent == "leaders":
        keywords = ["chief minister", "governor", "minister"]
        pipeline = {
            "$or": [
                {"position": {"$regex": "|".join(keywords), "$options": "i"}},
                {"name": {"$regex": query, "$options": "i"}}
            ]
        }
        docs = officials_collection.find(pipeline)
        results = []
        for doc in docs:
            results.append({
                "text": f"{doc.get('name')} - {doc.get('position')} ({doc.get('departments', [])})",
                "score": 1.0
            })
        return results

    elif intent == "schemes":
        docs = officials_collection.find({"schemes": {"$exists": True}})
        results = []
        for doc in docs:
            results.append({
                "text": f"{doc.get('name')} - Schemes: {', '.join(doc.get('schemes', []))}",
                "score": 1.0
            })
        return results

    elif intent == "list_departments":
        docs = officials_collection.find({}, {"departments": 1})
        departments = set()
        for doc in docs:
            for d in doc.get("departments", []):
                departments.add(d)
        return [{
            "text": "List of Departments:\n" + "\n".join(f"• {d}" for d in sorted(departments)),
            "score": 1.0
        }]

    return []

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"results": []})

    intent = detect_intent(user_query)

    # Check MongoDB first for structured answer
    mongo_results = mongo_lookup(intent, user_query)
    if mongo_results:
        return jsonify({"results": mongo_results})

    # Fallback to vector-based retrieval
    query_emb = normalize(model.encode([user_query]), axis=1)
    D, I = index.search(query_emb, k=15)

    raw_results = []
    for j, i in enumerate(I[0]):
        if D[0][j] >= 0.3:
            raw_results.append({
                "text": chunks[i],
                "score": float(D[0][j])
            })

    final_results = raw_results[:5]
    return jsonify({"results": final_results})

if __name__ == "__main__":
    app.run(debug=True)
