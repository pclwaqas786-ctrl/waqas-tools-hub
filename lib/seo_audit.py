"""SEO Quick Audit — lightweight on-page checker inspired by every-app/open-seo.

Uses requests + stdlib html.parser only (no lxml). Accepts a URL (fetched live)
or pasted HTML. Reports facts + pass/warn/fail checks — no invented scores.
"""
import re
from collections import Counter
from html.parser import HTMLParser

import requests

STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "from", "have", "were",
    "will", "would", "there", "their", "what", "which", "when", "your",
    "about", "into", "over", "after", "also", "more", "than", "then",
    "them", "they", "been", "are", "was", "has", "had", "can", "all",
    "each", "other", "some", "such", "only", "its", "our", "out", "who",
    "get", "how", "her", "his", "she", "you", "not", "but", "are",
}

TITLE_MIN, TITLE_MAX = 30, 60
DESC_MIN, DESC_MAX = 120, 160


class _SEOParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts = []
        self.in_title = False
        self.in_skip = False  # script / style
        self.meta_desc = ""
        self.h1 = 0
        self.h2 = 0
        self.h3 = 0
        self.imgs = 0
        self.imgs_no_alt = 0
        self.links_internal = 0
        self.links_external = 0
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag in ("script", "style"):
            self.in_skip = True
        elif tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            if name in ("description", "og:description") and not self.meta_desc:
                self.meta_desc = (a.get("content") or "").strip()
        elif tag == "h1":
            self.h1 += 1
        elif tag == "h2":
            self.h2 += 1
        elif tag == "h3":
            self.h3 += 1
        elif tag == "img":
            self.imgs += 1
            if not (a.get("alt") or "").strip():
                self.imgs_no_alt += 1
        elif tag == "a":
            href = (a.get("href") or "").strip()
            if href.startswith("http"):
                self.links_external += 1
            elif href.startswith(("#", "/", "?")) or (
                    href and not href.startswith(("mailto:", "tel:", "javascript:"))):
                self.links_internal += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag in ("script", "style"):
            self.in_skip = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        elif not self.in_skip:
            self.text_parts.append(data)


def _top_keywords(text, n=10):
    words = re.findall(r"[a-zA-Z]{4,}", text.lower())
    words = [w for w in words if w not in STOPWORDS]
    total = len(words)
    top = Counter(words).most_common(n)
    return [
        {"word": w, "count": c,
         "density_pct": round(c / total * 100, 2) if total else 0.0}
        for w, c in top
    ], total


def audit_html(html, source="pasted HTML"):
    """Audit an HTML string. Returns a report dict."""
    p = _SEOParser()
    try:
        p.feed(html or "")
    except Exception:
        pass
    title = "".join(p.title_parts).strip()
    desc = p.meta_desc
    text = " ".join(p.text_parts)
    text = re.sub(r"\s+", " ", text).strip()
    keywords, word_count = _top_keywords(text)

    checks = []
    issues = []

    # title
    if not title:
        checks.append(("Title tag", "fail", "Missing <title> tag."))
        issues.append("Add a <title> tag — it is the single most important on-page element.")
    elif len(title) < TITLE_MIN or len(title) > TITLE_MAX:
        checks.append(("Title tag", "warn",
                       f"Present but {len(title)} chars (ideal {TITLE_MIN}-{TITLE_MAX})."))
        issues.append(f"Title is {len(title)} characters; aim for {TITLE_MIN}-{TITLE_MAX}.")
    else:
        checks.append(("Title tag", "pass", f"{len(title)} chars — good length."))

    # meta description
    if not desc:
        checks.append(("Meta description", "warn", "Missing meta description."))
        issues.append("Add a meta description — it controls the search snippet.")
    elif len(desc) < DESC_MIN or len(desc) > DESC_MAX:
        checks.append(("Meta description", "warn",
                       f"Present but {len(desc)} chars (ideal {DESC_MIN}-{DESC_MAX})."))
    else:
        checks.append(("Meta description", "pass", f"{len(desc)} chars — good length."))

    # headings
    if p.h1 == 0:
        checks.append(("H1 heading", "fail", "No <h1> found."))
        issues.append("Add exactly one <h1> describing the page topic.")
    elif p.h1 == 1:
        checks.append(("H1 heading", "pass", "Exactly one <h1>."))
    else:
        checks.append(("H1 heading", "warn", f"{p.h1} <h1> tags — use only one."))
        issues.append(f"Found {p.h1} <h1> tags; keep one and demote the rest to <h2>.")
    checks.append(("H2 / H3 headings", "pass" if p.h2 else "warn",
                       f"{p.h2} H2, {p.h3} H3."))

    # images
    if p.imgs == 0:
        checks.append(("Images", "pass", "No images on page."))
    elif p.imgs_no_alt:
        checks.append(("Image alt text", "warn",
                       f"{p.imgs_no_alt} of {p.imgs} images missing alt text."))
        issues.append(f"Add alt text to {p.imgs_no_alt} image(s) — helps SEO and accessibility.")
    else:
        checks.append(("Image alt text", "pass", f"All {p.imgs} images have alt text."))

    # content depth
    if word_count < 300:
        checks.append(("Content depth", "warn", f"Only ~{word_count} words of text."))
        issues.append("Thin content (~%d words). Substantive pages usually need 300+." % word_count)
    else:
        checks.append(("Content depth", "pass", f"~{word_count} words of text."))

    return {
        "source": source,
        "title": title,
        "title_length": len(title),
        "meta_description": desc,
        "meta_description_length": len(desc),
        "h1_count": p.h1,
        "h2_count": p.h2,
        "h3_count": p.h3,
        "images_total": p.imgs,
        "images_missing_alt": p.imgs_no_alt,
        "links_internal": p.links_internal,
        "links_external": p.links_external,
        "word_count": word_count,
        "top_keywords": keywords,
        "checks": checks,
        "issues": issues,
    }


def audit_url(url, timeout=15):
    """Fetch a URL and audit it. Returns report dict or {'error': ...}."""
    url = (url or "").strip()
    if not url:
        return {"error": "Please enter a URL."}
    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "https://" + url
    try:
        r = requests.get(url, timeout=timeout,
                         headers={"User-Agent": "WaqasToolsHub/1.0 SEO-check"})
        r.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Could not fetch the page: {e}"}
    ctype = r.headers.get("Content-Type", "")
    if "html" not in ctype.lower():
        return {"error": f"URL did not return HTML (Content-Type: {ctype})."}
    report = audit_html(r.text, source=url)
    report["http_status"] = r.status_code
    return report
