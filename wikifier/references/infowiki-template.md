# infowiki.md — template and lookup rules

`infowiki.md` holds ONLY a few variables that identify one wiki. No procedures, no conventions: those live in the skill. One `infowiki.md` per project.

## Where it lives

- **Claude Desktop:** as a file in the Project knowledge (it is injected into context). Never inside `raw/` or `wiki/`.
- **A file attached to the current chat** is accepted too, if it is named `infowiki.md`. Say so when you use it.
- **Claude Code / Pi / other agents:** in the directory the agent was launched from (its working directory). Do not walk up to parent directories.
- If not found in these places: state S0 (see `preflight.md`). Do not search other folders.

Rule: the file must exist somewhere readable from the Project, the chat or the launch directory. Search those places actively before declaring S0. Being inside the wiki root is fine (tolerated, ignored by index and check), including when the launch directory is the root. Do not scan the rest of the filesystem (sandbox).

## Template

```markdown
---
project_name: <short project name>
path: <primary wiki root path, e.g. Z:\Wiki_Root\MyProject>
path_alt: <fallback root path, e.g. \\host\share\Wiki_Root\MyProject; may be empty>
domain: <one-line description of what this wiki is about>
language: it
confirmations: every-write
---
```

## Variables

| Key | Required | Values | Notes |
|---|---|---|---|
| `project_name` | yes | free text | Used in `index.md`/`log.md` titles |
| `path` | yes | absolute path | Wiki root. On Desktop it must be inside the connector's allowed directories |
| `path_alt` | no | absolute path | Tried when `path` is unreachable. Report which one was used |
| `domain` | yes | one line | Guides category names and ingest emphasis |
| `language` | no (default `it`) | ISO code | User-facing language and wiki language |
| `confirmations` | no (default `every-write`) | `every-write` \| `session-ok` | Write-confirmation policy |

Unknown keys: ignore and mention them in `wiki-check`.
A required key that is missing or empty makes the file "incomplete" (state S0).

## Path forms and validation

Valid forms only: a drive-letter path (`Z:\folder\sub`) or a UNC path (`\\host\share\folder`). Anything else is INVALID (for example `Server\\share\folder`).

- Never "correct" or reinterpret an invalid value on your own, and never fill a missing `path` from a folder the user selected or from the working directory. You may PROPOSE a candidate, but the user must confirm it.
- `path` missing or invalid → the file is incomplete (S0).
- `path_alt` invalid → warning in `wiki-check`, ask the user to fix it; if `path` works, carry on.
- A `path_alt` that was never reached is reported as "not verified", never as OK.
- Both forms may be valid for the same folder; some connector tools accept only the drive-letter form (see `tools-map.md`). If unsure, prefer the drive-letter form.

## Typos and corrections

Unknown keys are ignored and listed by `wiki-check`. In draft mode (`cmd-init.md`), when you correct an obvious typo in a key (for example `donain` → `domain`), list every correction you made so the user can see it.
