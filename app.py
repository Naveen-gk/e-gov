import streamlit as st
st.set_page_config(page_title="GTN Chatbot", page_icon="🤖")

import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

#  Load model and data
@st.cache_resource
def load_all():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = np.load("embeddings.npy")
    with open("chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    index = faiss.read_index("index.faiss")
    return model, index, chunks

model, index, chunks = load_all()

# Search logic
def find_chunks(query, top_k=5, threshold=0.3):
    query_emb = normalize(model.encode([query]), axis=1)
    D, I = index.search(query_emb, k=top_k)
    results = [(chunks[i], D[0][j]) for j, i in enumerate(I[0]) if D[0][j] >= threshold]
    return results

#  UI
st.title("GTN Governance Chatbot")

query = st.text_input("Ask about the Tamil Nadu Government ")
if query:
    st.info("Searching...")
    results = find_chunks(query)
    if not results:
        st.warning("No valid info found ")
    else:
        for i, (text, score) in enumerate(results):
            with st.expander(f"🔎 Match {i+1} (Confidence: {score:.2f})"):
                st.write(text)
