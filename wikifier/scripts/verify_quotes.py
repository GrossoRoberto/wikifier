#!/usr/bin/env python3
"""Mechanical quote check for wikifier citations (stdlib only, read-only).

Usage: python verify_quotes.py <wiki_root> [page.md ...]
  No pages given -> every *.md under <wiki_root>/wiki/ (trash/ excluded).

Citation format checked (one per footnote definition, see references/structure-v21.md):
  [^n]: raw/<folder>/<file> — "<verbatim quote>" (<locator>)
  [^n]: [synthesis] <paths> — explanation          (skipped, needs judgment)

Sources may be under raw/ or be a chat extract directly inside _wikifier/ (YYYY-MM-DD_chat-<topic>.md);
anything else (including saved plans and reports in _wikifier/) is OUTSIDE_ROOT.
A quote is OK only if, after collapsing whitespace runs to one space and NFC
normalisation, it occurs as an exact (case-sensitive) substring of the raw file.
This proves the text EXISTS in the source. It does NOT prove the page's claim is
supported by it: that is a judgment step (references/cmd-audit.md).

Output: one line per citation  <STATUS>\t<page>\t[^id]\t<detail>
Optional line locator: if the parenthesised locator contains L<n> or L<a>-<b> (1-based lines of the
raw file, split on newlines), the quote must occur inside those lines, else WRONG_LINES.
Locators without an L-token (e.g. "section 2") are not checked.

Statuses: OK NOT_FOUND WRONG_LINES FILE_MISSING UNSUPPORTED_TYPE MALFORMED OUTSIDE_ROOT
          SYNTHESIS_SKIPPED ORPHAN_REF UNUSED_DEF
Exit code 0 only if no line is NOT_FOUND/WRONG_LINES/FILE_MISSING/UNSUPPORTED_TYPE/MALFORMED/OUTSIDE_ROOT/ORPHAN_REF.
"""
import re, sys, unicodedata, pathlib

TEXT_EXT = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".html", ".htm", ".xml", ".log", ".tsv"}
DEF = re.compile(r"^\[\^([^\]]+)\]:\s*(.*)$")
QUOTE = re.compile(r'^(?P<path>.+?)\s+—\s+"(?P<q>.+)"\s*(?:\((?P<loc>[^()]*)\))?\s*$')
REF = re.compile(r"\[\^([^\]]+)\](?!:)")
CHAT_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}_chat-.+\.md$")
LINES = re.compile(r"(?<![A-Za-z0-9])L(\d+)(?:\s*-\s*L?(\d+))?(?![A-Za-z0-9])")
BAD = {"NOT_FOUND", "WRONG_LINES", "FILE_MISSING", "UNSUPPORTED_TYPE", "MALFORMED", "OUTSIDE_ROOT", "ORPHAN_REF"}

def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip()

def check_page(root, page):
    out = []
    rel = page.relative_to(root).as_posix()
    text = page.read_text(encoding="utf-8")
    lines = text.split("\n")
    defs = {}
    body = []
    for ln in lines:
        m = DEF.match(ln)
        if m:
            defs[m.group(1)] = m.group(2)
        else:
            body.append(ln)
    used = set(REF.findall("\n".join(body)))
    for i in sorted(used - set(defs)):
        out.append(("ORPHAN_REF", rel, f"[^{i}]", "referenced but not defined"))
    for i in sorted(set(defs) - used):
        out.append(("UNUSED_DEF", rel, f"[^{i}]", "defined but never referenced"))
    cache = {}
    for i, d in defs.items():
        tag = f"[^{i}]"
        if d.startswith("[synthesis]"):
            out.append(("SYNTHESIS_SKIPPED", rel, tag, "needs judgment"))
            continue
        m = QUOTE.match(d)
        if not m:
            out.append(("MALFORMED", rel, tag, "expected: <raw path> — \"<quote>\" (<locator>)"))
            continue
        p = pathlib.Path(m.group("path").strip())
        target = (root / p).resolve()
        in_raw = target.is_relative_to((root / "raw").resolve())
        is_chat = (target.parent == (root / "_wikifier").resolve()
                   and CHAT_NAME.match(target.name) is not None)
        if not (in_raw or is_chat):
            out.append(("OUTSIDE_ROOT", rel, tag, str(p)))
            continue
        if not target.is_file():
            out.append(("FILE_MISSING", rel, tag, str(p)))
            continue
        if target.suffix.lower() not in TEXT_EXT:
            out.append(("UNSUPPORTED_TYPE", rel, tag, f"{target.suffix or '(none)'}: verify by reading the source"))
            continue
        if target not in cache:
            raw = target.read_text(encoding="utf-8", errors="replace")
            cache[target] = (norm(raw), raw.split("\n"))
        whole, rows = cache[target]
        q = norm(m.group("q"))
        if not q or q not in whole:
            out.append(("NOT_FOUND", rel, tag, f'{p}: "{q[:60]}"'))
            continue
        lm = LINES.search(m.group("loc") or "")
        if lm:
            a = int(lm.group(1)); b = int(lm.group(2) or a)
            if a < 1 or b < a or b > len(rows):
                out.append(("WRONG_LINES", rel, tag, f"{p}: lines {a}-{b} outside file ({len(rows)} lines)"))
                continue
            if q not in norm("\n".join(rows[a - 1:b])):
                out.append(("WRONG_LINES", rel, tag, f"{p}: quote exists but not in lines {a}-{b}"))
                continue
        out.append(("OK", rel, tag, str(p)))
    return out

def main(argv):
    if not argv:
        print(__doc__); return 2
    root = pathlib.Path(argv[0]).resolve()
    if not (root / "wiki").is_dir():
        print(f"ERROR no wiki/ under {root}"); return 2
    pages = [pathlib.Path(a).resolve() for a in argv[1:]] or sorted((root / "wiki").rglob("*.md"))
    res = []
    for pg in pages:
        res += check_page(root, pg)
    for r in res:
        print("\t".join(r))
    n = sum(1 for r in res if r[0] in BAD)
    print(f"# {len(res)} lines, {n} blocking", file=sys.stderr)
    return 0 if n == 0 else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
