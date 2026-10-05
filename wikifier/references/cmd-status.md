# wiki-status

Read-only quick summary. Allowed in S3 and S4 (warn if S3). In S0–S2: error pointing to `wiki-check` / `wiki-check err`.

## Procedure

1. Run the preflight with the alignment check.
2. Gather (listings and reads only):
   - Total pages under `wiki/` and pages per category
   - Number of `raw/` folders, and which are **pending**: raw folders not listed under "Sorgenti raw indicizzate" in `index.md`
   - The last 3 entries of `log.md` (lines starting with `## [`)
   - Date of the last operation
3. Output, short and in the user's language:

```
<project_name> — state S<n>
Pages: N (category: n, ...)   Raw sources: N (pending: n)
Last operations: <3 lines from the log>
Attention: <index misaligned / pending sources / nothing>
```

Nothing is written, not even a log entry. Do not infer things the files do not show: if `log.md` is empty, say so.
