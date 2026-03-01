
# 📘 Project Report: GitHub Smart Search (AI GitHub Indexer)

### 🔧 Maintainer: [@AbitathaRoy](https://github.com/AbitathaRoy)  
### 🗂️ Codebase: `GitHub-Smart-Search`  
### 🧠 Concept: Semantic search over personal GitHub repositories

---

## 🔰 Project Objective

To create a **semantic search engine** that allows the user to input a natural language query and retrieve the most relevant repositories from their own GitHub account based on:

- Repository metadata (`name`, `description`, `README`)
- Optionally: embedded content from individual files (Deep Search)
- Using **sentence-transformer** models to generate vector embeddings
- Implemented via a **Streamlit app** for a clean UI/UX

---

## 🏗️ Components Summary

### ✅ Core Components Implemented

| Component | Description |
|----------|-------------|
| `repo_data.json`, `file_data.json` | Raw metadata extracted from cloned GitHub repos |
| `encoder.py` | Embeds the above data using `SentenceTransformer`, saving to `*_with_embeddings.json` |
| `streamlit_search_app_2.py` | Streamlit UI with Light and Deep Search |
| `config_loader.py` | Reads config either from `secrets.toml` (Streamlit Cloud) or `config_private.json` locally |
| `requirements.txt` | Manually maintained Python dependency file |
| GitHub Releases Integration | App fetches large pre-embedded JSON files from GitHub Releases instead of bundling them in the repo |

---

## 💡 Key Ideas & Concepts

### Light vs Deep Search

- **Light Search:** Operates only on metadata and READMEs.
- **Deep Search:** Uses chunked embeddings from individual files for higher relevance — currently under development due to size/performance constraints.

### Caching Strategy

- Introduced a **hash-based embedding cache** using `embedding_cache.json` to skip re-embedding unchanged repos.
- Issue: Some embedded files were missing from output due to a bug; currently reverted to a non-caching version for stability.

### JSON File Hosting via GitHub Releases

- App dynamically downloads large JSON embedding files (`repo_data_with_embeddings.json`, `file_data_with_embeddings.json`) from a GitHub Release.
- Prevents bloating the Git repo and circumvents GitHub's LFS limits.
- Used `requests.get()` with caching to manage local persistence.

### Config Fallback

```python
try:
    import streamlit as st
    config = st.secrets[...]
except:
    config = json.load(open("config_private.json"))
```

- Ensures seamless transition between local and hosted environments.

---

## 🧪 Current Testing Status

| Feature        | Status  | Notes |
|----------------|---------|-------|
| Light Search   | ✅ Working locally and in Cloud |
| Deep Search    | ⚠️ Partially implemented | Requires full file embedding, which is not stable yet |
| Caching System | ⚠️ Buggy | Causes missing outputs; reverted to stable version |
| Hosted App     | ⚠️ In alpha | Boots successfully; ongoing work to polish |
| Release-based Downloads | ✅ Works perfectly with cached `.json` files |

---

## 📁 File Structure Snapshot

```
.
├── encoder.py
├── streamlit_search_app_2.py
├── config_loader.py
├── config_private.json (local)
├── requirements.txt
├── repo_data.json / file_data.json
├── repo_data_with_embeddings.json / file_data_with_embeddings.json
├── embedding_cache.json
└── .streamlit/
    └── secrets.toml (for cloud hosting)
```

---

## 📦 Current Version Release Note (`v1.0.0-alpha`)

> This is the **first release** of my GitHub Smart Search application.
>
> **What works?**
> - ✅ Light Search: search across repo metadata and README.
> - ✅ Local App: run the app locally for your own GitHub account.
>
> **What does not work?**
> - ❌ Deep Search: under optimization.
> - ❌ Global Hosted Version: in progress.
>
> Developed by **[@AbitathaRoy](https://github.com/AbitathaRoy)**

🔗 [View Release →](https://github.com/AbitathaRoy/GitHub-Smart-Search/releases/tag/v1.0.0-alpha)

---

## 🚧 Pending / Next Steps

### For Local:

- [ ] Re-introduce caching once the embedding bug is fixed
- [ ] Better file chunking for large repos (possibly by file type or folder)
- [ ] Add a summary or preview in search results
- [ ] Improve error handling in file embedding stage

### For Hosting:

- [ ] Ensure Deep Search works with cloud-hosted embeddings
- [ ] Add retry or delay logic for streamlit startup downloads
- [ ] Add download progress bar for JSONs
- [ ] Configure auto-run after release publish

---

## 🧾 Final README Elements (integrated)

Your README has been written and structured with:

- App intro and scope
- Latest release and link
- Feature matrix
- Step-by-step installation guide
- Credits and roadmap

---

## ✅ Final Checklist for Public Showcasing

| Item | Status |
|------|--------|
| `requirements.txt` accurate | ✅ Manually maintained |
| README complete | ✅ Generated |
| GitHub Release Live | ✅ Created and linked |
| Hosting Works | ⚠️ In alpha, pending deep search and load handling |
| Source repo cleaned up | ✅ No large files or secrets |
