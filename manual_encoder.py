"""
For practice; not used.
Encoder with chunking implemented manually.
"""

import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load file data
with open("repo_data.json", "r", encoding="utf-8") as file:
    file_data = json.load(file)
    # file_string = file.read()

# print(type(file_data))
# print(type(file_string))

model = SentenceTransformer('all-MiniLM-L6-v2')  # fast + accurate

for dictionary in file_data:
    start_index = 0
    dictionary["embedding"] = []
    working_string = str({k: v for k, v in dictionary.items() if k != "embedding"})

    # implement the following dynamically irrespective of the model
    token_limit = 1024
    k = 1.1
    char_limit = int(k * token_limit)

    while start_index < len(working_string):
        # Python handles slicing automatically if start_index + char_limit is beyond the string limit
        chunk = working_string[start_index:start_index + char_limit]
        dictionary["embedding"].append(model.encode(chunk))
        start_index += char_limit
