"""Page 6 — Open-Generative-AI setup guide."""
import streamlit as st

st.set_page_config(page_title="Open-Generative-AI Guide", page_icon="🎨",
                   layout="centered")
st.title("🎨 Open-Generative-AI")
st.caption("📖 Setup guide — a desktop Electron app; cannot run as a Streamlit page.")

st.write("**What it is:** a self-hosted open-source app bundling **400+ image/video "
         "models** in one place — including lip-sync models useful for narration "
         "and video work.")

st.write("**Where it actually runs:** as a desktop app (Electron) on a machine with "
         "a real GPU — a laptop with NVIDIA graphics or a GPU server. "
         "It will **not** run usefully on a small CPU-only VM.")

st.subheader("Setup steps (on your GPU machine)")
st.code("""cd Open-Generative-AI
npm install
npm run electron:dev     # dev mode
# or build installers:
npm run electron:build:win    # Windows installer
npm run electron:build:linux  # Linux installer
""", language="bash")

st.subheader("Honest notes")
st.markdown("""
- 400+ models means large downloads — check disk space before pulling models.
- Lip-sync and video models are the heaviest; start with one image model to
  verify your GPU works.
- Relevant to the **AI Stories Hub** track (thumbnails, lip-synced narration)
  once you have GPU access.
""")

st.subheader("Links")
st.markdown("""
- Local copy: `~/workspace/github-repos-batch/Open-Generative-AI/`
- GitHub: https://github.com/Anil-matcha/Open-Generative-AI
""")
