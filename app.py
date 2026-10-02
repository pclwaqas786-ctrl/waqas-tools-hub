"""Waqas Tools Hub — phone-friendly front end for 9 open-source tools."""
import streamlit as st

st.set_page_config(page_title="Waqas Tools Hub", page_icon="🧰", layout="centered")

st.title("🧰 Waqas Tools Hub")
st.caption("9 open-source tools, one phone-friendly place. "
           "✅ = working page · 📖 = setup guide (tool needs its own environment).")

TOOLS = [
    ("pages/1_Slop_Cleaner.py", "🧹", "Slop Cleaner",
     "Paste AI-sounding English, get cleaner human English back. Real rules from no-ai-slop.",
     "working"),
    ("pages/2_SEO_Quick_Audit.py", "🔍", "SEO Quick Audit",
     "Paste a URL or HTML, get title/meta/headings/alt-text/keyword checks.",
     "working"),
    ("pages/3_Job_Tracker.py", "💼", "Job Tracker",
     "Log job applications, track status, CV-tailoring checklist per posting.",
     "working"),
    ("pages/4_Book_to_Skill_Lite.py", "📚", "Book to Skill Lite",
     "PDF → text → chapters → Markdown skill draft (heuristic draft, review needed).",
     "working"),
    ("pages/5_OmniRoute_Guide.py", "🌐", "OmniRoute",
     "Free AI gateway for coding agents. Needs Node.js — setup guide.",
     "guide"),
    ("pages/6_Open_Generative_AI_Guide.py", "🎨", "Open-Generative-AI",
     "400+ image/video models in one app. Needs GPU — laptop/server only.",
     "guide"),
    ("pages/7_Open_Notebook_Guide.py", "📓", "Open Notebook",
     "Private AI research assistant. Docker-based — setup guide.",
     "guide"),
    ("pages/8_Strix_Guide.py", "🛡️", "Strix",
     "Autonomous AI pentesting agents. Needs containers — setup guide.",
     "guide"),
    ("pages/9_ADHD_Style_Guide.py", "⚡", "ADHD Answer Style",
     "Not an app — an output-style skill. Its 5 core rules, ready to copy.",
     "guide"),
]

cols = st.columns(3)
for i, (page, icon, name, desc, kind) in enumerate(TOOLS):
    with cols[i % 3]:
        with st.container(border=True):
            badge = "✅ Working page" if kind == "working" else "📖 Setup guide"
            st.markdown(f"### {icon} {name}")
            st.caption(badge)
            st.write(desc)
            st.page_link(page, label=f"Open {name}", icon=icon)

st.divider()
st.caption("Built from MIT/Apache-2.0 repos cloned 3 Oct 2026 · "
           "Repos live at ~/workspace/github-repos-batch/ · "
           "Zero cost, zero signups on the working pages.")
