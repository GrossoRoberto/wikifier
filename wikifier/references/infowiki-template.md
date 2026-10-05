# infowiki.md — template and lookup rules

`infowiki.md` holds ONLY a few variables that identify one wiki. No procedures, no conventions: those live in the skill. One `infowiki.md` per project.

## Role

`infowiki.md` identifies ONE wiki: its name, where it is, what it is about, and two behaviour settings. It holds variables only. All procedures and conventions live in the skill. Keep one `infowiki.md` per wiki (one per Project, or one per launch directory).

## Where it lives

| Where you work | Put `infowiki.md` here | How the skill finds it |
|---|---|---|
| Claude Desktop, chat inside a Project | In the Project knowledge | It is injected into the chat context |
| Claude Desktop, chat outside a Project | Attach it to the chat (each new chat needs it) | It is in the chat context |
| Claude Code | In the directory where Claude Code is launched (its working directory) | Looked up there; parent directories are not searched |
| Pi and other agents | Same as Claude Code | Same |

- Search order when it exists in several places: Project knowledge, then chat attachment, then launch directory. Use the first one found, say which one, and mention the others.
- It is tolerated in the wiki root (index and check ignore it), including when the launch directory is the root. It must NOT be inside `raw/` or `wiki/`.
- Not found in any of these places: state S0 (see `preflight.md`). Do not scan the rest of the filesystem.
- The file is not inside the wiki by design: the skill needs it to know where the wiki is.
- Same wiki from several machines: keep the same file and put the other machine's path in `path_alt`.

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
