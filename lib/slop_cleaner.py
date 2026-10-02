"""Slop Cleaner — pure-Python implementation of the editing rules from
petergyang/no-ai-slop (skills/no-ai-slop/SKILL.md).

Two jobs, mirroring the skill:
  clean(text)  -> edited draft + "What changed" list
  detect(text) -> flagged patterns with line quotes and short fixes (no rewrite)

Only mechanical, verifiable rules are applied automatically. Anything needing
judgment (weasel attribution, puffery rewrites, colon reveals) is flagged,
never silently rewritten.
"""
import re

# ---------------------------------------------------------------------------
# Rule 1: banned words — replaced with a plain equivalent
# ---------------------------------------------------------------------------
BANNED_WORDS = {
    "delve": "explore",
    "foster": "build",
    "leverage": "use",
    "utilize": "use",
    "facilitate": "help",
    "empower": "enable",
    "streamline": "simplify",
    "robust": "solid",
    "cutting-edge": "latest",
    "paradigm shift": "big change",
    "game changer": "big improvement",
    "tapestry": "mix",
    "realm": "field",
    "beacon": "example",
    "multifaceted": "varied",
    "meticulous": "careful",
    "intricate": "complex",
    "paramount": "key",
    "transformative": "major",
    "elevate": "raise",
    "embark": "start",
    "supercharge": "boost",
    "harness": "use",
    "ever-evolving": "fast-changing",
    "this is huge": "",
    "this changes everything": "",
}

# ---------------------------------------------------------------------------
# Rule 2: often-empty adverbs — removed (listed in "What changed")
# ---------------------------------------------------------------------------
EMPTY_ADVERBS = [
    "just", "literally", "honestly", "simply", "actually", "truly",
    "fundamentally", "importantly", "crucially", "inherently", "inevitably",
]

# ---------------------------------------------------------------------------
# Rule 3: often-empty phrases / throat-clearing openers / faux-insight setups
# (regex, replacement)
# ---------------------------------------------------------------------------
PHRASE_RULES = [
    (r"\bit['\u2019]s worth noting that\b", ""),
    (r"\bit['\u2019]s important to note that\b", ""),
    (r"\bat the end of the day,?", ""),
    (r"\bwhen it comes to\b", "for"),
    (r"\bat its core,?", ""),
    (r"\bin today['\u2019]s world,?", "today,"),
    (r"\bin the age of\b", "today in"),
    (r"\bin the world of\b", "in"),
    (r"\bthe reality is that\b", ""),
    (r"\bthe truth is that\b", ""),
    (r"\bin terms of\b", "for"),
    (r"\bwith regard to\b", "about"),
    (r"\bin order to\b", "to"),
    (r"\bgoing forward,?", ""),
    (r"\bin this article,?", ""),
    (r"\blet['\u2019]s dive in\.?", ""),
    # throat-clearing openers
    (r"\bhere['\u2019]s the thing,?", ""),
    (r"\bhere['\u2019]s what i mean,?", ""),
    (r"\blet me be clear,?", ""),
    (r"\bi['\u2019]ll be honest,?", ""),
    (r"\bthe uncomfortable truth is(,| that)?", ""),
    # faux-insight setups
    (r"\bthis is the part most people skip:?", ""),
    (r"\bwhat most people get wrong:?", ""),
    (r"\bhere['\u2019]s what nobody tells you:?", ""),
    (r"\bthe part everyone misses:?", ""),
    # redundant metadiscourse / recap endings
    (r"\bin other words,?", ""),
    (r"\bin conclusion,?", ""),
]

# Sentence-initial recap words
RECAP_OPENERS = re.compile(r"(^|[.!?]\s+)(ultimately|overall),\s+", re.IGNORECASE)

# ---------------------------------------------------------------------------
# Rule 4: binary contrasts — simple mechanical cases only
# ---------------------------------------------------------------------------
def _fix_not_just(text, changes):
    # "It's not just X, it's Y." / "It's not just X but Y." -> "Y."
    def repl(m):
        y = m.group(2).strip().rstrip(".")
        y = y[0].upper() + y[1:] if y else y
        changes.append({
            "rule": "Binary contrast",
            "detail": f"Cut the 'not just X' setup; kept the point: \"{y}.\"",
        })
        return y + "."
    return re.sub(
        r"\bit['\u2019]s not just (.+?),?\s+(?:but |it['\u2019]s )([^.]+)\.",
        repl, text, flags=re.IGNORECASE)

def _fix_this_is_not(text, changes):
    # "This is not X. It's Y." -> "It's Y."
    def repl(m):
        y = m.group(2).strip().rstrip(".")
        changes.append({
            "rule": "Binary contrast",
            "detail": f"Cut the 'This is not X' setup; kept: \"It's {y}.\"",
        })
        return f"It's {y}."
    return re.sub(
        r"\bthis is not ([^.]+)\.\s+it['\u2019]s ([^.]+)\.",
        repl, text, flags=re.IGNORECASE)

# ---------------------------------------------------------------------------
# Rule 5: em-dash cleanup — spaced em/en dashes become commas
# ---------------------------------------------------------------------------
EMDASH_RE = re.compile(r"\s+[\u2014\u2013]\s+")

# ---------------------------------------------------------------------------
# Detect-only patterns: flagged with a short fix, never rewritten
# ---------------------------------------------------------------------------
DETECT_PATTERNS = [
    (re.compile(r"\b(experts agree|industry reports suggest|many argue|"
                r"widely regarded as|studies show)\b", re.IGNORECASE),
     "Weasel attribution", "Name the source or cut the claim."),
    (re.compile(r"\b(stands as a testament to|marks a pivotal moment for|"
                r"plays a vital role in|solidifies its position as|"
                r"underscores its significance)\b", re.IGNORECASE),
     "Importance puffery", "State the fact; let the reader judge whether it matters."),
    (re.compile(r"^[^:\n]{2,70}:\s+[a-z]", re.MULTILINE),
     "Colon reveal", "Rewrite as a plain sentence instead of a dramatic reveal."),
    (re.compile(r"\bthe question isn['\u2019]t\b", re.IGNORECASE),
     "Binary contrast", "State the point directly instead of the X-vs-Y setup."),
    (re.compile(r",\s+(highlighting|underscoring|reflecting|showcasing)\b",
                re.IGNORECASE),
     "Superficial analysis", "Replace the trailing -ing clause with the concrete effect."),
    (re.compile(r"\b(what if i told you|think about it:|plot twist:)\b",
                re.IGNORECASE),
     "Rhetorical setup", "Drop the setup and make the point."),
]


def _tidy(text):
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # fix double spaces left at sentence starts after removals
    text = re.sub(r"([.!?])\s+([a-z])",
                  lambda m: m.group(1) + " " + m.group(2).upper(), text)
    return text.strip()


def clean(text):
    """Edit a draft. Returns dict with 'cleaned', 'changes', 'flags'."""
    if not text or not text.strip():
        return {"cleaned": "", "changes": [], "flags": []}
    changes = []
    out = text

    # 1. banned words
    for word, plain in BANNED_WORDS.items():
        pat = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
        hits = pat.findall(out)
        if hits:
            def _rep(m, p=plain):
                w = m.group(0)
                if not p:
                    return ""
                if w[0].isupper():
                    return p[0].upper() + p[1:]
                return p
            out = pat.sub(_rep, out)
            changes.append({
                "rule": "Banned word",
                "detail": f"Replaced {len(hits)}x \"{word}\""
                          + (f" with \"{plain}\"" if plain else " (removed hype)")
                          + ".",
            })

    # 2. empty adverbs
    for adv in EMPTY_ADVERBS:
        pat = re.compile(r"\b" + adv + r"\b[,.]?", re.IGNORECASE)
        hits = pat.findall(out)
        if hits:
            out = pat.sub("", out)
            changes.append({
                "rule": "Empty adverb",
                "detail": f"Removed {len(hits)}x \"{adv}\" (added nothing).",
            })

    # 3. empty phrases / openers / setups
    for pattern, replacement in PHRASE_RULES:
        pat = re.compile(pattern, re.IGNORECASE)
        hits = pat.findall(out)
        if hits:
            out = pat.sub(replacement, out)
            label = ("Throat-clearing opener" if "here's the thing" in pattern
                     or "let me be clear" in pattern or "i'll be honest" in pattern
                     else "Faux-insight setup" if "most people" in pattern
                     or "nobody tells you" in pattern or "everyone misses" in pattern
                     else "Empty phrase")
            changes.append({
                "rule": label,
                "detail": f"Removed {len(hits)}x filler matching /{pattern[:40]}.../.",
            })

    # sentence-initial recap words
    recap_hits = RECAP_OPENERS.findall(out)
    if recap_hits:
        out = RECAP_OPENERS.sub(r"\1", out)
        changes.append({
            "rule": "Summary-recap ending",
            "detail": f"Removed {len(recap_hits)}x sentence-initial recap word.",
        })

    # 4. binary contrasts (mechanical cases)
    out = _fix_not_just(out, changes)
    out = _fix_this_is_not(out, changes)

    # 5. em dashes
    dash_hits = EMDASH_RE.findall(out)
    if dash_hits:
        out = EMDASH_RE.sub(", ", out)
        changes.append({
            "rule": "Em-dash cleanup",
            "detail": f"Replaced {len(dash_hits)}x decorative em/en dash with a comma.",
        })

    out = _tidy(out)

    # flags for anything needing human judgment
    flags = detect(out)
    return {"cleaned": out, "changes": changes, "flags": flags}


def detect(text):
    """Flag AI-slop patterns without rewriting. Returns list of findings."""
    findings = []
    if not text or not text.strip():
        return findings
    lines = text.splitlines()
    for pat, name, fix in DETECT_PATTERNS:
        for m in pat.finditer(text):
            lineno = text.count("\n", 0, m.start()) + 1
            line = lines[lineno - 1].strip() if lineno <= len(lines) else ""
            if len(line) > 120:
                line = line[:117] + "..."
            findings.append({
                "pattern": name,
                "line_no": lineno,
                "quote": line,
                "fix": fix,
            })
    return findings
