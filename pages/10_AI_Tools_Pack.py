"""Page 10 — AI Tools Pack: 5 verified free tools (from Technical Ameen's post,
checked 20 Oct 2026). A curated guide page — these tools run on your own
machine, not inside Streamlit."""
import streamlit as st

st.set_page_config(page_title="AI Tools Pack", page_icon="🧰", layout="centered")
st.title("🧰 AI Tools Pack — 5 Verified Free Tools")
st.caption("📖 Curated guide — links and install commands in one place. "
           "All 5 links verified 20 Oct 2026.")

# 1 ---------------------------------------------------------------------
st.header("1. SuperLocalMemory")
st.caption("FREE · repo cloned locally")
st.write("**What it is:** one **shared memory** for all your AI tools — Claude, "
         "Codex, Cursor, ChatGPT — stored on your own computer (local-first, "
         "no cloud). Tell one tool something, the others remember it.")
st.write("**Your use:** you work across multiple accounts/tools — this saves "
         "re-explaining context to every AI, every time.")
st.code("npm install -g superlocalmemory\nslm setup", language="bash")
st.markdown("- Website: https://superlocalmemory.com\n"
            "- GitHub: https://github.com/qualixar/superlocalmemory")

st.divider()

# 2 ---------------------------------------------------------------------
st.header("2. Pomerado")
st.caption("FREE / Open-source · repo cloned locally")
st.write("**What it is:** turns any website into an **API or MCP tool** in "
         "minutes. For sites with no API of their own (old portals, booking "
         "sites), an AI agent can then work on them. Y Combinator (F2026).")
st.write("**Your use:** automation work — any site where you currently type "
         "data in by hand can be handed to an agent.")
st.markdown("- Website: https://pomerado.ai\n"
            "- GitHub: https://github.com/Pomerado")

st.divider()

# 3 ---------------------------------------------------------------------
st.header("3. BOSS Console")
st.caption("FREE / Open-source · repo cloned locally")
st.write("**What it is:** one workspace to run all your AI agents (Claude "
         "Code, Codex, Gemini) — browser, terminal and editor in one place, "
         "agents stay \"on\" and you can watch them.")
st.write("**Your use:** heavy for now — ready for when you need several "
         "agents running side by side. Skipping it for now is fine.")
st.markdown("- Website: https://bossconsole.ai\n"
            "- GitHub: https://github.com/risa-labs-inc/BossConsole")

st.divider()

# 4 ---------------------------------------------------------------------
st.header("4. Skisso")
st.caption("FREE Chrome Extension")
st.write("**What it is:** point at an element on your live website, change "
         "its colour/size/layout visually — and your coding agent (Claude "
         "Code/Codex) gets a ready-made exact patch. No explaining in "
         "paragraphs.")
st.write("**Your use:** small design changes on white-label sites (SchoolWeb, "
         "Kiryana Pro, DrawSew site) — point at the client's site, the agent "
         "applies the code change.")
st.code("npx skisso   # MCP route — or install the Chrome extension",
        language="bash")
st.markdown("- Product Hunt: "
            "https://www.producthunt.com/products/skisso-design-on-the-live-product")

st.divider()

# 5 ---------------------------------------------------------------------
st.header("5. Grablo Spot")
st.caption("FREE")
st.write("**What it is:** **free AI CCTV software** that works with your "
         "existing cameras. Type a face, clothing, vehicle or number plate "
         "and find the person in seconds across hours of footage. Footage "
         "stays on your own computer, never goes to the cloud. (Only the "
         "remote-viewing relay is paid, past 1GB/month.)")
st.write("**Your use (the money one):** offer kiryana/medical/mobile-shop "
         "clients an \"AI CCTV search\" **setup service** — the software is "
         "free, the fee is for your work.")
st.markdown("- Website / Download: https://grablo.co")

st.divider()
st.caption("Repos for tools 1–3 live at ~/workspace/tools/ · "
           "Say the word when you're at your laptop — install help, step by step.")
