from github import Github
import json

"""
This program only indexes the repo names and their metadata for a user.
"""

# 🔑 Replace with your token
ACCESS_TOKEN = "your_personal_access_token"
USERNAME = "your_user_name"

# To load the token and username from a private json
with open("config_private.json", "r") as f:
    config = json.load(f)

ACCESS_TOKEN = config["ACCESS_TOKEN"]
USERNAME = config["USERNAME"]

g = Github(ACCESS_TOKEN)
user = g.get_user(USERNAME)

repo_data = []

for repo in user.get_repos():
    if repo.private:
        continue  # Skip private repos
    try:
        readme = repo.get_readme().decoded_content.decode()
    except:
        readme = ""

    repo_data.append({
        "name": repo.name,
        "url": repo.html_url,
        "description": repo.description or "",
        "readme": readme
    })

# Save to JSON
with open("github_repos.json", "w", encoding="utf-8") as f:
    json.dump(repo_data, f, ensure_ascii=False, indent=2)

print("✅ Repo data saved to github_repos.json")
