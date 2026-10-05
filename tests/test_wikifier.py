"""Sandbox tests. They validate file formats, the preflight DEFINITIONS (via a reference
implementation) and scripts/verify_quotes.py. They do NOT test how a model behaves:
that needs a field test (see tests/field/README.md)."""
import os, re, shutil, subprocess, sys, tempfile, pathlib
REPO = pathlib.Path(__file__).resolve().parent.parent
SK = REPO / "wikifier"
SCRIPT = SK / "scripts" / "verify_quotes.py"
ok = True
def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg); ok &= bool(cond)

# ---- 1. skill structure ----
txt = (SK/"SKILL.md").read_text(encoding="utf-8")
m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", txt)
check(m, "frontmatter present")
name, desc = m.group(1), m.group(2)
check(name == SK.name and len(name) <= 64, "name == folder, <=64")
check(len(desc) <= 200, f"description {len(desc)} <= 200")
check("<" not in desc and ">" not in desc, "no angle brackets in description")
check(len(txt.splitlines()) < 500, "SKILL.md < 500 lines")
for r in sorted(set(re.findall(r"references/([\w\-\.]+\.md)", txt))):
    check((SK/"references"/r).exists(), f"references/{r} exists")
for r in sorted(set(re.findall(r"scripts/([\w\-\.]+\.py)", txt))):
    check((SK/"scripts"/r).exists(), f"scripts/{r} exists")
for f in list((SK/"references").glob("*.md")) + [SK/"SKILL.md", SCRIPT]:
    t = f.read_bytes()
    check(b"\r" not in t and not t.startswith(b"\xef\xbb\xbf"), f"{f.name}: LF, no BOM")
for f in (SK/"references").glob("*.md"):
    t = f.read_text(encoding="utf-8")
    check("192.168" not in t and "DatiLab" not in t, f"{f.name}: no personal data")
for cmd in ("ingest", "audit", "delete"):
    check(f"cmd-{cmd}.md" in txt and "not implemented" not in
          [l for l in txt.splitlines() if f"`wiki-{cmd}`" in l][0], f"SKILL.md routes wiki-{cmd}")

ing = (SK/"references/cmd-ingest.md").read_text(); dl = (SK/"references/cmd-delete.md").read_text()
check("reading it is allowed" in txt.lower(), "SKILL.md: reading raw/ allowed")
check("Approval covers every write listed in the plan" in ing, "ingest: plan approval covers writes")
check("loose files" in ing and "mkdir" in ing, "ingest: loose files get ready commands")
check("trash/" in dl and "Never `raw/`" in dl and "BOTH confirmation modes" in dl, "delete: trash only, never raw, plan always approved")
check("approval covers every write" in txt, "SKILL.md: confirmation exception")

# ---- 2. reference preflight ----
REQ = ["index.md","log.md","raw","wiki","trash"]
def parse_info(p):
    if not p.exists(): return None
    m = re.match(r"---\n(.*?)\n---", p.read_text(), re.S)
    if not m: return None
    d = {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)}
    return d if all(d.get(k) for k in ("project_name","path","domain")) else None
def aligned(root):
    idx = (root/"index.md").read_text()
    links = set(re.findall(r"\]\((wiki/[^)]+\.md)\)", idx))
    pages = {p.relative_to(root).as_posix() for p in (root/"wiki").rglob("*.md")}
    raws = {p.name for p in (root/"raw").iterdir() if p.is_dir()}
    listed = set(re.findall(r"`raw/([^/`]+)/`", idx))
    return pages <= links and all((root/l).exists() for l in links) and listed <= raws
def state(info):
    d = parse_info(info)
    if not d: return "S0"
    root = next((pathlib.Path(d[k]) for k in ("path","path_alt") if d.get(k) and pathlib.Path(d[k]).exists()), None)
    if not root: return "S1"
    if not all((root/x).exists() for x in REQ): return "S2"
    return "S4" if aligned(root) else "S3"
pf = (SK/"references/preflight.md").read_text()
for c in ("`wiki-init`","`wiki-check`","`wiki-check err`","`wiki-status`","`wiki-audit`"):
    check(c in pf or "`audit`" in pf, f"preflight covers {c}")
check("pending ingest" in pf, "preflight defines pending ingest")
tmp = pathlib.Path(tempfile.mkdtemp())
def mk(name, info=True, root=True, req=None, index="ok", pending=False, listed_missing=False):
    base = tmp/name; base.mkdir(); r = base/"root"; req = REQ if req is None else req
    if info:
        (base/"infowiki.md").write_text(f"---\nproject_name: T\npath: {r}\npath_alt: \ndomain: d\n---\n")
    if root:
        r.mkdir()
        for x in req: (r/x).mkdir() if "." not in x else (r/x).write_text("")
        if "wiki" in req: (r/"wiki/cat").mkdir(); (r/"wiki/cat/p.md").write_text("x")
        if "raw" in req:
            (r/"raw/2026-01-01_a").mkdir()
            if pending: (r/"raw/2026-02-02_b").mkdir()
        if "index.md" in req:
            body = "# Index\n### cat\n- [P](wiki/cat/p.md) — d\n## Sorgenti raw indicizzate\n- `raw/2026-01-01_a/` — s\n"
            if listed_missing: body += "- `raw/2025-12-12_gone/` — s\n"
            if index == "stale": body = "# Index\n"
            (r/"index.md").write_text(body)
    return base/"infowiki.md"
for k, (p, exp) in {
  "S0 no infowiki": (mk("a", info=False), "S0"), "S1 root missing": (mk("b", root=False), "S1"),
  "S2 no trash": (mk("c", req=["index.md","log.md","raw","wiki"]), "S2"),
  "S3 page not in index": (mk("d", index="stale"), "S3"), "S4 healthy": (mk("e"), "S4"),
  "S4 with pending raw (must NOT be S3)": (mk("f", pending=True), "S4"),
  "S3 listed raw source gone": (mk("g", listed_missing=True), "S3")}.items():
    got = state(p); check(got == exp, f"{k}: expected {exp}, got {got}")
bad = tmp/"bad.md"; bad.write_text("---\nproject_name: T\npath:\ndomain: d\n---\n")
check(state(bad) == "S0", "empty path -> S0")

# ---- 3. verify_quotes.py with seeded errors ----
w = tmp/"vw"; (w/"wiki/cat").mkdir(parents=True); (w/"raw/2026-10-01_n").mkdir(parents=True)
(w/"raw/2026-10-01_n/notes.md").write_text("Pump A.\nNominal speed is\n  1450   rpm  at 50 Hz.\nService every 2000 hours.\n", encoding="utf-8")
(w/"raw/2026-10-01_n/scan.pdf").write_bytes(b"%PDF-1.4")
(w/"secret.md").write_text("Outside raw: nominal speed is 1450 rpm")
page = '''---
titolo: P
---
Ok whitespace.[^1] Wrong text.[^2] Missing file.[^3] Pdf.[^4] Bad shape.[^5] Escape.[^6] Synth.[^7] Case.[^8] Orphan.[^9]

[^1]: raw/2026-10-01_n/notes.md — "Nominal speed is 1450 rpm" (line 2)
[^2]: raw/2026-10-01_n/notes.md — "nominal speed is 1480 rpm" (line 2)
[^3]: raw/2026-10-01_n/ghost.md — "anything at all here" (p1)
[^4]: raw/2026-10-01_n/scan.pdf — "some text from the pdf" (p1)
[^5]: raw/2026-10-01_n/notes.md nominal speed
[^6]: raw/../secret.md — "nominal speed is 1450 rpm" (x)
[^7]: [synthesis] raw/2026-10-01_n/notes.md — my inference
[^8]: raw/2026-10-01_n/notes.md — "NOMINAL SPEED IS 1450 RPM" (line 2)
[^10]: raw/2026-10-01_n/notes.md — "Service every 2000 hours" (line 3)
'''
(w/"wiki/cat/p.md").write_text(page, encoding="utf-8")
def run(*a): return subprocess.run([sys.executable, str(SCRIPT), *map(str, a)], capture_output=True, text=True)
r = run(w); got = {}; allst = {}
for l in r.stdout.splitlines():
    s, _, tag, _ = l.split("\t", 3); got.setdefault(tag, s) if s != "UNUSED_DEF" else None; allst.setdefault(tag, set()).add(s)
exp = {"[^1]":"OK","[^2]":"NOT_FOUND","[^3]":"FILE_MISSING","[^4]":"UNSUPPORTED_TYPE","[^5]":"MALFORMED",
       "[^6]":"OUTSIDE_ROOT","[^7]":"SYNTHESIS_SKIPPED","[^8]":"NOT_FOUND","[^9]":"ORPHAN_REF","[^10]":"OK"}
for k, v in exp.items(): check(got.get(k) == v, f"verify_quotes {k}: expected {v}, got {got.get(k)}")
check("UNUSED_DEF" in allst["[^10]"], "unused definition flagged")
check(r.returncode == 1, "exit 1 when blocking findings exist")
good = tmp/"gw"; (good/"wiki").mkdir(parents=True); shutil.copytree(w/"raw", good/"raw")
(good/"wiki/g.md").write_text('Fact.[^1]\n\n[^1]: raw/2026-10-01_n/notes.md — "Service every 2000 hours" (l3)\n', encoding="utf-8")
check(run(good).returncode == 0, "exit 0 on a clean wiki")
check(run(tmp/"nope").returncode == 2, "exit 2 when wiki/ is missing")
# no writes
before = sorted(p.as_posix() for p in w.rglob("*")); run(w)
check(before == sorted(p.as_posix() for p in w.rglob("*")), "script is read-only")
shutil.rmtree(tmp)
print("\nALL PASS" if ok else "\nSOME FAILED"); sys.exit(0 if ok else 1)
