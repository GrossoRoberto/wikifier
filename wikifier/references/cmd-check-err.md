# wiki-check err

Runs `wiki-check`, then proposes and applies repairs. Allowed in S2 and S3. In S4: say "nothing to repair". In S0 or S1: error, point to `wiki-init`.

## Procedure

1. Run the `wiki-check` procedure (`cmd-check.md`) and keep the findings.
2. Build a repair plan from the fixable findings only, in this order, and show it as a numbered list BEFORE writing:

| Finding | Repair |
|---|---|
| Missing `raw/`, `wiki/`, `trash/` | Create the folder |
| Missing `index.md` | Create the empty skeleton, then rebuild (next row) |
| `index.md` misaligned (pages missing from the index, dead links, wrong counts) | Rebuild the affected entries. Title and description come from each page's frontmatter (`titolo`) and its first sentence; if none can be derived, ask the user or mark `> ❓ DA VERIFICARE`. Never invent descriptions |
| Missing `log.md` | Create it with a first `update` entry describing the repair |

3. **Raw sources and the index:** a `raw/` folder that is not listed is pending ingest, not an error. Never add it to the index: that would claim it was processed. A listed source that no longer exists in `raw/` is reported to the user, never removed automatically.
4. **Not repaired automatically** (list them as "needs your decision"): stray files, naming violations, malformed log entries, links into `trash/`, raw folder names. Never rename, move or delete anything in `raw/`.
5. Apply the plan following the `confirmations` policy from `infowiki.md`: `every-write` = ask before each step; `session-ok` = one confirmation for the whole plan.
6. After each step, verify by re-reading/listing.
7. Append one entry to `log.md`: `## [YYYY-MM-DD] update | check err: <n> repairs` with a short list of what changed (append method in `structure-v21.md`).
8. Re-run the alignment check. Report the new state. If it is not S4, list what remains.

## Rules

- Never overwrite a file without reading it first.
- Repairs touch only structure and `index.md`/`log.md`; page content is never modified here.
- If a repair fails, stop, report the exact error and the current state; do not retry blindly.
