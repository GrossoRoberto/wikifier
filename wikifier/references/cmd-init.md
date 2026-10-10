# wiki-init

Two modes, decided by the preflight state.

## State S0 — draft mode (nothing is created)

`infowiki.md` is missing or incomplete. Do NOT create any wiki folder.

1. Say which variables are missing or empty (if the file exists) or that the file was not found, and where you looked (Project knowledge; launch directory).
2. Collect the values with a short interview (use a multiple-choice question tool if available, otherwise plain questions). Ask only what you cannot infer: `project_name`, `path`, `path_alt` (optional), `domain`, `language` (default `it`), `confirmations` (default `every-write`). Explain each in one line.
3. If `path` is on a machine you can reach, verify it (see `tools-map.md`) without writing anything. If unreachable, still produce the draft and flag the path as unverified.
4. Output the completed `infowiki.md` (template in `infowiki-template.md`) in a code block, plus these instructions:
   - **Claude Desktop:** add it as a file named `infowiki.md` to the Project knowledge, then start a new chat and run `wiki-init` again.
   - **Claude Code / other agents:** save it as `infowiki.md` in the directory the agent is launched from (offer to write it there; ask for confirmation first), then run `wiki-init` again.
5. Stop. Do not run the bootstrap in the same turn.

## States S1 and S2 — bootstrap

1. Show the resolved root path and which of `path` / `path_alt` is used. Ask the user to confirm it **before writing anything**, and (Desktop) confirm it is inside the allowed directories.
2. List what exists in the root (S2) so existing files are never overwritten. Read a file before touching it.
3. Create, per `structure-v21.md`, only what is missing: the root folder, and the EMPTY folders `raw/`, `wiki/`, `trash/`, `_wikifier/chat/`, `_wikifier/report/` (the whole structure, from the start). Creating empty `raw/` is part of the bootstrap. If the toolset cannot create empty folders, write a `.gitkeep` inside each one and tell the user. Do not say you will try something and then skip it: report exactly what you did.
4. Create `index.md` as the empty skeleton (`Pagine totali: 0`, `Sorgenti raw: 0`, today's date) if missing.
5. Create `log.md` if missing, with the first entry `## [YYYY-MM-DD] update | bootstrap struttura iniziale`. If it exists, append an entry instead (never rewrite history).
6. Verify every item by listing the root and re-reading `index.md` and `log.md`.
7. Report in one or two lines what was created and what already existed. Suggest the next step: put the first source in a dated folder in `raw/` and run `wiki-ingest` (the wiki is born from ingest and then lives on with `wiki-update`), or `wiki-check` to confirm state S4.

Do NOT ingest anything during init.

## States S3 and S4 — refuse

`⛔ wiki-init not available: state <S3|S4> (already initialized).` Suggest `wiki-check` (or `wiki-check err` in S3).
