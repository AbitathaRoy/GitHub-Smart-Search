# encoder.py
import json
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from transformers import AutoTokenizer
from utils import char_to_token_ratio
import hashlib
import os

from config_loader import config_loader
config = config_loader()

# --- Configuration ---

# Fetch Model Name from Config
MODEL_NAME = config["MODEL_NAME"]

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)   # Does not work with non-Hugging Face or Transformer based tools
TOKEN_LIMIT = tokenizer.model_max_length or 512  # Fallback in case it's not set
CHAR_TO_TOKEN_RATIO = char_to_token_ratio(MODEL_NAME)
CHAR_LIMIT = int(TOKEN_LIMIT * CHAR_TO_TOKEN_RATIO)
# INPUT_FILE = ["repo_data.json", "file_data.json"]
INPUT_FILE = ["repo_data.json"]
# OUTPUT_FILE = ["repo_data_with_embeddings.json", "file_data_with_embeddings.json"]  # storing in new file
OUTPUT_FILE = ["repo_data_with_embeddings.json"]

# --- Load Embedding Model ---
model = SentenceTransformer(MODEL_NAME)

# --- Helper Function: Chunk a String ---
def chunk_string(text, chunk_size):
    """Yields successive chunk_size chunks from text."""
    for start in range(0, len(text), chunk_size):
        # yield: return keyword which does not exit the function after returning a value
        # Allows streaming-like activity
        yield text[start:start + chunk_size]

# --- Helper Function: Prepare a Dictionary for Embedding ---
def prepare_text_for_embedding(data):
    """Prepare string to embed by excluding the embedding key."""
    return str({k: v for k, v in data.items() if k != "embedding"})

# Hash function
def compute_hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()

# --- Main Processing ---
input_data = []
for i in range(len(INPUT_FILE)):
    with open(INPUT_FILE[i], "r", encoding="utf-8") as f:
        input_data.append(json.load(f))

    print(f"🔍 Embedding {len(input_data[i])} items using {MODEL_NAME}...")

    # Load cache
    try:
        with open("embedding_cache.json", "r", encoding="utf-8") as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = {}

    this_file_cache = cache.get(INPUT_FILE[i], {})
    updated_file_cache = {}

    for data in tqdm(input_data[i], desc="Embedding Data"):
        unique_id = data.get("repo_name")
        text_to_embed = prepare_text_for_embedding(data)
        current_hash = compute_hash(text_to_embed)

        if unique_id in this_file_cache and this_file_cache[unique_id] == current_hash:
            continue  # Skip embedding

        chunks = list(chunk_string(text_to_embed, CHAR_LIMIT))
        data["embedding"] = [model.encode(chunk).tolist() for chunk in chunks]
        updated_file_cache[unique_id] = current_hash

    updated_file_cache = {**this_file_cache, **updated_file_cache}  # Preserve previous cache entries
    cache[INPUT_FILE[i]] = updated_file_cache

    with open("embedding_cache.json.tmp", "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)
    os.replace("embedding_cache.json.tmp", "embedding_cache.json")  # Atomic write

    # --- Save Cache and Output ---

    with open(OUTPUT_FILE[i], "w", encoding="utf-8") as f:
        json.dump(input_data[i], f, ensure_ascii=False, indent=2)

    print(f"✅ Embeddings saved to {OUTPUT_FILE[i]}")

