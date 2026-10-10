# wiki-ingest

Turn ONE raw source into wiki pages. Allowed only in state S4 (see `preflight.md`). Citation rules: `structure-v21.md` "Citations".

## Procedure

1. **Pick the source.** List `raw/` folders NOT listed in `index.md` ("Sorgenti raw indicizzate") = pending ingest. If `raw/` holds loose files instead of folders, do not move them (raw is immutable) and do not start: tell the user, with ready-to-run commands, how to place each file in a `raw/YYYY-MM-DD_description/` folder (PowerShell: `mkdir <folder>` then `move <file> <folder>\<file>`). Do NOT ask whether you may read `raw/`: reading is always allowed. If the user named one, use it (it must exist in `raw/`). If several are pending and none was named, show the list and ask which. One source per run, never a batch. `_wikifier/` is not a source: never ingest from it. Do not create plan or report files: the plan is shown in the chat.
2. **Read the source completely.** Read every file in the folder with the tools in `tools-map.md`. If a file cannot be read (binary, scanned, too large, unsupported), say which and what part is therefore NOT covered. Never summarize from a partial read without saying so.
3. **Read the wiki context:** `index.md`, then the pages that may overlap (by title/category). Do not read the whole wiki.
   **Backlink sweep (search only):** take the names of the entities/concepts this source will create or touch (page titles and key terms). Search the other pages in `wiki/` by text for each name (a text search tool, not reading every page; if no search tool exists, use the index descriptions and say the sweep was partial). Collect: pages that mention an entity without linking to it, and pages that mention it with a value that may conflict.
4. **Propose a plan and wait for approval — in BOTH confirmation modes.** Show: (a) 3–7 key takeaways; (b) pages to CREATE (path + one line, always including the source page `wiki/sorgenti/<raw-folder>.md`) and pages to UPDATE (path + what changes); (c) backlinks to add in existing pages, one line each with the exact line that would change, plus possible conflicts found by the sweep; (d) conflicts with existing content; (e) what the source does not cover. Ingest changes many files at once, so the plan is always approved first. Approval covers every write listed in the plan, including `index.md` and `log.md`: do not ask again for each page. A write that is NOT in the plan (an extra page, a changed plan) needs a new approval.
5. **Write the pages**, following `structure-v21.md` (frontmatter, relative links, categories rule):
   - Every factual claim carries a footnote with a verbatim quote from the raw file. Copy the quote exactly from the source (4–25 words); never reconstruct it from memory.
   - Your own inference or combination of sources: footnote `[synthesis]`, never a quote.
   - Something the source does not state or you cannot confirm: `> ❓ DA VERIFICARE`. Do not fill gaps.
   - Conflict with an existing page: keep both, add the `> ⚠️ CONTRADDIZIONE` block (format in `structure-v21.md`). Never overwrite or silently "correct" existing content.
   - Updating an existing page: change only what the source affects, set `aggiornato`, add the new `sorgenti` entry; keep earlier citations intact.
   - Source page first (see `structure-v21.md` "Source pages"), then entity/concept pages linking to it.
   - Add relative links to and from related pages. Apply ONLY the backlinks listed in the approved plan; do not rewrite the surrounding text. If a mention is ambiguous (generic word), leave it out and say so.
   - Line locators (`L12-14`) on citations for text files, per `structure-v21.md`.
6. **Verify, before touching the index:** re-read each written page; check frontmatter, that every link resolves, and that every footnote reference has a definition. Check that no new page is an orphan (every new page has an inbound link from another page). If `scripts/verify_quotes.py` can run (Claude Code, Pi with a shell), run it on the written pages; otherwise re-check each quote against the raw text by reading. Fix and repeat. Report honestly any quote you could not verify.
7. **Update `index.md`:** add/refresh page entries, add the source under "Sorgenti raw indicizzate" with today's date, update the counts and "Aggiornato".
8. **Append to `log.md` LAST** (so the log never claims work that did not finish): `## [YYYY-MM-DD] ingest | <raw folder>` with pages created/updated and unresolved items.
9. **Final checks:** `raw/` untouched (same listing as step 2); index aligned (state still S4). Report in a few lines: pages created/updated, citations verified how (script or manual), open `DA VERIFICARE` and `CONTRADDIZIONE` items, anything not covered.

## Failure handling

- Stopped midway (error, user cancels): do NOT write the index or log. Tell the user exactly which pages were already written; the next `wiki-check` will flag them as not indexed and `wiki-check err` can finish the job.
- Never delete or overwrite a page to "start over"; use `trash/` (soft-delete) only if the user asks.

The plan is shown in the chat. Save it as a file only if the user asks (`structure-v21.md` "Saved plans and reports"); a saved plan never replaces the approval.
