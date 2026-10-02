"""Page 7 — open-notebook setup guide."""
import streamlit as st

st.set_page_config(page_title="Open Notebook Guide", page_icon="📓",
                   layout="centered")
st.title("📓 Open Notebook")
st.caption("📖 Setup guide — a Docker-based app with its own UI; cannot run as a Streamlit page.")

st.write("**What it is:** turn PDFs, videos, websites and notes into a **private, "
         "local AI research assistant** — a self-hosted, open-source alternative "
         "to NotebookLM. Ask questions over your own documents.")

st.write("**Where it actually runs:** via **Docker** (Docker Desktop on your laptop, "
         "or Docker on a server). It has its own web UI — Streamlit cannot host it.")

st.subheader("Setup steps")
st.code("""# 1. Install Docker Desktop: https://www.docker.com/products/docker-desktop/
cd ~/workspace/github-repos-batch/open-notebook
cp .env.example .env   # then edit .env: add your model API key
docker compose up      # open the printed localhost URL
""", language="bash")
st.caption("Full options are in the repo's CONFIGURATION.md.")

st.subheader("Honest notes")
st.markdown("""
- Needs Docker **and** an AI model API key (it calls a model to answer over your docs).
- Best use here: **AI Stories Hub research** — drop source material for a video
  topic in, get grounded notes out.
- Heavier than the lite pages in this hub; set it up when you have a research
  backlog worth it.
""")

st.subheader("Links")
st.markdown("""
- Local copy: `~/workspace/github-repos-batch/open-notebook/`
- GitHub: https://github.com/lfnovo/open-notebook
""")
