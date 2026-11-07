# wiki-dig

Deep search in the wiki's SOURCES, used now and then when the pages are not enough: "when did we decide X?", "why did we choose Y?", "are we sure about Z?". It is the safety net behind `wiki-query`: the pages hold distilled knowledge, the sources also hold what distillation dropped (reasons, discarded alternatives, intermediate data, the exact original wording). Read-only: allowed in S3/S4 (see `preflight.md`). Writes nothing at all: no page, no index change, no `log.md` entry, no file.

Trigger phrases besides the command: "dig in the wiki", "deep search in the wiki"; Italian: "scava nella wiki", "storico della wiki", "ricerca approfondita nella wiki". A bare "storico" or "history" is NOT a trigger. A request to see the log (`log.md`) is not this command either: ask if unsure. Plain "deep search" or "ricerca approfondita" without the wiki is a web research request, not this command: ask if unsure.

## Scope

- `_wikifier/`: chat extracts (`*_chat-*.md`) and chat attachments (`*_allegato-*`). Saved plans and reports are NOT sources: skip them.
- `raw/`: every source folder, listed in the index or still pending ingest. Read only, as always.
- Never `trash/`. Wiki pages are read only to know what the wiki already says (step 2), never as evidence.

## Procedure

1. **Take the question** as given. If it is too vague to search, ask one short clarifying question (topic, rough period, names involved), otherwise start.
2. **Read what the wiki says first:** `index.md` and the pages that bear on the question, as in `cmd-query.md` step 2. This tells you what to look for and lets you compare.
3. **Pick candidate sources, do not read everything.** Use: the descriptions in `index.md` ("Estratti di chat" with their `allegato:` lines, "Sorgenti raw indicizzate"), the source pages under `wiki/sorgenti/` (summaries and "Allegati" sections), dates in `log.md`, and the names of pending `raw/` folders. Rank them by likelihood.
4. **Search the candidates.**
   - With a shell (Claude Code, Pi): run a case-insensitive keyword search with line numbers over the scope (for example `grep -rni`), with the obvious variants (singular/plural, Italian and English terms, codes and tag names). Then read only the passages around the hits.
   - Without a shell (Claude Desktop with file tools only): read the candidates one at a time, most likely first. After 5 files without an answer, stop: report what you read and what you found so far, and ask whether to continue and where.
   - Files you cannot read (binary, scanned, unsupported): name them as not searched.
5. **Answer in the chat,** in the user's language, short:
   - Every statement comes from a source you read, with the file path, the line locator (`L12` or `L12-14`) and a short verbatim quote.
   - Say how it relates to the pages: confirms them, adds something they lack, or differs from them. When it differs, give both versions with their locations and never pick one silently.
   - Do not add knowledge from outside the wiki's sources; if you must, mark it as "not from the wiki".
6. **Say what was not found and what was not searched** (files skipped, files unreadable, the part of the scope left out). Never fill gaps by guessing.
7. **If the finding should be in the pages** (a lost reason, a value that differs), suggest it in one line: "Questo manca nelle pagine: vuoi che lo registri con `wiki-update`?" The answer is now part of this chat, so `wiki-update` can record it citing the original source. Never write on your own.

## Cost

Use it occasionally, not for every question: `wiki-query` stays the normal way to ask the wiki. Never load the whole of `_wikifier/` or `raw/` into the chat; search, then read the passages that match.
