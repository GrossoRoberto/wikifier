# Wikifier

An [Agent Skill](https://code.claude.com/docs/en/skills) that builds and maintains a persistent, interlinked markdown wiki compiled by an LLM from immutable raw sources, following Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (raw sources / wiki / schema, plus `index.md` and `log.md`), with a command set inspired by [kfchou/wiki-skills](https://github.com/kfchou/wiki-skills). See [Credits](#credits).

One skill, several commands. Before running anything, every command checks whether it can run in the wiki's current state (for example `wiki-audit` before `wiki-init` is refused with a clear error).

> **Status: early (v1.9).** All commands were run in the field on **Claude Code** by the author, who reports they work (no detailed log is published). Claude Desktop beyond the first test, Pi and the Project-knowledge route are still unverified. See [Status and limits](#status-and-limits) for exactly what has and has not been tested.

## Commands

Write them in natural language ("run wiki-check") or as an argument to the skill.

| Command | What it does | Status |
|---|---|---|
| `wiki-init` | Bootstraps the wiki with its whole structure (`raw/`, `wiki/`, `trash/`, `_wikifier/chat/`, `_wikifier/report/`, `index.md`, `log.md`). If `infowiki.md` is missing it drafts one and explains where to save it; it creates nothing in that case | field-tested (Claude Code, Desktop) |
| `wiki-check` | Read-only self-diagnosis: config found? root reachable? structure complete? `index.md` aligned with the files? | field-tested (Claude Code, Desktop) |
| `wiki-check err` | Runs the check, then proposes repairs and applies them only after your confirmation | field-tested (Claude Code) |
| `wiki-status` | Quick summary: pages, pending raw sources, last log entries | field-tested (Claude Code) |
| `wiki-ingest` | One raw source into a source page plus cited wiki pages, with a backlink sweep (plan approved first) | field-tested (Claude Code) |
| `wiki-audit` | Read-only check of citations (incl. line locators), uncited claims, contradictions, lint suggestions | field-tested (Claude Code) |
| `wiki-delete` | Soft-delete pages into `trash/` (plan approved first) | field-tested (Claude Code) |
| `wiki-update` | Bring durable news from the current chat into the wiki (plan approved first; saves a verbatim chat extract in `_wikifier/chat/`). Chats also suggest it at milestones | **beta** (written, sandbox-tested only) |
| `wiki-query` | Answer a question in the chat from the wiki only; writes nothing | field-tested (Claude Code) |

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

### Role and location of `infowiki.md`

`infowiki.md` identifies **one** wiki and holds **only variables**; procedures live in the skill. Keep one per wiki. It is **not** stored inside the wiki, because the skill needs it to know where the wiki is.

| Where you work | Put `infowiki.md` here | How the skill finds it |
|---|---|---|
| Claude Desktop, chat **inside a Project** | In the **Project knowledge** | Injected into the chat context |
| Claude Desktop, chat **outside a Project** | **Attach it to the chat** (each new chat needs it) | It is in the chat context |
| Claude Code | In the **directory where you launch it** (working directory) | Looked up there; parent directories are not searched |
| Pi and other agents | Same as Claude Code | Same |

- If several copies exist, the order is: Project knowledge, chat attachment, launch directory. The first one found wins and the skill says which one it used.
- It is tolerated in the wiki root (ignored by index and check), but never inside `raw/` or `wiki/`.
- If it is not found, the state is S0 and the skill does not search anywhere else. Run `wiki-init` and it will interview you and draft the file.
- Same wiki from several machines? Keep the same file and put the other machine's path in `path_alt`.
- Field-tested so far: the chat-attachment route on Claude Desktop (phase 1 commands) and the launch-directory route on Claude Code (all commands, author's report). The Project knowledge route and Pi are written from the documentation but not yet tried.

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

## Folders the skill writes to

Besides `index.md`, `log.md` and `wiki/`, the skill may write to `trash/` (soft-deleted pages) and to the system folder `_wikifier/` (created, with `chat/` and `report/`, by `wiki-init` together with the rest of the structure; wikis made before v1.8 get it from `wiki-check err`): `chat/` for chat extracts made by `wiki-update`, `report/` only for plans or reports you explicitly ask to save. It never writes to `raw/` (immutable, no exceptions) and creates no other files in the wiki root: `wiki-check` flags any it finds.

## Making every chat aware of the wiki

The skill tells a chat to suggest `wiki-update` at milestones (decision taken, fact corrected, about to close or hand off), but a chat only knows this once the skill is active. To have it from the first message, add two lines to the Project instructions (Claude Desktop) or to `CLAUDE.md` (Claude Code):

```
This project has a wiki managed by the Wikifier skill. Content that happens in the chat goes into the wiki with `wiki-update` (never `wiki-ingest`, which is only for folders in raw/). At milestones, suggest `wiki-update` in one line; never write without the user's approval.
```

## Status and limits

What was actually tested:

- Static checks of the skill (frontmatter, description length, links between files, line endings) and of the state definitions S0-S4 on synthetic wikis, with a reference checker written by the author. This validates the *definitions*, not the model's behaviour.
- One field test on Claude Desktop (a cloud session linked to a computer): activation from the description, S0 to draft to bootstrap to S4, `index.md`/`log.md` verified byte for byte. It led to the v1.1 fixes.
- Field tests on Claude Code by the author after v1.6: all commands, reported working. A first Code run (v1.3) exposed the loose-files-in-`raw/` case and the too-many-confirmations issue, fixed in v1.4.
- `scripts/verify_quotes.py` (quote exists in the raw file) tested on a synthetic wiki with seeded errors (`tests/test_wikifier.py`, run `python tests/test_wikifier.py`). A field-test kit for ingest/audit is in `tests/field/`.

Not tested or not verified:

- All commands were run on Claude Code by the author, who reports they work; no detailed log is published here, and it is one tester on one setup. On Claude Desktop only the phase 1 commands were run. The script only proves a quote exists in the source, not that it supports the claim; that part is the model's judgment and is reported as such.
- A fix in v1.3: a `raw/` folder not yet listed in the index used to make the wiki state S3 and block ingest; it is now "pending ingest" and the state stays S4.
- Whether every state (S1, S3) was exercised individually in the field: not recorded.
- Pi: tool names, permissions, mapped network drives, and whether project skills are also found in parent directories (two sources disagreed).
- The Claude Desktop local Filesystem connector (the field test used a different toolset).
- Concurrent access from two machines to the same wiki: the rule is one session at a time.
- The PowerShell install commands above.

## Name

Other, unrelated projects use the name "Wikifier" (for example [IronAdamant/wikifier](https://github.com/IronAdamant/wikifier), a codebase documentation tool, and the academic "wikification" research line). This repository is independent of them.

## Credits

This project builds on two sources, and I am grateful to both:

1. **Andrej Karpathy, [llm-wiki.md](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)** (gist, April 2026). The pattern itself: three layers (immutable raw sources, an LLM-maintained wiki, a schema that tells the LLM how to behave), the operations ingest / query / lint, and the two special files `index.md` (content catalog) and `log.md` (chronological record).
2. **kfchou, [wiki-skills](https://github.com/kfchou/wiki-skills)** (MIT). A Claude Code plugin implementing the same pattern. It inspired the command set (`init`, `ingest`, `query`, `update`, `audit`, `merge`), the "ask before writing" behaviour, and the idea of a per-wiki configuration file that tells the skill where the wiki is (their `SCHEMA.md`; here it became `infowiki.md`).

A [comment by wy-cats](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f?permalink_comment_id=6362239#gistcomment-6362239) on Karpathy's gist points out that "pending ingest" is better computed from the files than kept as a flag. `wiki-status` follows the same idea (pending sources are the `raw/` folders not yet listed in `index.md`).

Specific to this project (not taken from either source): the self-diagnosis states S0-S4 with a command eligibility matrix, `wiki-check` / `wiki-check err` / `wiki-status`, the `infowiki.md` variables-only configuration, soft-delete to `trash/`, and the layout-agnostic structure profile.

The skill was written from scratch from these descriptions; no code was copied. This project is not affiliated with either author.

## License

[MIT](LICENSE)

---

## Italiano (sintesi)

**Cos'è:** una skill che crea e mantiene una wiki markdown secondo il pattern "LLM Wiki" di Karpathy. Ogni comando controlla prima se può girare nello stato attuale della wiki (S0-S4) e altrimenti si ferma con un errore chiaro.

**Comandi:** tutti provati sul campo dall'autore su Claude Code (funzionano, segnalazione dell'autore, senza log dettagliato). Su Claude Desktop sono stati provati solo i comandi di fase 1; Pi e la route Project knowledge non sono ancora verificati. Altri comandi non fanno parte di Wikifier.

**Installazione:**
- **Claude Desktop:** scarica `dist/wikifier.zip` e caricalo da *Impostazioni > Competenze > + > Carica una skill*.
- **Claude Code:** copia l'intera cartella `wikifier/` (non solo il contenuto) in `~/.claude/skills/`. Uso: `/wikifier check`.
- **Pi:** copia la cartella `wikifier/` in `~/.pi/agent/skills/` ed esegui `/reload`. Uso: `/skill:wikifier check`.

**Configurazione:** un file `infowiki.md` con poche variabili (`project_name`, `path`, `path_alt`, `domain`, `language`, `confirmations`). Identifica una sola wiki e non sta dentro la wiki. Se non ce l'hai, lancia `wiki-init`: ti intervista e ne prepara una bozza.

**Dove metterlo:**
- **Claude Desktop, chat in un Project:** nel Project knowledge.
- **Claude Desktop, chat fuori da un Project:** allegalo alla chat (a ogni nuova chat).
- **Claude Code e Pi:** nella cartella da cui lanci l'agente (non cerca nelle cartelle superiori).
- Se ne esistono più copie vale la prima in quest'ordine: Project knowledge, allegato, cartella di lancio.
- Provato sul campo finora: solo l'allegato in chat su Desktop.

**Limiti:** è una versione iniziale. Non sono ancora stati provati sul campo `wiki-check err`, `wiki-status`, gli stati S1 e S3, né l'uso su Pi. La struttura delle cartelle ("v2.1") è provvisoria.
