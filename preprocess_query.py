# Pre-process the query to extract essential keywords
from transformers import pipeline
import json

# --- Load Config and Examples ---
with open("config_private.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    EXAMPLES_PATH = config["QUERY_FEW_SHOTS_PATH"]

with open(EXAMPLES_PATH, "r", encoding="utf-8") as f:
    EXAMPLES = json.load(f)

# --- Build final prompt with few-shot examples ---
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

# --- Main function to call the model ---
def condense_query_with_model(query, model_name=None):
    if model_name is None:
        model_name = config.get("QUERY_MODEL_NAME", "google/flan-t5-base")
    pipe = pipeline("text2text-generation", model=model_name, device=-1)
    prompt = build_prompt_few_shot(query)
    output = pipe(prompt, max_length=128, do_sample=False)
    return output[0]['generated_text']
