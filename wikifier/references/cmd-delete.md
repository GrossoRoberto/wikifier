# wiki-delete

Soft-delete wiki pages: MOVE them into `trash/`, never erase. Allowed only in state S4 (see `preflight.md`).

## Scope

- Only files under `wiki/` (pages). Never `raw/` (immutable: if asked, refuse and say so), never `index.md`, `log.md`, `infowiki.md`.
- One or more pages named by the user. No wildcards and no "delete everything": if the request is vague, list candidates and ask.

## Procedure

1. **Resolve** each target to a real path under `wiki/`; refuse any path that does not resolve there.
2. **Find inbound links:** read `index.md` and the other pages, list every page that links to a target. These links would break.
3. **Show the plan and wait for approval — in BOTH confirmation modes.** For each target: path, title, inbound links, and what happens to each (default: remove the link from the linking page, keeping its text; or leave it and report it as dead, the user chooses). Deleting is the one operation the user must always see in full before it happens.
4. **Move** each target to `trash/` with a unique dated name: `trash/YYYY-MM-DD_<category>_<file>.md` (add `-2`, `-3` if that name exists; the connector's move fails when the destination exists). Do not edit the moved content.
5. **Fix the wiki:** remove the page from `index.md` (entry, counts, "Aggiornato"); apply the approved edits to the linking pages (and set their `aggiornato`). If the category folder is now empty, leave it and tell the user (an empty folder cannot be removed here).
6. **Append to `log.md` LAST:** `## [YYYY-MM-DD] delete | <page path>` with the trash name and the pages edited.
7. **Verify:** targets gone from `wiki/`, present in `trash/`, no link in `index.md` or in any page points to them, state still S4. Report in a few lines, including the trash name so the user can restore it (restore = move back by hand or by asking; it is not a command).

## Notes

- The raw source a deleted page cited stays in `raw/` and in "Sorgenti raw indicizzate": other pages may use it. Say so if the deleted page was the only one citing it, and leave the decision to the user.
- If interrupted midway, do not write the log; tell the user which pages were already moved.
