# 🧰 Waqas Tools Hub

Phone-friendly web front end for 9 open-source tools (MIT/Apache-2.0), cloned 3 Oct 2026.

**Honest scope:** 4 pages genuinely work in pure Python. 5 tools cannot run as
Streamlit pages (they need Node.js / Docker / GPU / containers, or are not apps
at all) — those get honest setup-guide pages instead of fake buttons.

## Working pages (✅)

| Page | What it does | Source repo |
|---|---|---|
| 🧹 Slop Cleaner | Paste AI-sounding English → cleaner human English, with a "What changed" list. Real regex rules from the skill. | petergyang/no-ai-slop |
| 🔍 SEO Quick Audit | URL or pasted HTML → title/meta/headings/alt-text/keyword-density checks. | every-app/open-seo (lite) |
| 💼 Job Tracker | Log applications in local JSON, track status, per-posting CV-tailoring checklist. | MadsLorentzen/ai-job-search (lite) |
| 📚 Book to Skill Lite | PDF → chapters → Markdown skill **draft** (heuristic, needs human review). | virgiliojr94/book-to-skill (lite) |

## Setup-guide pages (📖)

OmniRoute · Open-Generative-AI · open-notebook · Strix · ADHD Answer Style —
what each is, where it actually runs, setup steps, local path + GitHub link.

## Run locally

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud (free)

1. Push this folder to GitHub (repo `waqas-tools-hub`).
2. Go to https://share.streamlit.io → **New app**.
3. Pick the repo, branch `main`, main file path `app.py` → **Deploy**.
4. Done — you get a public `*.streamlit.app` URL. `requirements.txt` is installed automatically.

Notes:
- Job Tracker data lives in `data/applications.json` (git-ignored). On Streamlit
  Cloud the filesystem is ephemeral — entries persist for the container lifetime.
- No API keys, no signups, no cost on any working page.

## Source repos (local clones)

`~/workspace/github-repos-batch/` — see its `README.txt`.
