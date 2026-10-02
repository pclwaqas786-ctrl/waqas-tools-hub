"""Page 1 — Slop Cleaner. Real rules from petergyang/no-ai-slop."""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.slop_cleaner import clean, detect  # noqa: E402

st.set_page_config(page_title="Slop Cleaner", page_icon="🧹", layout="centered")
st.title("🧹 Slop Cleaner")
st.caption("Paste AI-sounding English → get cleaner, more human English. "
           "Rules from the open-source **no-ai-slop** skill. "
           "Tricky cases are *flagged for you*, never silently rewritten.")

mode = st.radio("Mode", ["Clean my draft", "Detect only (no rewrite)"],
                horizontal=True)

sample = ("In today's fast-paced world, it's worth noting that our cutting-edge "
          "platform will leverage AI to streamline your workflow. It's not just "
          "fast, it's transformative. In conclusion, this is huge for the "
          "ever-evolving market.")
if st.button("Load sample slop text"):
    st.session_state["slop_in"] = sample

text = st.text_area("Your draft", key="slop_in", height=220,
                    placeholder="Paste outreach email, gig description, caption...")

if st.button("✨ Clean it", type="primary"):
    if not text.strip():
        st.warning("Paste some text first.")
        st.stop()
    if mode == "Detect only (no rewrite)":
        findings = detect(text)
        if not findings:
            st.success("No known AI-slop patterns detected.")
        else:
            st.write(f"**{len(findings)} pattern(s) found:**")
            for f in findings:
                with st.expander(f"{f['pattern']} — line {f['line_no']}"):
                    st.write(f"> {f['quote']}")
                    st.write(f"**Fix:** {f['fix']}")
    else:
        res = clean(text)
        st.subheader("Cleaned text")
        st.text_area("Result", res["cleaned"], height=220, key="slop_out")
        st.download_button("⬇️ Download cleaned text",
                           res["cleaned"].encode("utf-8"),
                           file_name="cleaned.txt")

        st.subheader(f"What changed ({len(res['changes'])})")
        if not res["changes"]:
            st.write("Nothing to fix — already clean.")
        for ch in res["changes"]:
            st.markdown(f"- **{ch['rule']}** — {ch['detail']}")

        if res["flags"]:
            st.subheader(f"Needs your judgment ({len(res['flags'])})")
            st.caption("These need a human call — flagged, not auto-fixed.")
            for f in res["flags"]:
                st.markdown(f"- **{f['pattern']}** (line {f['line_no']}): {f['fix']}  \n"
                            f"> {f['quote']}")

st.divider()
st.caption("Source: petergyang/no-ai-slop (MIT) · "
           "Heuristic edits — always re-read the result before publishing.")
