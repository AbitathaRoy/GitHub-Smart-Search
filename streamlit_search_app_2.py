# streamlit_search_app_2.py
import streamlit as st
import time
import os
import requests
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess_query_3 import condense_query_with_model

from config_loader import config_loader
config = config_loader()

# --- Configuration ---
MODEL_NAME = config["MODEL_NAME"]
NUMBER_OF_MATCHES = config.get("NUMBER_OF_MATCHES", 3)
RELEASE_TAG = config["RELEASE_TAG"]
REPO_OWNER = config["REPO_OWNER"]
REPO_NAME = config["REPO_NAME"]

# MUST BE FIRST Streamlit command
st.set_page_config(page_title="GitHub AI Search", layout="centered")

# --- GitHub Release Downloader ---
def get_release_url(file_name):
    return f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/download/{RELEASE_TAG}/{file_name}"

@st.cache_data
def download_or_load_json(file_name):
    if not os.path.exists(file_name):
        url = get_release_url(file_name)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Failed to fetch `{file_name}` from GitHub: {e}")
            return None
        with open(file_name, "wb") as f:
            f.write(response.content)
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Load all data early ---
repo_data_with_embeddings = download_or_load_json("repo_data_with_embeddings.json")
file_data_with_embeddings = download_or_load_json("file_data_with_embeddings.json")

# --- Load Embedding Model ---
@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)

model = load_model()

# --- Search Functions ---
def light_search(query_embedding, data):
    results = {}
    for item in data:
        best_score = -1
        for chunk_embedding in item["embedding"]:
            score = cosine_similarity([query_embedding], [chunk_embedding])[0][0]
            best_score = max(best_score, score)

        repo_name = item["repo_name"]
        if repo_name not in results or results[repo_name][0] < best_score:
            results[repo_name] = (best_score, item)

    top_results = sorted(results.values(), reverse=True, key=lambda x: x[0])[:NUMBER_OF_MATCHES]
    return top_results

def deep_search(query_embedding, file_data, repo_data):
    repo_lookup = {item["repo_name"]: item for item in repo_data}
    results = {}
    for item in file_data:
        repo_name = item["repo_name"]
        for chunk_embedding in item["embedding"]:
            score = cosine_similarity([query_embedding], [chunk_embedding])[0][0]
            if repo_name not in results or results[repo_name][0] < score:
                results[repo_name] = (
                    score,
                    repo_lookup.get(repo_name, {
                        "repo_name": repo_name,
                        "repo_description": "N/A",
                        "repo_url": "#"
                    })
                )
    top_results = sorted(results.values(), reverse=True, key=lambda x: x[0])[:NUMBER_OF_MATCHES]
    return top_results

# --- Display Results ---
def display_results(results, mode, elapsed_time):
    st.markdown(f"**{mode} search results.**")
    st.markdown(f"###### Scanned `{len(repo_data_with_embeddings)}` repos in `{elapsed_time:.2f}` seconds. Displaying top `{NUMBER_OF_MATCHES}` results.\n---")
    for score, item in results:
        repo_url = item.get("repo_url") or f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
        st.markdown(f"### 🔗 [{item['repo_name']}]({repo_url}) (Score: `{score:.2f}`)")
        st.markdown(f"**Description:** {item.get('repo_description', 'N/A')}")
        st.markdown("---")

# --- Streamlit UI ---
st.title("🧠 GitHub Smart Search")

query = st.text_input("Ask your question:")

col1, col2 = st.columns(2)
with col1:
    do_light = st.button("🔦 Light Search")
with col2:
    do_deep = st.button("🧠 Deep Search")

if do_light or do_deep:
    if not query:
        st.warning("⚠️ Please enter a query before searching.")
    else:
        query = condense_query_with_model(query)
        query_embedding = model.encode(query)
        mode = "Deep" if do_deep else "Light"
        start_time = time.time()

        if mode == "Deep":
            results = deep_search(query_embedding, file_data_with_embeddings, repo_data_with_embeddings)
        else:
            results = light_search(query_embedding, repo_data_with_embeddings)

        elapsed_time = time.time() - start_time
        display_results(results, mode, elapsed_time)
