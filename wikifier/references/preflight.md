# Preflight — states and command eligibility

Run before every command. Goal: know the wiki state and refuse commands that cannot work in it.

## States

| State | Definition | How to test |
|---|---|---|
| **S0** | `infowiki.md` not found, or a required variable is missing/empty, or `path` is syntactically invalid (see `infowiki-template.md`) | Lookup per `infowiki-template.md` |
| **S1** | `infowiki.md` valid, but neither `path` nor `path_alt` exists / is reachable | List the directory (see `tools-map.md`) |
| **S2** | Root reachable, but the required structure is incomplete | Compare against `structure-v21.md` "Required items" |
| **S3** | Structure complete, but `index.md` is not aligned with the real files | Full alignment check (below) |
| **S4** | Healthy | All the above pass |

Evaluate in order S0 → S1 → S2 → S3 and stop at the first that applies.

## Cost control

- **Mini-check (every command):** infowiki lookup, root reachability, existence of the required items. About 2–4 listings/reads.
- **Alignment check (S3 vs S4):** run only for write commands, `wiki-check`, `wiki-check err`, `wiki-status`. Read commands (`query`, `audit`) skip it: if the mini-check passes they are treated as S4, with a note that the index freshness was not verified.

Alignment check: every `*.md` under `wiki/` appears in `index.md`, every link in `index.md` points to an existing file, and every folder in `raw/` is listed under "Sorgenti raw indicizzate" (see `structure-v21.md`). `trash/` is excluded everywhere.

## Eligibility matrix

| Command | S0 | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|
| `wiki-init` | draft mode* | allowed | allowed | refuse ("already initialized") | refuse ("already initialized") |
| `wiki-check` | error | report only (root unreachable) | allowed | allowed | allowed |
| `wiki-check err` | error | error → `wiki-init` | allowed | allowed | nothing to repair |
| `wiki-status` | error | error | error → `wiki-check err` | allowed (warn index) | allowed |
| read commands (`query`, `audit`) | error | error | error | allowed (warn index) | allowed |
| write commands (`ingest`, `update`, `merge`, `rename`, `delete`) | error | error | error | error → `wiki-check err` | allowed |

*Draft mode: no wiki is created; the skill proposes a filled `infowiki.md` (see `cmd-init.md`).

## Standard error format

```
⛔ <command> not available: state <Sx> (<short reason>).
Do this first: <command to run>.
```

Write it in the user's language. Example (it): `⛔ wiki-audit non eseguibile: stato S1 (root non raggiungibile). Prima: wiki-init.`

Never work around a refusal by partially executing the command.
