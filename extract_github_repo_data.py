from github import Github
import json
import os
from utils import detect_language_from_extension

"""
This program indexes the repo names, their metadata and the files contained
in them for a user.
"""

# 🔑 Replace with your token
ACCESS_TOKEN = "your_personal_access_token"
USERNAME = "your_user_name"
LOCAL_REPO_PATH = "your_local_repo_path"
FILE_EXTENSION = (
    # Programming languages
    ".py", ".java", ".cpp", ".c", ".js", ".ts", ".rb", ".php", ".go",
    ".swift", ".kt", ".rs", ".lua", ".sh", ".bat", ".pl", ".html", ".css",
    ".sql", ".json", ".xml", ".yaml", ".toml",

    # R language files
    ".r", ".R", ".rmd", ".rdata", ".rds", ".rnw",

    # Mathematical and computational languages
    ".m", ".mlx",  # MATLAB / Octave
    ".nb", ".cdf",  # Mathematica / Wolfram
    ".tex", ".bib", ".sty", ".cls",  # LaTeX
    ".sage",  # SageMath
    ".gp",  # PARI/GP

    # Document formats
    ".pdf", ".doc", ".docx", ".odt", ".txt", ".rtf",

    # Spreadsheet formats
    ".xls", ".xlsx", ".ods", ".csv",

    # Presentation formats
    ".ppt", ".pptx", ".odp",

    # Archive formats
    ".zip", ".tar", ".gz", ".rar",

    # Miscellaneous
    ".md", ".yml"
)

# To load the token and username from a private json
with open("config_private.json", "r") as f:
    config = json.load(f)

ACCESS_TOKEN = config["ACCESS_TOKEN"]
USERNAME = config["USERNAME"]
LOCAL_REPO_PATH = config["LOCAL_REPO_PATH"]

g = Github(ACCESS_TOKEN)
user = g.get_user(USERNAME)

repo_data = []
file_data = []

for repo in user.get_repos():
    if repo.private:
        continue  # Skip private repos
    try:
        readme = repo.get_readme().decoded_content.decode()
    except:
        readme = ""

    repo_data.append({
        "repo_name": repo.name,
        "repo_url": repo.html_url,
        "repo_description": repo.description or "",
        "repo_readme": readme
    })

    # File-level indexing starts here
    local_repo_path = f"{LOCAL_REPO_PATH}/{repo.name}"  # adjust

    for root, dirs, files in os.walk(local_repo_path):
        # Skip hidden folders like .git, __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            matched_ext = next((ext for ext in FILE_EXTENSION if file.endswith(ext)), None)
            if matched_ext:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, local_repo_path)

                # Optimizer for development stage; add triple double-quotes later

                if os.path.getsize(file_path) > 500_000:  # 500 KB
                    continue


                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()
                except Exception as e:
                    code = ""

                file_data.append({
                    "repo_name": repo.name,
                    "repo_url": repo.html_url,
                    "file_path": rel_path.replace("\\", "/"),
                    "language": detect_language_from_extension(matched_ext),
                    "code": code
                })

# Save to JSON
with open("repo_data.json", "w", encoding="utf-8") as f:
    json.dump(repo_data, f, ensure_ascii=False, indent=2)
with open("file_data.json", "w", encoding="utf-8") as f:
    json.dump(file_data, f, ensure_ascii=False, indent=2)

print("✅ Repo data saved to repo_data.json and file_data.json")
print(f"✅ Indexed {len(repo_data)} repos and {len(file_data)} files.")
