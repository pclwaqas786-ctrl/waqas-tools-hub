"""Page 4 — Book to Skill Lite. PDF -> chapters -> Markdown draft (heuristic)."""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.book_skill import build_markdown_draft, extract_pdf_text  # noqa: E402

st.set_page_config(page_title="Book to Skill Lite", page_icon="📚",
                   layout="centered")
st.title("📚 Book to Skill Lite")
st.warning("**Honest label:** this produces a *heuristic draft* (word-frequency, "
           "heading patterns) — NOT LLM-quality extraction. "
           "A human must review and rewrite it before it becomes a skill.",
           icon="⚠️")
st.caption("Lite take on virgiliojr94/book-to-skill: turn a technical book PDF "
           "into a structured starting draft.")

uploaded = st.file_uploader("Upload a PDF book/manual", type=["pdf"])

if uploaded and st.button("📖 Build draft", type="primary"):
    try:
        with st.spinner("Extracting text..."):
            text, pages, truncated = extract_pdf_text(uploaded)
        with st.spinner("Splitting chapters & finding key terms..."):
            md, n_chapters = build_markdown_draft(uploaded.name, text, pages,
                                                  truncated)
        st.success(f"Draft ready: {pages} pages → {n_chapters} chapters "
                   f"({'truncated at 400k chars' if truncated else 'full text'}).")
        st.download_button("⬇️ Download Markdown draft",
                           md.encode("utf-8"),
                           file_name=uploaded.name.rsplit(".", 1)[0] + "-skill-draft.md")
        st.markdown("---")
        st.markdown(md)
    except ValueError as e:
        st.error(str(e))
    except Exception as e:  # noqa: BLE001 - never crash the page
        st.error(f"Something went wrong reading the PDF: {e}")

st.divider()
st.caption("Source idea: virgiliojr94/book-to-skill · "
           "The real tool uses AI agents per chapter; this page is a lite draft-maker.")
