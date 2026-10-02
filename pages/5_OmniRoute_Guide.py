"""Page 5 — OmniRoute setup guide (not convertible to a Streamlit page)."""
import streamlit as st

st.set_page_config(page_title="OmniRoute Guide", page_icon="🌐", layout="centered")
st.title("🌐 OmniRoute")
st.caption("📖 Setup guide — this tool has its own dashboard and cannot run as a Streamlit page.")

st.write("**What it is:** a free, self-hosted AI gateway. One endpoint routes "
         "requests to 350+ AI providers with automatic fallback when a quota runs out. "
         "Built for **Claude Code / Codex / Cursor / Cline / Copilot** users — "
         "it serves coding agents, not browsers.")

st.write("**Where it actually runs:** on a machine with Node.js (your laptop or a "
         "server), not inside Streamlit. It is a Next.js app with its own dashboard.")

st.subheader("Setup steps")
st.code("""cd ~/workspace/github-repos-batch/OmniRoute
npm install          # installs deps, auto-generates .env from .env.example
npm run dev          # dev server at http://localhost:20128
# then point your coding agent at http://localhost:20128
""", language="bash")

st.subheader("Honest notes")
st.markdown("""
- The repo advertises ~1.62B free tokens/month across free tiers — that is the
  repo's own marketing claim and was **not independently verified**.
- Most free tiers still need **free API keys you create yourself** (2-minute
  signups: Groq, Mistral, etc.). Without keys the dashboard runs but models
  will not respond.
- If you do not use Claude Code / Cursor / Cline, there is no consumer for this
  gateway — it would sit idle.
""")

st.subheader("Links")
st.markdown("""
- Local copy: `~/workspace/github-repos-batch/OmniRoute/`
- GitHub: https://github.com/diegosouzapw/OmniRoute
- Docs: https://omniroute.online
""")
