#!/usr/bin/env python3
"""Convert the QuietSkies Privacy/Terms markdown into styled site pages.

Run from the apaisant-site folder:  python build_docs.py
Re-run whenever the source .md files change. It strips the internal
"draft / not legal advice" banner (that was a note to us, not the public) and
tidies the "Last updated" line.
"""
import html
import re
from pathlib import Path

SRC = Path(r"E:/Development/1-Projects/Project QuietSkies")
SITE = Path(__file__).resolve().parent

DOCS = [
    ("Privacy_Policy.md", "quietskies/privacy/index.html", "QuietSkies Privacy Policy"),
    ("Terms_of_Use.md", "quietskies/terms/index.html", "QuietSkies Terms of Use"),
]

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="theme-color" content="#5b7360" />
  <link rel="icon" href="/assets/favicon-32.png" sizes="32x32" />
  <link rel="stylesheet" href="/css/style.css" />
</head>
<body>
  <header class="site-head">
    <a class="brand" href="/" aria-label="Apaisant home"><img src="/assets/apaisant-logo.png" alt="Apaisant" /></a>
    <nav><a href="/quietskies/">QuietSkies</a></nav>
  </header>
  <main class="doc">
    <a class="back" href="/quietskies/">← Back to QuietSkies</a>
    <h1>{h1}</h1>
    <p class="updated">{updated}</p>
{body}
  </main>
  <footer class="site-foot">
    <div class="foot-inner">
      <a class="foot-brand" href="/" aria-label="Apaisant home"><img src="/assets/apaisant-logo.png" alt="Apaisant" /></a>
      <div class="foot-links">
        <a href="/quietskies/">QuietSkies</a>
        <a href="/quietskies/privacy/">Privacy</a>
        <a href="/quietskies/terms/">Terms</a>
        <a href="mailto:apaisant.github.precise709@passmail.com">Contact</a>
      </div>
      <p class="foot-note">© 2026 Apaisant. Made in Australia.</p>
    </div>
  </footer>
</body>
</html>
"""


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


def convert(md):
    lines = md.split("\n")
    h1, updated = "", ""
    out, para, ul = [], [], []

    def flush_para():
        if para:
            out.append("    <p>" + " ".join(para) + "</p>")
            para.clear()

    def flush_ul():
        if ul:
            out.append("    <ul>")
            out.extend("      <li>" + li + "</li>" for li in ul)
            out.append("    </ul>")
            ul.clear()

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("# "):
            h1 = line[2:].strip()
            continue
        if "Draft for review" in line:  # internal banner — drop from public page
            continue
        if line.lower().startswith("last updated"):
            updated = re.sub(r"\s*\(draft\)\s*", "", line).strip()
            continue
        if not line.strip():
            flush_para(); flush_ul(); continue
        if line.startswith("## "):
            flush_para(); flush_ul(); out.append("    <h2>" + inline(line[3:].strip()) + "</h2>"); continue
        if line.startswith("### "):
            flush_para(); flush_ul(); out.append("    <h3>" + inline(line[4:].strip()) + "</h3>"); continue
        if line.strip() == "---":
            flush_para(); flush_ul(); out.append("    <hr />"); continue
        if line.lstrip().startswith("- "):
            flush_para(); ul.append(inline(line.lstrip()[2:].strip())); continue
        flush_ul(); para.append(inline(line.strip()))

    flush_para(); flush_ul()
    return h1, (updated or "Last updated: 8 August 2026"), "\n".join(out)


for src_name, dest_rel, title in DOCS:
    md = (SRC / src_name).read_text(encoding="utf-8")
    h1, updated, body = convert(md)
    dest = SITE / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(PAGE.format(title=title, h1=html.escape(h1), updated=html.escape(updated), body=body), encoding="utf-8")
    print("wrote", dest_rel, "-", h1)
