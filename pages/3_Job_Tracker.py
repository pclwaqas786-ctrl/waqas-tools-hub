"""Page 3 — Job Tracker. JSON-backed application log + CV-tailoring checklist."""
import sys
from datetime import date
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.job_tracker import (  # noqa: E402
    STATUSES, CV_TAILORING_CHECKLIST, add_application, delete_application,
    load_applications, update_status,
)

st.set_page_config(page_title="Job Tracker", page_icon="💼", layout="centered")
st.title("💼 Job Tracker")
st.caption("Log every application. Tailor the CV per posting — never send one generic CV.")

with st.expander("➕ Add application", expanded=False):
    with st.form("add_app"):
        company = st.text_input("Company *")
        role = st.text_input("Role *")
        c1, c2 = st.columns(2)
        applied = c1.date_input("Date applied", value=date.today())
        status = c2.selectbox("Status", STATUSES)
        cv_version = st.text_input("CV version", placeholder="e.g. v3-lucky-cement")
        notes = st.text_area("Notes", height=80,
                             placeholder="HR email, portal link, referral...")
        submitted = st.form_submit_button("Save application", type="primary")
    if submitted:
        try:
            add_application(company, role, applied.isoformat(), status,
                            cv_version, notes)
            st.success(f"Saved: {company} — {role}")
            st.rerun()
        except ValueError as e:
            st.error(str(e))

apps = load_applications()
st.subheader(f"Applications ({len(apps)})")
if not apps:
    st.info("No applications yet. Add your first one above.")
else:
    st.dataframe(
        [{"Company": a["company"], "Role": a["role"], "Date": a["applied_date"],
          "Status": a["status"], "CV": a["cv_version"]} for a in
         sorted(apps, key=lambda x: x["applied_date"], reverse=True)],
        hide_index=True, use_container_width=True)

    st.write("**Update / delete**")
    labels = {a["id"]: f"{a['company']} — {a['role']} ({a['applied_date']})"
              for a in apps}
    sel_id = st.selectbox("Select application",
                          options=list(labels.keys()),
                          format_func=lambda i: labels[i])
    u1, u2 = st.columns(2)
    cur = next(a["status"] for a in apps if a["id"] == sel_id)
    new_status = u1.selectbox("New status", STATUSES,
                              index=STATUSES.index(cur))
    if u1.button("Update status"):
        update_status(sel_id, new_status)
        st.success("Status updated.")
        st.rerun()
    if u2.button("🗑️ Delete", type="secondary"):
        delete_application(sel_id)
        st.success("Deleted.")
        st.rerun()

    sel = next(a for a in apps if a["id"] == sel_id)
    if sel["notes"]:
        st.caption(f"Notes: {sel['notes']}")

with st.expander("✅ CV-tailoring checklist (per posting)"):
    st.caption("Do this for every application before sending.")
    for i, item in enumerate(CV_TAILORING_CHECKLIST, 1):
        st.checkbox(f"{i}. {item}", key=f"cvcheck_{i}")

st.divider()
st.caption("Idea from MadsLorentzen/ai-job-search · Data stored locally in data/applications.json")
