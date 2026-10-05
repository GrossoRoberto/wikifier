# Structure profile "v2.1" (provisional)

Layout taken from the project's SCHEMA v2.1, tested on the field with the filesystem connector. It is a provisional profile: a dedicated session will decide whether to keep it, adopt a hybrid, or replace it. ALL layout knowledge lives in this file, nowhere else in the skill.

## Required items (used by preflight S2)

```
<root>/
├── index.md          catalog of all wiki pages and raw sources
├── log.md            chronological, append-only record
├── raw/              immutable sources
├── wiki/             pages written and maintained by Claude
└── trash/            soft-delete bin (ignored by everything)
```

Rules: `raw/` sources live in folders named `YYYY-MM-DD_short-description/`. `wiki/` allows at most 2 levels: `wiki/<category>/<page>.md`. Categories and page files are lowercase, hyphen-separated, no spaces, `.md`. Create a category only when at least 3 pages share a distinct domain.

**Tolerated files (not reported as stray, ignored by index and ingest):** `.gitkeep` placed inside a required folder (some toolsets cannot create empty folders, so it is the accepted workaround; tell the user when you use it), and `infowiki.md` in the wiki root.
**Never valid inside `raw/` or `wiki/`:** `infowiki.md` (it is configuration, not a source or a page).

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
```

Empty skeleton (used by init): same header with `Pagine totali: 0 | Sorgenti raw: 0` and the section headings without entries.

## log.md format

Append-only: never modify previous entries. Each entry starts with a parseable prefix.

```markdown
# Log — <project_name> Wiki

## [YYYY-MM-DD] update | short description
Reason / details.
```

Entry types: `ingest`, `query`, `lint`, `update`. First entry written by init: `## [date] update | bootstrap struttura iniziale`.

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

## Links

Relative markdown links based on the file's own path (no `[[wikilinks]]`). Renaming or moving a page breaks inbound links.
