# Wikifier

An [Agent Skill](https://code.claude.com/docs/en/skills) that builds and maintains a persistent, interlinked markdown wiki compiled by an LLM from immutable raw sources, following Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (raw sources / wiki / schema, plus `index.md` and `log.md`).

One skill, several commands. Before running anything, every command checks whether it can run in the wiki's current state (for example `wiki-audit` before `wiki-init` is refused with a clear error).

> **Status: early (v1.2).** Phase 1 is implemented. See [Status and limits](#status-and-limits) for exactly what has and has not been tested.

## Commands

Write them in natural language ("run wiki-check") or as an argument to the skill.

| Command | What it does | Status |
|---|---|---|
| `wiki-init` | Bootstraps the wiki. If `infowiki.md` is missing it drafts one and explains where to save it; it creates nothing in that case | implemented |
| `wiki-check` | Read-only self-diagnosis: config found? root reachable? structure complete? `index.md` aligned with the files? | implemented |
| `wiki-check err` | Runs the check, then proposes repairs and applies them only after your confirmation | implemented |
| `wiki-status` | Quick summary: pages, pending raw sources, last log entries | implemented |
| `wiki-ingest`, `wiki-query`, `wiki-update` | Content operations | planned |
| `wiki-merge`, `wiki-rename`, `wiki-delete`, `wiki-audit` | Maintenance and content audit | planned |

Planned commands answer "not implemented yet" and stop; they do not improvise.

### Self-diagnosis states

| State | Meaning |
|---|---|
| S0 | `infowiki.md` not found or incomplete |
| S1 | config valid, wiki root not reachable |
| S2 | root reachable, required structure incomplete |
| S3 | structure complete, `index.md` not aligned with the real files |
| S4 | healthy |

The matrix of which command is allowed in which state is in [`wikifier/references/preflight.md`](wikifier/references/preflight.md).

## Install

Download or clone this repository. The skill is the `wikifier/` folder (it must keep that name: it has to match the skill name).

### Claude Desktop / claude.ai

1. Download [`dist/wikifier.zip`](dist/wikifier.zip).
2. Open *Customize > Skills* (Italian UI: *Impostazioni > Competenze*), click **+**, choose **Upload a skill** and select the ZIP.
3. Code execution must be enabled for skills to work (per Anthropic's help center).

The ZIP contains the `wikifier/` folder as its root, with `SKILL.md` inside, as the uploader requires.

### Claude Code

macOS / Linux:

```bash
git clone https://github.com/GrossoRoberto/wikifier.git
cd wikifier
mkdir -p ~/.claude/skills
cp -r wikifier ~/.claude/skills/
```

Windows (PowerShell, not run by the author on Windows):

```powershell
git clone https://github.com/GrossoRoberto/wikifier.git
cd wikifier
New-Item -ItemType Directory -Force $HOME\.claude\skills | Out-Null
Copy-Item -Recurse .\wikifier $HOME\.claude\skills\
```

For a single project, use `.claude/skills/` inside the project instead. Invoke with `/wikifier check`, `/wikifier check err`, and so on.

### Pi

Copy the `wikifier/` folder into `~/.pi/agent/skills/` (or `~/.agents/skills/`) for all projects, or into `.pi/skills/` for one project, then run `/reload`. Invoke with `/skill:wikifier check`.

### Other agents

Any agent that follows the Agent Skills layout (a folder with `SKILL.md`, plus `references/`) should be able to load it. This is untested outside the three tools above.

## Configure: `infowiki.md`

Each wiki is identified by one small file, `infowiki.md`, that holds **only variables**. All procedures live in the skill.

```markdown
---
project_name: My Project
path: Z:\Wiki_Root\MyProject
path_alt:
domain: One-line description of what this wiki is about
language: it
confirmations: every-write
---
```

| Variable | Required | Notes |
|---|---|---|
| `project_name` | yes | Used in the titles of `index.md` and `log.md` |
| `path` | yes | Absolute wiki root: a drive-letter path (`Z:\...`) or UNC (`\\host\share\...`) |
| `path_alt` | no | Fallback root, used if `path` is unreachable |
| `domain` | yes | One line; guides category names |
| `language` | no (default `it`) | Language used with the user and in the wiki |
| `confirmations` | no (default `every-write`) | `every-write` or `session-ok` |

The skill looks for `infowiki.md` in, in order: the Project knowledge (Claude Desktop), a file attached to the chat, the directory the agent was launched from. It does not search elsewhere. If you don't have one yet, just run `wiki-init`: it interviews you and drafts it.

> Path rules, validation and edge cases: [`wikifier/references/infowiki-template.md`](wikifier/references/infowiki-template.md).

## Layout of the wiki it manages

Provisional profile, called "v2.1" (`wikifier/references/structure-v21.md`); it is expected to change after a design review. All layout knowledge is isolated in that one file.

```
<root>/
├── index.md   catalog of pages and raw sources
├── log.md     append-only chronological log
├── raw/       immutable sources
├── wiki/      pages written and maintained by the LLM (max 2 levels)
└── trash/     soft-delete bin
```

Rules enforced by the skill: `raw/` content is never modified; nothing is ever deleted (it is moved to `trash/`); the skill only operates inside the configured root.

## Status and limits

What was actually tested:

- Static checks of the skill (frontmatter, description length, links between files, line endings) and of the state definitions S0-S4 on synthetic wikis, with a reference checker written by the author. This validates the *definitions*, not the model's behaviour.
- One field test on Claude Desktop (a cloud session linked to a computer): activation from the description, S0 to draft to bootstrap to S4, `index.md`/`log.md` verified byte for byte. It led to the v1.1 fixes.

Not tested or not verified:

- `wiki-check err`, `wiki-status`, and the states S1 and S3 in the field.
- Pi: tool names, permissions, mapped network drives, and whether project skills are also found in parent directories (two sources disagreed).
- The Claude Desktop local Filesystem connector (the field test used a different toolset).
- Concurrent access from two machines to the same wiki: the rule is one session at a time.
- The PowerShell install commands above.

## Name

Other, unrelated projects use the name "Wikifier" (for example [IronAdamant/wikifier](https://github.com/IronAdamant/wikifier), a codebase documentation tool, and the academic "wikification" research line). This repository is independent of them.

## Credits

Inspired by Karpathy's [llm-wiki.md](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and by the command set of [kfchou/wiki-skills](https://github.com/kfchou/wiki-skills). The skill was written from scratch from their descriptions; no code was copied. Not affiliated with either.

## License

[MIT](LICENSE)

---

## Italiano (sintesi)

**Cos'è:** una skill che crea e mantiene una wiki markdown secondo il pattern "LLM Wiki" di Karpathy. Ogni comando controlla prima se può girare nello stato attuale della wiki (S0-S4) e altrimenti si ferma con un errore chiaro.

**Comandi disponibili (fase 1):** `wiki-init`, `wiki-check`, `wiki-check err`, `wiki-status`. Gli altri (`ingest`, `query`, `update`, `merge`, `rename`, `delete`, `audit`) sono pianificati e per ora rispondono "non implementato".

**Installazione:**
- **Claude Desktop:** scarica `dist/wikifier.zip` e caricalo da *Impostazioni > Competenze > + > Carica una skill*.
- **Claude Code:** copia l'intera cartella `wikifier/` (non solo il contenuto) in `~/.claude/skills/`. Uso: `/wikifier check`.
- **Pi:** copia la cartella `wikifier/` in `~/.pi/agent/skills/` ed esegui `/reload`. Uso: `/skill:wikifier check`.

**Configurazione:** un file `infowiki.md` con poche variabili (`project_name`, `path`, `path_alt`, `domain`, `language`, `confirmations`). Se non ce l'hai, lancia `wiki-init`: ti intervista e ne prepara una bozza.

**Limiti:** è una versione iniziale. Non sono ancora stati provati sul campo `wiki-check err`, `wiki-status`, gli stati S1 e S3, né l'uso su Pi. La struttura delle cartelle ("v2.1") è provvisoria.
