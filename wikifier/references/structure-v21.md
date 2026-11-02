# Structure profile "v2.1" (provisional)

Layout taken from the project's SCHEMA v2.1, tested on the field with the filesystem connector. It is a provisional profile: a dedicated session will decide whether to keep it, adopt a hybrid, or replace it. ALL layout knowledge lives in this file, nowhere else in the skill.

## Required items (used by preflight S2)

```
<root>/
├── index.md          catalog of all wiki pages and raw sources
├── log.md            chronological, append-only record
├── raw/              immutable sources
├── wiki/             pages written and maintained by Claude
├── trash/            soft-delete bin (ignored by everything); names `YYYY-MM-DD_<category>_<file>.md`
└── _wikifier/        system folder, NO subfolders (ignored by index, ingest and the alignment check, like `trash/`)
```

`_wikifier/` holds three kinds of files, told apart by the word after the date:
- `YYYY-MM-DD_chat-<topic>.md`: chat extracts written by `wiki-update`. They are sources: never edited afterwards, cited by pages.
- `YYYY-MM-DD_allegato-<topic>--<original-name>.<ext>`: chat attachments written by `wiki-update` (files generated during that chat, copied as they are). Same date and topic as their extract. They are sources: never edited afterwards, may be cited, searched by `wiki-dig`.
- `YYYY-MM-DD_<type>-<topic>.md` with type `piano-ingest`, `piano-update`, `piano-delete`, `audit` or `check`: plans and reports, ONLY when the user asks to save them. They are not sources: never cited.
The word `chat` is reserved for extracts and the word `allegato` for attachments.

The whole tree above is created by `wiki-init` (empty folders). `_wikifier/` is a required item: a wiki created before it existed is state S2 until `wiki-check err` adds it. No other file or folder may be created in the wiki root. Plans and reports are shown in the chat.

Rules: `raw/` sources live in folders named `YYYY-MM-DD_short-description/`. `wiki/` allows at most 2 levels: `wiki/<category>/<page>.md`. Categories and page files are lowercase, hyphen-separated, no spaces, `.md`. Create a category only when at least 3 pages share a distinct domain.

**Tolerated files (not reported as stray, ignored by index and ingest):** the `_wikifier/` system folder (above); `.gitkeep` placed inside a required folder (some toolsets cannot create empty folders, so it is the accepted workaround; tell the user when you use it), and `infowiki.md` in the wiki root.
**Never valid inside `raw/` or `wiki/`:** `infowiki.md` (it is configuration, not a source or a page).

## Chat extracts

`wiki-update` saves what it records from a conversation as `_wikifier/YYYY-MM-DD_chat-<topic>.md` (verbatim extract of the relevant messages only; if the name exists add `-2`). NEVER in `raw/`, which no command writes to. After writing, the file is not edited again; it is cited with verbatim quotes and line locators, listed in the index section "Estratti di chat", and has its own source page `wiki/sorgenti/YYYY-MM-DD_chat-<topic>.md`. Log entries: `## [date] update | chat: <topic>` including `Coperto fino a: ...`. A correction of an earlier value keeps its history with `> 🔄 CORRETTO (date): old[^a] → new[^b]`.

## Chat attachments

Files that Claude generated or rewrote during the chat (notes, reports, analyses, lists, code in any language, HTML, JSON, config) are the densest part of a session and an extract of the messages does not contain them. `wiki-update` saves the latest version of each one next to its extract:

- Name: `_wikifier/YYYY-MM-DD_allegato-<topic>--<original-name>.<ext>`. `<topic>` is the extract's topic, `--` separates it from the original file name (lowercased, spaces turned into hyphens), and the original extension is kept so the file still opens as what it is. If the name exists add `-2` before the extension.
- Content: the file as it is, never rewritten, summarized or "cleaned". Copy it with a tool that transfers the file unchanged; see `cmd-update.md` step 6 ("Save the attachments") for the copy rule and how to mark a copy that could not be verified.
- Not saved: files the user uploaded to the chat (the user still has them: list them in the source page instead), binary files (list them), intermediate versions, and any file holding secrets (passwords, tokens, keys).
- After writing, never edited again.
- Role: a **safety net**, not the primary knowledge. What matters is distilled into pages as usual; attachments keep what distillation drops (reasons, discarded alternatives, intermediate data) so that it can still be found with `wiki-dig`. Pages do not have to link them.
- Listed in `index.md` under their extract (see the format below) and in the "Allegati" section of the extract's source page, each with 2–3 lines on what it CONTAINS (topics, decisions, data), not just its name: a report with a vague title must still be findable.

## Saved plans and reports

Default: plans (ingest, update, delete) and reports (audit, check) are shown in the chat and NOT saved. Only when the user explicitly asks to keep one:

- File: `_wikifier/YYYY-MM-DD_<type>-<topic>.md`. Types: `piano-ingest`, `piano-update`, `piano-delete`, `audit`, `check`. Example: `2026-10-10_piano-ingest-pump-notes.md`. If the name exists add `-2`, `-3`; never overwrite.
- Content: frontmatter (`tipo`, `comando`, `data`, `ambito`) followed by exactly what was shown in the chat. Nothing is added or invented.
- One file per run, written only after the user asks, and not edited afterwards.
- Not listed in `index.md`, not written to `log.md`, never cited as a source, ignored by ingest, audit and query.
- A saved plan is NOT an approval: approval is still asked in the chat. Never create these files "to be safe" and never put them anywhere else (no `piano-*.md` or `audit-*.md` in the root, in `raw/` or in `wiki/`).

## Source pages

Each ingested raw source has ONE source page: `wiki/sorgenti/<raw-folder-name>.md` (category `sorgenti`, exempt from the 3-pages rule). It holds: a short summary, 3–7 key takeaways with citations, a "Pagine derivate" list linking the pages created or updated from that source, and what the source does not cover. Other pages link to it from their `sorgenti` field and footnotes' context. Frontmatter as usual (`categoria: sorgenti`).

A chat extract's source page (`wiki/sorgenti/YYYY-MM-DD_chat-<topic>.md`) also has an "Allegati" section when attachments were saved: one entry per attachment with a relative link (`../../_wikifier/<file>`) and 2–3 lines on what it contains, plus a "Non salvati" line listing files the user uploaded and binary or secret-holding files that were left out. Without attachments the section says "nessuno".

## index.md format

```markdown
# Index — <project_name> Wiki
Aggiornato: YYYY-MM-DD | Pagine totali: N | Sorgenti raw: N

## Categorie

### <category>
- [Page title](wiki/<category>/<file>.md) — one-line description (agg: YYYY-MM-DD)

## Pagine da completare
- [Page](path) — what is missing

## Sorgenti raw indicizzate
- `raw/YYYY-MM-DD_topic/` — description, processed on: date

## Estratti di chat
- `_wikifier/YYYY-MM-DD_chat-topic.md` — description, recorded on: date
  - allegato: `_wikifier/YYYY-MM-DD_allegato-topic--file.ext` — what it contains, in one line
```

The section "Estratti di chat" is added by `wiki-update` the first time; the empty skeleton does not have it. Attachments are listed as indented `allegato:` lines under their extract. A `.gitkeep` inside `_wikifier/` is not an extract, an attachment or a report. The counts in the header refer to raw sources only.

Empty skeleton (used by init): same header with `Pagine totali: 0 | Sorgenti raw: 0` and the section headings without entries.

## log.md format

Append-only: never modify previous entries. Each entry starts with a parseable prefix.

```markdown
# Log — <project_name> Wiki

## [YYYY-MM-DD] update | short description
Reason / details.
```

Entry types: `ingest`, `update` (including `update | chat: <topic>`), `delete` (`wiki-query` and `wiki-audit` write nothing, so they have no entry). First entry written by init: `## [date] update | bootstrap struttura iniziale`.

Appending: the connector has no append tool. Use an exact-match edit (old text = last entry, new text = last entry + new entry) or read-modify-write. Both preserve earlier entries and LF line endings.

## Page frontmatter (for pages created by later phases)

```yaml
---
titolo: Readable Page Name
categoria: category-name
creato: YYYY-MM-DD
aggiornato: YYYY-MM-DD
---
```

Optional: `sorgenti` (list of raw paths), `importanza` (bassa|media|alta|critica), `stato` (bozza|verificato|archiviato), `tag`.

## Citations (used by ingest and audit)

Claims in a page body carry footnote references; definitions go at the bottom of the page. Straight double quotes, em dash `—` as separator:

```markdown
The pump runs at 1450 rpm.[^1] The service interval looks shorter than the vendor's.[^2]

[^1]: raw/2026-10-01_pump-notes/notes.md — "nominal speed is 1450 rpm" (section 2)
[^2]: [synthesis] raw/2026-10-01_pump-notes/notes.md, raw/2026-10-05_vendor/sheet.md — compared the two service intervals
```

- Quote: verbatim from the raw file, 4–25 words, copied not recalled. A check ignores only whitespace differences (case-sensitive, NFC).
- Locator in parentheses: section, page, line or timestamp, as precise as the source allows. For text files add line numbers as `L12` or `L12-14` (1-based lines of the raw file, e.g. `(L3)` or `(section 2, L12-14)`); `verify_quotes.py` then checks the quote lies inside those lines. Use line numbers only when your tool shows them; never guess them (a section locator is better than a wrong line number).
- Information not stated by the sources: `> ❓ DA VERIFICARE`.
- Conflict between sources or with existing text (keep both, never overwrite):

```markdown
> ⚠️ CONTRADDIZIONE (YYYY-MM-DD): 1450 rpm[^1] ↔ 1480 rpm[^3]
```

## Links

Relative markdown links based on the file's own path (no `[[wikilinks]]`). Renaming or moving a page breaks inbound links.
