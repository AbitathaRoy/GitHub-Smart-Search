# Pre-process the query to extract essential keywords
# Using Google Gemini API
import requests
import json
import os
from google_genai import generate

from config_loader import config_loader
config = config_loader()

CACHE_PATH = "query_cache.json"

# ----------- Cache Handling -----------

def load_cache():
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Cache file is corrupted. Starting with empty cache.")
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)
        print("✅ Cache saved to", CACHE_PATH)

# ----------- Main Condenser Function -----------

def condense_query_with_model(query):
    cache = load_cache()
    if query in cache:
        return cache[query]

    response = generate(query)

    if response not in (None, ""):
        cache[query] = response  # Store response in cache
        save_cache(cache)  # Save the updated cache
        return response
    else:
        print("⚠️ Unexpected response format:", response)

    return query  # Fallback if something goes wrong
