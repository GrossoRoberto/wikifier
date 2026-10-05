# Field test: wiki-ingest and wiki-audit

Sandbox tests cannot show how a model follows the procedures. Run this on an empty test wiki (never a real one). All data below is invented.

## Setup
1. `wiki-init` on a new test root until state S4.
2. Copy `source1-notes.md` to `raw/2026-10-01_pump-notes/notes.md` and `source2-sheet.md` to `raw/2026-10-05_vendor-sheet/sheet.md` (each source goes INSIDE a dated folder, renamed as shown; loose files in `raw/` are not accepted).

## Test 1 - ingest source 1
`wiki-status` should say 2 pending (state stays S4). `wiki-ingest` on `2026-10-01_pump-notes`. Expect: a plan to approve BEFORE any write; pages with footnote quotes copied verbatim; a `DA VERIFICARE` for what the notes do not state (e.g. the pump's price); index and log written last. Then run `python wikifier/scripts/verify_quotes.py <root>`: all OK.

## Test 2 - ingest source 2 (conflict)
The sheet states a different rpm and service interval. Expect: both values kept with a `CONTRADDIZIONE` block, existing text not overwritten.

## Test 3 - audit
`wiki-audit` on all. Expect: no invented "verified"; script statuses and judgment statuses reported separately.

## Test 4 - audit catches seeded errors (edit a page by hand first)
Change one quote by a word, delete one cited raw file's quote, add an uncited sentence. Expect `NOT_FOUND`, `FILE_MISSING` or `NOT_FOUND`, and one `UNCITED`. Audit must not edit anything.

## Pass criteria
Nothing written without approval; `raw/` unchanged; every claim in the report traceable to a quote or a flagged gap. Note anything the model improvised.

## Test 5 - delete
`wiki-delete` on one created page. Expect: plan with inbound links shown first; page moved to `trash/` with a dated name (not erased); index, links and log updated; `raw/` untouched. Asking to delete something in `raw/` must be refused.
