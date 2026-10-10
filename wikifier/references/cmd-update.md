# wiki-update

Bring what happened in THIS chat into the wiki. Allowed only in state S4 (see `preflight.md`). It is NOT `wiki-ingest`: ingest processes folders that already exist in `raw/`; update processes the conversation itself. Never run ingest on chat content.

## Procedure

1. **Find the starting point.** Read the last entries of `log.md` and take the most recent `## [date] update | chat: ...` entry; its "Coperto fino a" line says where the previous update stopped. Compare with what you can still see in this chat. If the chat started after that point, or the earlier part is no longer visible (new chat, compacted context), say so and state exactly which range you can cover; ask the user if the range is unclear. Never reconstruct from memory what you cannot see.
2. **Select what is durable.** Keep: decisions taken, facts established or changed, definitions, corrections of earlier data, relations between things, open questions that matter. Drop: small talk, failed attempts, discarded ideas, tool noise. An important but unconfirmed idea goes in only as `> ❓ DA VERIFICARE`. NEVER write secrets (passwords, tokens, keys) or personal data that has no reason to be in the wiki.
3. **Read the wiki context** like ingest step 3: `index.md`, the pages the news may touch, and the backlink sweep (search only, by entity name).
4. **Propose a plan and wait for approval — in BOTH confirmation modes.** Show: (a) the items to record, one line each; (b) for each: the page to create or update and what changes (for an existing value: old → new); (c) the chat extract that would be created (file name in `_wikifier/`, which messages, roughly how many lines); (d) backlinks to add, one line each; (e) what you could NOT cover. Approval covers every write in the plan, including `index.md` and `log.md`. Anything outside the plan needs a new approval.
5. **Save the chat extract** as `_wikifier/YYYY-MM-DD_chat-<topic>.md` (topic in lowercase hyphens; if the name exists add `-2`; `_wikifier/` already exists, created by `wiki-init`: if it is missing the wiki is not S4). NEVER write in `raw/`: it is immutable and no command touches it. Content: a header (date, topic, "verbatim extract, do not edit"), then only the relevant messages, each as `## Message N — user|assistant` followed by its text copied exactly as visible. Never paraphrase, never include secrets. Re-read the file after writing; do not edit it afterwards. Do not create any other file (no plan or report files): plans are shown in the chat.
6. **Write the pages** as in `cmd-ingest.md` step 5 (source page `wiki/sorgenti/<folder>.md`, footnotes with a verbatim quote and `L` line locator pointing to the chat extract, `[synthesis]`, `DA VERIFICARE`, approved backlinks only). When the chat states that an earlier value was wrong or changed, update the value in place and keep the history with:
   `> 🔄 CORRETTO (YYYY-MM-DD): <old value>[^a] → <new value>[^b]`
   Do not use this block when two sources merely disagree: that is a `CONTRADDIZIONE`.
7. **Verify** as in `cmd-ingest.md` step 6 (links, footnotes, `verify_quotes.py` if a shell exists, no new orphan page).
8. **Update `index.md`** (pages, the extract under "Estratti di chat" (add the section if missing), "Aggiornato"). Counts of raw sources do not change.
9. **Append to `log.md` LAST:** `## [YYYY-MM-DD] update | chat: <topic>` with the lines `Coperto fino a: <last topic or message covered>`, the pages created/updated, and open items.
10. **Report** in a few lines: pages touched, extract size (lines), what was not covered. Keep it cheap: if nothing durable happened since the last update, say so and write nothing.

## Failure handling

Same as `cmd-ingest.md`: if interrupted, do not write index or log; tell the user which files were already written.

## Proactive suggestion

See SKILL.md "Working inside a wiki chat". The suggestion never writes anything.

The plan is shown in the chat. Save it as a file only if the user asks (`structure-v21.md` "Saved plans and reports"); a saved plan never replaces the approval.
