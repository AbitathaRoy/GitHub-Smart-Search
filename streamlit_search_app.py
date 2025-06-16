# Old version; not used in final project
import streamlit as st

# MUST BE FIRST Streamlit command (why? :) just a convention I guess)
st.set_page_config(page_title="GitHub AI Search", layout="centered")

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- Configuration ---
CONFIG_PATH = "config_private.json"
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)
MODEL_NAME = config["MODEL_NAME"]
NUMBER_OF_MATCHES = config.get("NUMBER_OF_MATCHES", 3)

# --- Load Data and Model ---
@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)

@st.cache_data
def load_data():
    with open("repo_data_with_embeddings.json", "r", encoding="utf-8") as f:
        return json.load(f)

model = load_model()
data = load_data()

# --- Streamlit UI ---
st.title("🔍 GitHub Repository Search (Light)")

query = st.text_input("Ask your question:")
if query:
    query_embedding = model.encode(query)

    # Search logic
    results = {}
    for item in data:
        best_score = -1
        for chunk_embedding in item["embedding"]:
            score = cosine_similarity([query_embedding], [chunk_embedding])[0][0]
            best_score = max(best_score, score)

        repo_name = item["repo_name"]
        if repo_name not in results or results[repo_name][0] < best_score:
            results[repo_name] = (best_score, item)

    # Display sorted top results
    top_results = sorted(results.values(), reverse=True, key=lambda x: x[0])[:NUMBER_OF_MATCHES]
    for score, match in top_results:
        st.markdown(f"### 🔗 {match['repo_name']} (Score: `{score:.2f}`)")
        st.markdown(f"**Description:** {match.get('repo_description', 'N/A')}")
        st.markdown("---")
