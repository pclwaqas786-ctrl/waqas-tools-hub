"""Page 2 — SEO Quick Audit. requests + stdlib html.parser only."""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.seo_audit import audit_html, audit_url  # noqa: E402

st.set_page_config(page_title="SEO Quick Audit", page_icon="🔍", layout="centered")
st.title("🔍 SEO Quick Audit")
st.caption("On-page checks inspired by the open-source **open-seo** project. "
           "Facts only — no invented scores.")

tab_url, tab_html = st.tabs(["Audit a URL", "Paste HTML"])

report = None
with tab_url:
    url = st.text_input("Page URL", placeholder="https://example.com/page")
    if st.button("Audit URL", type="primary"):
        with st.spinner("Fetching page..."):
            report = audit_url(url)
with tab_html:
    html = st.text_area("HTML source", height=200, placeholder="Paste full page HTML...")
    if st.button("Audit HTML", type="primary"):
        report = audit_html(html)

if report:
    if "error" in report:
        st.error(report["error"])
        st.stop()
    st.subheader(f"Report: {report['source']}")
    if report.get("http_status"):
        st.caption(f"HTTP {report['http_status']}")

    st.write("**Checks**")
    for label, status, detail in report["checks"]:
        icon = {"pass": "✅", "warn": "⚠️", "fail": "❌"}.get(status, "•")
        st.markdown(f"{icon} **{label}** — {detail}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Words", f"~{report['word_count']}")
    c2.metric("Images missing alt", report["images_missing_alt"])
    c3.metric("Links in/out", f"{report['links_internal']}/{report['links_external']}")

    with st.expander("Title & meta description"):
        st.write("**Title:**", report["title"] or "_missing_")
        st.write("**Meta description:**", report["meta_description"] or "_missing_")

    st.write("**Top keywords (4+ letters)**")
    kw = report["top_keywords"]
    if kw:
        st.dataframe([{"keyword": k["word"], "count": k["count"],
                       "density %": k["density_pct"]} for k in kw],
                     hide_index=True, use_container_width=True)
    else:
        st.write("No keywords found.")

    if report["issues"]:
        st.subheader("Suggested fixes")
        for issue in report["issues"]:
            st.markdown(f"- {issue}")
    else:
        st.success("No issues found.")

st.divider()
st.caption("Source idea: every-app/open-seo (open-source Semrush/Ahrefs alternative) · "
           "This page is a lite audit, not the full tool.")
