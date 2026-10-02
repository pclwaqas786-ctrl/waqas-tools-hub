"""Job Tracker — local JSON-backed application log inspired by
MadsLorentzen/ai-job-search (listings + resume tailoring + cover letters).

Applications are stored in data/applications.json next to the app.
On Streamlit Cloud the filesystem is ephemeral, so entries persist for the
session / container lifetime; locally they persist on disk.
"""
import json
from datetime import date, datetime
from pathlib import Path

STATUSES = ["Applied", "Screening", "Interview", "Offer", "Rejected", "On hold"]

REQUIRED = ("company", "role")


def default_data_path():
    return Path(__file__).resolve().parent.parent / "data" / "applications.json"


def load_applications(path=None):
    path = Path(path) if path else default_data_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _save(applications, path):
    path = Path(path) if path else default_data_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(applications, ensure_ascii=False, indent=2),
                    encoding="utf-8")


def add_application(company, role, applied_date=None, status="Applied",
                    cv_version="", notes="", path=None):
    """Validate and append one application. Returns the new entry dict."""
    company = (company or "").strip()
    role = (role or "").strip()
    if not company:
        raise ValueError("Company name is required.")
    if not role:
        raise ValueError("Role title is required.")
    if status not in STATUSES:
        raise ValueError(f"Status must be one of: {', '.join(STATUSES)}.")
    if applied_date is None:
        applied_date = date.today().isoformat()
    applications = load_applications(path)
    existing_ids = {a.get("id") for a in applications}
    new_id = int(datetime.now().timestamp() * 1000)
    while new_id in existing_ids:
        new_id += 1
    entry = {
        "id": new_id,
        "company": company,
        "role": role,
        "applied_date": str(applied_date),
        "status": status,
        "cv_version": (cv_version or "").strip(),
        "notes": (notes or "").strip(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    applications.append(entry)
    _save(applications, path)
    return entry


def update_status(app_id, status, path=None):
    if status not in STATUSES:
        raise ValueError(f"Status must be one of: {', '.join(STATUSES)}.")
    applications = load_applications(path)
    for a in applications:
        if a.get("id") == app_id:
            a["status"] = status
            _save(applications, path)
            return True
    return False


def delete_application(app_id, path=None):
    applications = load_applications(path)
    kept = [a for a in applications if a.get("id") != app_id]
    if len(kept) == len(applications):
        return False
    _save(kept, path)
    return True


# Static per-posting CV-tailoring checklist (from the ai-job-search idea:
# tailor the resume to each listing instead of sending one generic CV).
CV_TAILORING_CHECKLIST = [
    "Copy 5-8 keywords from the job ad into your CV's skills section (only skills you truly have).",
    "Rewrite the CV summary line to mirror the exact role title in the ad.",
    "Move the most relevant job/project to the top of experience.",
    "Quantify one achievement per role (numbers, %, Rs, kW, machines — real figures only).",
    "Match the ad's must-have tools (e.g. Siemens TIA, AB Studio 5000, VFDs) with your real versions.",
    "Save as a new CV version and note the version name in the tracker above.",
    "Write 3 lines for the cover note: why this company, why you fit, one proof.",
]
