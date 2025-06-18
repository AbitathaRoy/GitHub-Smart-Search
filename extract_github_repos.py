# Old version; not used in final project

from github import Github
import json

from config_loader import config_loader
config = config_loader()

"""
This program only indexes the repo names and their metadata for a user.
"""

# To load the token and username from a private json
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
