# wiki-check

Read-only self-diagnosis. It never writes anything: no files, no log entry.

## Procedure

1. Run the full preflight (`preflight.md`), including the alignment check. Do not stop at the first failure: collect all findings up to the point where later checks become impossible (for example, if the root is unreachable, nothing below it can be checked).
2. Run these checks and record each as ✅ / ⚠️ / ❌:

| # | Check | Fail level |
|---|---|---|
| 1 | `infowiki.md` found, all required variables present; list unknown keys | ❌ missing/incomplete, ⚠️ unknown keys |
| 2 | Root reachable (`path`, else `path_alt`); say which one is used | ❌ |
| 3 | Required items exist: `index.md`, `log.md`, `raw/`, `wiki/`, `trash/` | ❌ each missing |
| 4 | `index.md` header present; counts (`Pagine totali`, `Sorgenti raw`) match reality | ⚠️ |
| 5 | Every page under `wiki/` is listed in `index.md` | ⚠️ |
| 6 | Every link in `index.md` resolves to an existing file (no links into `trash/`) | ❌ |
| 7 | Every raw source listed in `index.md` still exists in `raw/` (❌ if missing). Unlisted `raw/` folders are NOT a problem: report them as info "pending ingest: n". Folder names follow `YYYY-MM-DD_description` (⚠️ if not) | ❌ / ⚠️ |
| 8 | Page files and category folders follow naming (lowercase, hyphens, `.md`); depth ≤ 2 levels | ⚠️ |
| 9 | `log.md` entries all start with `## [YYYY-MM-DD] <type> | ...` | ⚠️ |
| 10 | Stray files outside the expected layout (report only, never move). Do not report `.gitkeep` files or `infowiki.md` in the root. Report `infowiki.md` found inside `raw/` or `wiki/` as misplaced (it would be mistaken for a source) | ⚠️ |
| 11 | Orphan pages: a page under `wiki/` that no OTHER page under `wiki/` links to (links from `index.md` do not count). List them | ⚠️ |
| 12 | Every raw source listed in `index.md` has its source page `wiki/sorgenti/<folder>.md` (wikis ingested before source pages existed will show this: report as info, not an error) | ⚠️ |

Checks 5–9, 11 and 12 need a populated wiki; on an empty one they pass trivially.
This phase does not verify page content (contradictions, citations): that is `wiki-audit`.

## Output (in the user's language, short)

```
State: S<n> — <one-line meaning>
Root: <path used>
✅ / ⚠️ / ❌ per check (only list the non-✅ ones in detail)
Next step: <command>
```

Next-step mapping: S0 → `wiki-init` (draft mode); S1 → `wiki-init`; S2 or S3 → `wiki-check err`; S4 → nothing to do.
Never claim a check passed if you did not run it: say "not verified".
