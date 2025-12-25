# encoder_without_caching.py
import json
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from transformers import AutoTokenizer
from utils import char_to_token_ratio

from config_loader import config_loader
config = config_loader()

# --- Configuration ---
MODEL_NAME = config["MODEL_NAME"]

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)   # Does not work with non-Hugging Face or Transformer based tools
TOKEN_LIMIT = tokenizer.model_max_length or 512  # Fallback in case it's not set
CHAR_TO_TOKEN_RATIO = char_to_token_ratio(MODEL_NAME)
CHAR_LIMIT = int(TOKEN_LIMIT * CHAR_TO_TOKEN_RATIO)
# INPUT_FILE = ["repo_data.json", "file_data.json"]
# OUTPUT_FILE = ["repo_data_with_embeddings.json", "file_data_with_embeddings.json"]  # storing in new file
# INPUT_FILE = ["repo_data.json"]
# OUTPUT_FILE = ["repo_data_with_embeddings.json"]  # storing in new file
INPUT_FILE = ["file_data.json"]
OUTPUT_FILE = ["file_data_with_embeddings.json"]  # storing in new file

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

# --- Main Processing ---
input_data = []
for i in range(len(INPUT_FILE)):
    with open(INPUT_FILE[i], "r", encoding="utf-8") as f:
        input_data.append(json.load(f))

    print(f"🔍 Embedding {len(input_data[i])} items using {MODEL_NAME}...")

    for data in tqdm(input_data[i], desc="Embedding Data"):
        working_text = prepare_text_for_embedding(data)
        chunks = list(chunk_string(working_text, CHAR_LIMIT))
        data["embedding"] = [model.encode(chunk).tolist() for chunk in chunks]
        # tolist() as encode returns ndarrays which cannot be dumped as json

    # --- Save Output ---
    with open(OUTPUT_FILE[i], "w", encoding="utf-8") as f:
        json.dump(input_data[i], f, ensure_ascii=False, indent=2)

    print(f"✅ Embeddings saved to {OUTPUT_FILE[i]}")
