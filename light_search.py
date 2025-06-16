# --- Note ---
# Standalone Light Search mechanism through CLI.
# Not used in final product.

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

# Load embeddings
with open("repo_data_with_embeddings.json", "r", encoding="utf-8") as f:
    repo_data = json.load(f)

# Load model
with open("config_private.json", "r") as f:
    config = json.load(f)
    MODEL_NAME = config["MODEL_NAME"]

model = SentenceTransformer(MODEL_NAME)

# Get query and encode
query = input("🔍 Ask your question: ")
query_embedding = model.encode(query)

# Search
results = []

for item in repo_data:
    best_score = -1

    for chunk_embedding in item["embedding"]:
        similarity = cosine_similarity([query_embedding], [chunk_embedding])[0][0]
        best_score = max(best_score, similarity)

    results.append((best_score, item))

# Sort and show top 3 unique repos
results.sort(reverse=True, key=lambda x: x[0])

number_of_matches = config["NUMBER_OF_MATCHES"]
for score, match in results[:number_of_matches]:
    print(f"\n🔗 Repo: {match['repo_name']} (score: {score:.2f})")
    print(f"📄 Description: {match.get('repo_description', 'N/A')}")

# --- Note ---
# The model sentence-transformers/all-MiniLM-L6-v2 already handles the language context well.
# No query preprocessing has been done as it can harm the context of the user query.