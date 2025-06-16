# Pre-process the query to extract essential keywords
import requests
import json
import os

# Load API key and config
with open("config_private.json", "r", encoding="utf-8") as f:
    config = json.load(f)

HF_API_KEY = config["HF_API_KEY"]
QUERY_MODEL_NAME = config["QUERY_MODEL_NAME"]
EXAMPLES_PATH = config["QUERY_FEW_SHOTS_PATH"]

with open(EXAMPLES_PATH, "r", encoding="utf-8") as f:
    EXAMPLES = json.load(f)

API_URL = f"https://api-inference.huggingface.co/models/{QUERY_MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

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

# ----------- Prompt Builder -----------

def build_prompt_few_shot(user_query):
    formatted_examples = ""
    for ex in EXAMPLES:
        q = ex.get("input", "").strip()
        a = ex.get("output", "").strip()
        formatted_examples += f"User Query: {q}\nEssential Keywords: {a}\n\n"

    prompt = (
        "Transform the following user query into a concise keyword-based version for a codebase/repo search.\n"
        "Here are a few examples:\n\n"
        f"{formatted_examples}"
        f"User Query: {user_query}\n"
        f"Essential Keywords:"
    )
    return prompt

# ----------- Main Condenser Function -----------

def condense_query_with_model(query):
    cache = load_cache()
    if query in cache:
        return cache[query]

    prompt = build_prompt_few_shot(query)

    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        response.raise_for_status()
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            condensed = result[0]["generated_text"].strip()
            cache[query] = condensed
            save_cache(cache)
            return condensed
        else:
            print("⚠️ Unexpected response format:", result)

    except requests.exceptions.HTTPError as e:
        print(f"⚠️ HTTP error: {e}")
        print(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Request error: {e}")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"⚠️ Parsing error: {e}")
        print("Response content:", response.text)

    return query  # Fallback if something goes wrong
