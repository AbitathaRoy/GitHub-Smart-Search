# 🔍 GitHub Smart Search
A **semantic search engine** that understands natural language queries and returns the most relevant repositories from your **own GitHub account**, based on repository metadata and content.

Powered by `SentenceTransformer` embeddings and a lightweight Streamlit UI.

## Latest Version
**v1.0.0-alpha**
This is the **first public release** of GitHub Smart Search.
Check out the [Release Notes](https://github.com/AbitathaRoy/AI-GitHub-Indexer/releases/tag/v1.0.0-alpha%2B20250619) for details.

### ✅ What works?
- **Light Search –** Retrieve repositories based on queries using metadata from your GitHub account — including **repo name**, **description**, **URL**, and **README** content.
- **Local App Functionality –** You can **clone this repository**, configure it for your own GitHub account, and run smart searches by hosting it **locally**.

### ⚠️ What doesn't work (yet)?
- **Deep Search (In Progress) –** Intended to go beyond READMEs and analyze **file-level embeddings**. Currently under development and optimization.
- **Global/Hosted App –** A publicly-available hosted version (configured to my account 😁 and yours) is not yet stable and is undergoing debugging.

## Getting Started
### 1. Clone the Repository
```bash
git clone https://github.com/AbitathaRoy/GitHub-Smart-Search.git
cd GitHub-Smart-Search
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Set Up Configuration
Using the `config_template.json` file provided, create a `config_private.json` file, or use `.streamlit/secrets.toml` for hosted environments (currently under development). Some of the default fields are provided below:
```json
{
  "MODEL_NAME": "sentence-transformers/all-MiniLM-L6-v2",
  "NUMBER_OF_MATCHES": 5,
  "QUERY_FEW_SHOTS_PATH": "query_few_shot_examples.json"
}
```
- For `ACCESS_TOKEN`, generate your own GitHub account access token.
- For `USERNAME`, assign your own GitHub username.
- `LOCAL_REPO_PATH` is where you clone this repo in your device.
- For `GEMINI_API_KEY`, generate your own Google Gemini API key from a Google Cloud free tier. In case you want to use some other API, the file `google_genai.py` which contains the query processing logic will have to be modified accordingly.

The rest of the keys MAY be kept un-configured for the current version of the application.
### 4. Initialize your Required Data Files
After completing your configuration file with your data and keys, run the `extract_github_repo_data.py` to collect data from your GitHub account. It will generate two files— `repo_data.json` (for light search) and `files_data.json` (for deep search).
```bash
python3 extract_github_repo_data.py
```
Run the file `encoder_without_caching.py` to embed your data and create their subsequent output files.
**Note:** As of this version of this application, to keep things cool and swift, DO NOT embed your `files_data`. For that, in `encoder_without_caching.py`, ensure that the lists `INPUT_FILE` and `OUTPUT_FILE` contain the filenames `repo_data.json` and `repo_data_with_embeddings.json` ONLY.
```bash
python3 encoder_without_caching.py
```
### Run the Application
```bash
streamlit run streamlit_search_app_2.py
```
## How It Works
- Your GitHub repos are cloned and parsed.
- Metadata (repo name, description, README) and optionally individual files are embedded.
- The embeddings are stored in JSON and searched using cosine similarity.
- You enter a query → it's embedded → top N results are shown.

## Credits
Built with [Streamlit](https://github.com/streamlit), [Sentence Transformers](https://github.com/UKPLab/sentence-transformers), and a lot of 💕 by [Abitatha Roy](https://linkedin.com/in/abitatha).
You may also reach me out through [e-mail](mailto:abitatharoy@cic.du.ac.in).
