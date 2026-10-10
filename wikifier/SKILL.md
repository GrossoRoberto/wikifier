---
name: wikifier
description: Wiki skill (Karpathy LLM wiki). Commands: wiki-init, wiki-check, wiki-check err, wiki-status, wiki-ingest (raw/ sources), wiki-update (news from this chat), wiki-query, wiki-audit, wiki-delete.
---

# Wikifier

Builds and maintains a persistent, interlinked markdown wiki compiled by the LLM from immutable raw sources (Karpathy "LLM Wiki" pattern: raw sources / wiki / schema, with `index.md` and `log.md`).
This file is only the router. Procedures live in `references/` and are read on demand.

## How a wiki lives

A wiki is born from `wiki-ingest` (the first sources in `raw/`) and then lives on with `wiki-update` (what happens in the chats), further ingests of new sources, and `wiki-query`/`wiki-audit` to use and verify it. `wiki-init` creates the whole structure at once.

## Commands

The user writes commands in natural language ("wiki-check") or as a slash command with the command as argument: `/wikifier check err` in Claude Code, `/skill:wikifier check err` in Pi.

| Command | Purpose | Phase | Procedure |
|---|---|---|---|
| `wiki-init` | Bootstrap the wiki, or draft `infowiki.md` if missing | 1 | `references/cmd-init.md` |
| `wiki-check` | Read-only self-diagnosis | 1 | `references/cmd-check.md` |
| `wiki-check err` | Check, then propose and apply repairs (with confirmation) | 1 | `references/cmd-check-err.md` |
| `wiki-status` | Quick summary (pages, last operations, pending sources) | 1 | `references/cmd-status.md` |
| `wiki-ingest` | Turn one raw source into cited wiki pages (plan approved first) | 2 | `references/cmd-ingest.md` |
| `wiki-audit` | Read-only check of citations, uncited claims, contradictions | 3 | `references/cmd-audit.md` |
| `wiki-update` | Bring durable news from THIS chat into the wiki (plan approved first; saves a chat extract in `_wikifier/chat/`). Beta | 2 | `references/cmd-update.md` |
| `wiki-query` | Answer a question in the chat from the wiki only; writes nothing | 2 | `references/cmd-query.md` |
| `wiki-delete` | Soft-delete pages: move them into `trash/`, fix index and links (plan approved first) | 3 | `references/cmd-delete.md` |

`wiki-ingest` is only for folders already in `raw/`. Anything that happened in the chat goes through `wiki-update`, never through ingest.

Any other `wiki-*` command is not part of Wikifier (for example merge, rename): say so plainly and stop. Never improvise a procedure.

## Mandatory sequence for EVERY command

1. **Locate `infowiki.md`** — see `references/infowiki-template.md`. Sources, in order: (a) Project knowledge/context (Claude Desktop), (b) a file attached to the current chat, (c) the directory the agent was launched from (Claude Code, Pi, other agents). Use the first one found (if several exist, mention the others) and say which one you used. Look nowhere else.
2. **Resolve the wiki root** with `path`, then `path_alt`; verify access with the tools in `references/tools-map.md`. Never assume or guess a path (not from a selected folder, not by "fixing" a malformed value): validate it per `infowiki-template.md` and ask the user when it is missing or invalid.
3. **Run the preflight** in `references/preflight.md`: determine state S0–S4 and check that the command is allowed in that state.
4. If not allowed, stop with the standard error (format in `preflight.md`). Do not partially execute.
5. Read the command's procedure file and follow it.

## Hard rules

- **Sandbox:** operate only inside the resolved wiki root. Other folders, other wikis and the rest of the filesystem do not exist for you.
- **`raw/` is immutable:** never edit, move or delete anything inside it. Reading it is allowed and expected (ingest and audit read it). Creating the EMPTY `raw/` folder at bootstrap is required, not a violation.  No command writes there, with no exception (chat extracts go to `_wikifier/chat/`).
- **Confirmations:** follow `confirmations` from `infowiki.md` (`every-write` = ask before each write; `session-ok` = one confirmation per session, then proceed). If the variable is missing, use `every-write`. Exception: `wiki-ingest`, `wiki-update` and `wiki-delete` show a plan first (always, in both modes); once the user approves it, that approval covers every write listed in the plan (pages, index, log). Anything NOT in the plan still needs its own confirmation under `every-write`.
- **No stray files:** create nothing in the wiki root except `index.md`, `log.md`, `raw/`, `wiki/`, `trash/` and the system folder `_wikifier/` (created by `wiki-init`; `chat/` for chat extracts, `report/` for plans and reports the user explicitly asks to save). Plans, audits and notes are shown in the chat, never written as files unless asked.
- **No deletion:** the filesystem connector has none. "Delete" means soft-delete into `trash/` (a dated unique name). `trash/` is ignored by index, log, check and ingest.
- **Do not invent data.** If unsure, mark `> ❓ DA VERIFICARE` in the page or say you don't know.
- **One session at a time** on a wiki (it may be a shared network drive). Do not start parallel sessions on the same root.
- **File format:** UTF-8, LF line endings, no BOM.
- **Language:** talk to the user in the `language` variable (default `it`). Wiki content follows the same language; technical terms stay in the original language.
- After any write operation, re-read what you wrote to verify it. Log writes to `log.md` (see `references/structure-v21.md`).
- Keep a short session report in markdown when the user or project asks for one.

## Working inside a wiki chat

When a chat is working on this wiki (the skill is active, `infowiki.md` found), keep in mind from the start that the wiki must evolve with the conversation: important things that happen here belong in it. Do not write on your own. Instead, at natural milestones, suggest ONE line: "Questo mi sembra da registrare nella wiki: vuoi che faccia `wiki-update`?" Milestones: a decision is taken, a fact is established or corrected, the user is about to close, run a handoff, clear the context or switch task. Suggest at most once per milestone; if the user declines or ignores, do not repeat until a new milestone. Never suggest for small talk or minor steps. The user decides when the update runs.

## Current limits

- Wiki layout is provisionally the "v2.1" profile (`references/structure-v21.md`). It will be replaced after a dedicated design session; keep all layout knowledge in that file only.
- `scripts/verify_quotes.py` (stdlib Python) is an optional helper for ingest/audit where a shell exists (Claude Code, Pi). Without it, quotes are checked by reading. It proves a quote exists in the source, not that it supports the claim.

## Credits

Pattern: Andrej Karpathy, "LLM Wiki" (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Command set inspired by kfchou/wiki-skills (https://github.com/kfchou/wiki-skills). Independent implementation; no code copied.
