# wiki-query

Answer a question in the chat, using ONLY what the wiki contains. Read-only: allowed in S3/S4 (see `preflight.md`). Writes nothing at all: no page, no index change, no `log.md` entry, no file. If the user wants the answer saved, tell them wiki-query does not do that.

## Procedure

1. **Take the question** as given. If it is too vague to search ("tell me about the pump"), ask one short clarifying question, otherwise start.
2. **Find the pages:** read `index.md` and pick the pages whose title or description may bear on the question. Read those pages fully; follow relative links only when needed. Do not read the whole wiki, and do not open `raw/` or `trash/` (the wiki answers; sources are for `wiki-audit`).
3. **Answer in the chat,** in the user's language, short and direct:
   - Every statement comes from a page you read. Name the page (path or title) after it.
   - When a page carries a footnote citation, you may mention the raw source it points to, without re-checking it.
   - Do not add knowledge from outside the wiki. If you must say something general, mark it clearly as "not from the wiki".
4. **Say what the wiki does not cover.** If the answer is missing or partial, say so plainly ("the wiki does not say X"). Never fill gaps by guessing.
5. **Flag open items that touch the answer:** a `> ⚠️ CONTRADDIZIONE` block (give both values and their citations, never pick one), a `> ❓ DA VERIFICARE` item, or a page whose `stato` is not `verificato`.
6. **If the index looked stale** (state S3: pages missing from `index.md`), say the answer may be incomplete and suggest `wiki-check`.

Answers are only as reliable as the pages. Do not present a wiki answer as verified against the sources: that is what `wiki-audit` is for.
