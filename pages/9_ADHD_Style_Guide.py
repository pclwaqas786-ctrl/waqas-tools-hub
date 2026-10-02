"""Page 9 — i-have-adhd: not an app, an output-style skill. Show the 5 core rules."""
import streamlit as st

st.set_page_config(page_title="ADHD Answer Style", page_icon="⚡", layout="centered")
st.title("⚡ ADHD Answer Style")
st.caption("📖 Not an app — an **output-style skill** for coding assistants. "
           "Its 5 core rules, ready to copy into any AI chat.")

st.write("From **ayghri/i-have-adhd** (MIT). The idea: shape answers so a busy "
         "brain can *act* on them — lead with the next action, number the steps, "
         "one concrete next move at the end. The skill has 10 rules total; "
         "these 5 are the core.")

RULES = [
    ("1. Lead with the next action",
     "The first line is something the reader can do. Not context. Not a plan.\n\n"
     "Bad: \"Let's think about this. Your auth flow has a few moving pieces...\"\n"
     "Good: \"Run `npm install jsonwebtoken`, then edit `src/auth.ts:42`.\""),
    ("2. Number multi-step tasks",
     "Each step is one bounded action. Fewest steps that still work.\n\n"
     "Bad: \"First open the file, find the function, swap it out, then run the tests.\"\n"
     "Good:\n1. Open `src/auth.ts`\n2. Replace `verifyToken` (lines 42–58) with the snippet below\n"
     "3. Run `npm test -- auth.spec.ts`"),
    ("3. End with one concrete next action",
     "If anything is left open, name ONE thing doable in under two minutes.\n\n"
     "Bad: \"Hope that helps. Let me know if you want to dig deeper.\"\n"
     "Good: \"Next: run `npm test` and paste the first failing line.\""),
    ("4. Suppress tangents",
     "Finish the first issue, then offer the second as a separate question.\n\n"
     "Bad: \"Here's the fix. By the way, your dependency is also stale, and your README...\"\n"
     "Good: \"Here's the fix. Separately: there is also a stale dependency. "
     "Want me to handle that next?\""),
    ("5. Restate state every turn",
     "The reader cannot hold \"step 3 of 5\" between messages. Restate it.\n\n"
     "Bad: \"Done. Ready for the next part?\"\n"
     "Good: \"Step 3 of 5 done: schema updated. Next: backfill the new column.\""),
]

for title, body in RULES:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.write(body)

st.subheader("Copy-paste prompt")
st.code("Answer in ADHD mode: lead with the next action, number multi-step work, "
        "end with one concrete next action, no tangents, restate state.",
        language="text")

st.subheader("Links")
st.markdown("""
- Local copy: `~/workspace/github-repos-batch/i-have-adhd/`
- GitHub: https://github.com/ayghri/i-have-adhd
- Full skill (10 rules): `skills/i-have-adhd/SKILL.md` in the repo
""")
