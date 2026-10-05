# Tools map — how to do each operation

Use only what the current session actually offers. Check tool availability; do not assume the environment (each machine has different permissions and OS).

## Claude Desktop with the Filesystem connector

First action of any wiki session: `list_allowed_directories`. The wiki root must be inside one of the returned directories. If it is not, stop and tell the user which path to add to the connector's allowed directories.

| Operation | Tool | Notes |
|---|---|---|
| Read a file | `read_text_file` | Prefer over deprecated `read_file` |
| Read several | `read_multiple_files` | |
| List a folder | `list_directory` | Distinguishes files and folders |
| File metadata | `get_file_info` | |
| Create a folder | `create_directory` | Creates nested, idempotent |
| Create/overwrite a file | `write_file` | Overwrites silently: read first if the file may exist |
| Edit part of a file | `edit_file` | `oldText` must match exactly (spaces, case). Supports dry run |
| Append | `edit_file` or read-modify-write | No native append |
| Move/rename | `move_file` | Fails if the destination exists → use unique dated names |
| Delete | — | **Not available** → soft-delete to `trash/` |
| Copy a file into the sandbox for byte checks | `copy_file_user_to_claude` | Requires the drive-letter path form |

The Filesystem connector cannot run scripts. Some setups expose it under different names (for example a `remote-devices` prefix): match by function.

## Claude Code and other agents with a shell

Use the native Read / Write / Edit / Glob tools for wiki files. Deletion is technically possible but the rule stays: soft-delete to `trash/`, and never touch `raw/`. Optional helper scripts may be added in a later phase; never depend on them.

## Verification

- After every write, re-read the file (tool result alone is not proof).
- For byte-critical checks (LF, BOM, trailing newline) use an independent method (copy to sandbox and inspect bytes, or a hexdump).

## Cloud session linked to the user's computer (device bridge)

Seen in the field test of 2026-09-29. The session runs in a cloud workspace (working directory such as `/home/claude`) and reaches the user's files through bridge tools: `device_list_dir` (list), `device_stage_files` (bring a file into the workspace), `device_commit_files` (write files back), and `device_bash` when present.

- Match tools by function, not by name. Verify what is actually available before promising an operation.
- Empty folders may not be creatable: write a `.gitkeep` inside and tell the user.
- The device shell may not see mapped network drives (for example `Z:`): then `device_bash` is useless on the wiki and only file tools work. Everything must still work with file tools alone.
- Reported in that test (cause NOT verified): the Filesystem connector failed on every call with an `outputSchema` (JSON Schema draft-07) error. If this happens, use the bridge tools and tell the user.

## Pi (terminal agent)

Pi runs in the terminal with a working directory. Its tools run with the permissions of the Pi process, so deletion may be technically possible: the rules stay (soft-delete to `trash/`, never touch `raw/`).

- Built-in tool names and the behaviour on mapped network drives (for example `Z:`) are NOT verified in the docs read so far. Match tools by function and verify on first use.
- Invocation: `/skill:wikifier <command>`. After editing the skill during a session, run `/reload`.
- Install: copy the `wikifier/` folder into `~/.pi/agent/skills/` (or `~/.agents/skills/`) for all projects, or `.pi/skills/` / `.agents/skills/` for one project. Whether project skills are also found in parent directories is reported differently by two sources: verify.

## Known unknowns (verify on first use, do not assume)

- Behaviour under concurrent access from two machines (SMB locking): not tested. The one-session rule applies.
- Very large files: not tested.
