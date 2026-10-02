"""Page 8 — Strix setup guide."""
import streamlit as st

st.set_page_config(page_title="Strix Guide", page_icon="🛡️", layout="centered")
st.title("🛡️ Strix")
st.caption("📖 Setup guide — autonomous pentest agents needing containers; cannot run as a Streamlit page.")

st.write("**What it is:** the open-source AI pentesting tool — **autonomous AI agents "
         "that attack your app like real hackers**, then produce proof-of-concept "
         "exploits plus fixes.")

st.write("**Where it actually runs:** in containers against a target app "
         "(the repo ships `containers/` and a `Makefile`). You point it at **your own "
         "apps** — never anyone else's.")

st.subheader("Setup steps")
st.code("""cd ~/workspace/github-repos-batch/strix
# read docs first: https://docs.strix.ai
make --help        # see available targets (repo uses a Makefile)
""", language="bash")

st.subheader("Honest notes")
st.markdown("""
- Only ever test **your own** apps (SchoolWeb, Invoice Builder, this hub).
  Testing other people's systems without permission is illegal.
- Needs container runtime + model API keys for the agents.
- Practical use: before sharing an app publicly, let Strix find the holes first.
- There is also a hosted option: https://app.strix.ai (their cloud).
""")

st.subheader("Links")
st.markdown("""
- Local copy: `~/workspace/github-repos-batch/strix/`
- GitHub: https://github.com/usestrix/strix
- Docs: https://docs.strix.ai
""")
