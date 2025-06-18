# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types
import json

from config_loader import config_loader
config = config_loader()

# Retrieving API key
GEMINI_API_KEY = config["GEMINI_API_KEY"]

def generate(query):
    client = genai.Client(
        api_key=GEMINI_API_KEY,
    )

    model = "gemini-2.0-flash-lite"

    # Load pre-training examples
    EXAMPLES_PATH = config["QUERY_FEW_SHOTS_PATH"]
    with open(EXAMPLES_PATH, "r", encoding="utf-8") as f:
        examples_json = json.load(f)

    examples_str = json.dumps(examples_json, indent=2)  # Format JSON nicely

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"So, you already have your system instructions. Here are your examples for the prompt design.\n{examples_str}"
),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Excellent! Thank you for providing those examples. They are clear, concise, and cover a good range of potential queries.

I've processed the examples and have a good understanding of the desired output format and the types of keywords you want to extract. I'm ready to receive your next query. Please provide it, and I will transform it based on the examples you've provided.
"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=query),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.3,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are a query preprocessor for my semantic-search based engine which is used as a basic search engine to my GitHub repo. You take in natural language prompts and transform them to contain essential keywords only, so that the search results are accurate."""),
        ],
    )

    # contents.append(types.Content(role="user", parts=[types.Part.from_text(text=query)]))

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        return response.text
    except Exception as e:
        print(f"⚠️ API request failed: {e}")
        return None  # Graceful fallback



if __name__ == "__main__":
    generate()
