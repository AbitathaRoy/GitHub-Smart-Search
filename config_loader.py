# config_loader.py

import json

def config_loader():
    try:
        import streamlit as st
        return {
            "ACCESS_TOKEN": st.secrets["ACCESS_TOKEN"],
            "USERNAME": st.secrets["USERNAME"],
            "LOCAL_REPO_PATH": st.secrets["LOCAL_REPO_PATH"],
            "MODEL_NAME": st.secrets["MODEL_NAME"],
            "NUMBER_OF_MATCHES": st.secrets["NUMBER_OF_MATCHES"],
            "QUERY_MODEL_NAME": st.secrets["QUERY_MODEL_NAME"],
            "QUERY_FEW_SHOTS_PATH": st.secrets["QUERY_FEW_SHOTS_PATH"],
            "HF_API_KEY": st.secrets["HF_API_KEY"],
            "GEMINI_API_KEY": st.secrets["GEMINI_API_KEY"],
            "RELEASE_TAG": st.secrets["RELEASE_TAG"],
            "REPO_OWNER": st.secrets["REPO_OWNER"],
            "REPO_NAME": st.secrets["REPO_NAME"]
        }
    except Exception:
        with open("config_private.json", "r", encoding="utf-8") as f:
            return json.load(f)