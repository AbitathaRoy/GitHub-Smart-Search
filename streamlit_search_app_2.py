# streamlit_search_app_2.py
import streamlit as st
import time

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

def light_search(query_embedding, dataset):
    @st.cache_data
    def load_data():
        with open(dataset, "r", encoding="utf-8") as f:
            return json.load(f)

    data = load_data()

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

    # Sort top results
    top_results = sorted(results.values(), reverse=True, key=lambda x: x[0])[:NUMBER_OF_MATCHES]

    return top_results

def deep_search(query_embedding, file_dataset, repo_dataset):
    # Load data
    @st.cache_data
    def load_file_data():
        with open(file_dataset, "r", encoding="utf-8") as f:
            return json.load(f)

    @st.cache_data
    def load_repo_data():
        with open(repo_dataset, "r", encoding="utf-8") as f:
            return json.load(f)

    file_data = load_file_data()
    repo_data = load_repo_data()

    # Convert repo_data to a lookup
    repo_lookup = {item["repo_name"]: item for item in repo_data}

    # Compute scores from file_data
    results = {}
    for item in file_data:
        repo_name = item["repo_name"]
        for chunk_embedding in item["embedding"]:
            score = cosine_similarity([query_embedding], [chunk_embedding])[0][0]
            if repo_name not in results or results[repo_name][0] < score:
                results[repo_name] = (score, repo_lookup.get(repo_name, {"repo_name": repo_name, "repo_description": "N/A", "repo_url": "#"})
)

    # Sort and return top results
    top_results = sorted(results.values(), reverse=True, key=lambda x: x[0])[:NUMBER_OF_MATCHES]
    return top_results

def display_results(results, mode, elapsed_time):
    st.markdown(f"**{mode} search results.**")
    # To count number of repos scanned
    with open("repo_data.json", "r", encoding="utf-8") as file:
        repo_data = json.load(file)
    st.markdown(f"###### Scanned `{len(repo_data)}` repos in `{elapsed_time:.2f}` seconds. Displaying top `{NUMBER_OF_MATCHES}` results.\n---")
    for score, item in results:
        # st.json(item)  # DEBUG LINE
        st.markdown(f"### 🔗 [{item['repo_name']}]({item.get('repo_url', '#')}) (Score: `{score:.2f}`)")
        st.markdown(f"**Description:** {item.get('repo_description', 'N/A')}")
        st.markdown("---")

model = load_model()

# --- Streamlit UI ---
st.title("🧠 GitHub Smart Search")

query = st.text_input("Ask your question:")

# Buttons for search modes
col1, col2 = st.columns(2)
with col1:
    do_light = st.button("🔦 Light Search")
with col2:
    do_deep = st.button("🧠 Deep Search")

if query:
    query_embedding = model.encode(query)

    # Detect if user just typed and pressed enter (no button clicked)
    trigger_default_light = query and not (do_light or do_deep)

    # Choose search mode
    if query and (trigger_default_light or do_light or do_deep):
        import time

        start_time = time.time()
        query_embedding = model.encode(query)

        if do_deep:
            results = deep_search(query_embedding, "file_data_with_embeddings.json", "repo_data_with_embeddings.json")
            mode = "Deep"
        else:  # default OR light search
            results = light_search(query_embedding, "repo_data_with_embeddings.json")
            mode = "Light"

        elapsed_time = time.time() - start_time
        display_results(results, mode, elapsed_time)