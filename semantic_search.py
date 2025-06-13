import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load repo data
with open("github_repos.json", "r", encoding="utf-8") as f:
    repos = json.load(f)

# Prepare text and metadata
texts = []
metadata = []
for repo in repos:
    combined_text = f"{repo['name']}\n{repo['description']}\n{repo['readme']}"
    texts.append(combined_text)
    metadata.append({
        "name": repo["name"],
        "url": repo["url"],
        "description": repo["description"]
    })

# Load sentence transformer
model = SentenceTransformer('all-MiniLM-L6-v2')  # fast + accurate

# Generate embeddings
embeddings = model.encode(texts, show_progress_bar=True)

# --- Search Interface ---
def search(query, top_k=3):
    query_vec = model.encode([query])
    similarities = cosine_similarity(query_vec, embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]

    print("\n🔍 Top Matching Repositories:\n")
    for i in top_indices:
        print(f"📁 {metadata[i]['name']}")
        print(f"🔗 {metadata[i]['url']}")
        print(f"📝 {metadata[i]['description']}\n")  # emoticons for fun

# Example usage
if __name__ == "__main__":
    while True:
        query = input("\nAsk something about your repos (or type 'exit'): ")
        if query.lower() == 'exit':
            break
        search(query)
