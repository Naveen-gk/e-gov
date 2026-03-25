from flask import Flask, request, jsonify, render_template  # Added render_template
from flask_cors import CORS
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
from pymongo import MongoClient
import os

# =========================
# Configuration & Path Fixes
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # This is inside /app
PROJECT_ROOT = os.path.dirname(BASE_DIR)              # This is the root folder /SRC

# Initialize Flask with specific folders based on your directory structure
app = Flask(__name__, 
            template_folder=os.path.join(PROJECT_ROOT, "templates"),
            static_folder=os.path.join(PROJECT_ROOT, "static"))

CORS(app)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
PORT = int(os.getenv("PORT", 5000))

# =========================
# Model & Index Paths
# =========================
MODEL_PATH = os.path.join(PROJECT_ROOT, "fine-tuned-tamilnadu-model")
FAISS_PATH = os.path.join(PROJECT_ROOT, "models", "index.faiss")
CHUNKS_PATH = os.path.join(PROJECT_ROOT, "models", "chunks.pkl")
EMBEDDINGS_PATH = os.path.join(PROJECT_ROOT, "models", "embeddings.npy")

print("Loading model and index...")
model = SentenceTransformer(MODEL_PATH)
index = faiss.read_index(FAISS_PATH)

with open(CHUNKS_PATH, "rb") as f:
    chunks = pickle.load(f)
print("Model loaded successfully.")

# =========================
# MongoDB Setup
# =========================
client = MongoClient(MONGO_URI)
db = client["tnegov"]
officials_collection = db["officials"]

# ... [Intent Detection, Mongo Lookup, and Vector Search functions remain the same] ...

# =========================
# WEB ROUTES (To fix the styling issue)
# =========================

@app.route("/")
def index():
    # This renders the home page with all CSS/JS linked via url_for
    return render_template("index.html")

@app.route("/departments")
def departments():
    return render_template("departments.html")

@app.route("/schemes")
def schemes():
    return render_template("schemes.html")

@app.route("/services")
def services():
    return render_template("services.html")

# =========================
# API ROUTES
# =========================
@app.route("/query", methods=["POST"])
def query():
    try:
        data = request.get_json()
        user_query = data.get("query", "").strip()
        if not user_query:
            return jsonify({"reply": "Please enter a valid question."})

        intent = detect_intent(user_query)
        structured_reply = mongo_lookup(intent, user_query)
        if structured_reply:
            return jsonify({"reply": structured_reply})

        vector_reply = vector_search(user_query)
        if vector_reply:
            return jsonify({"reply": vector_reply})

        return jsonify({"reply": "Sorry, I could not find relevant information."})
    except Exception:
        return jsonify({"reply": "An internal error occurred."}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})

if __name__ == "__main__":
    # Note: Using port 5000 by default; change to 8080 if needed
    app.run(host="0.0.0.0", port=PORT, debug=True)