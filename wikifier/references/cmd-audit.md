# wiki-audit

READ-ONLY check of the wiki's content against `raw/`. Allowed in S3/S4 (see `preflight.md`). Writes nothing, not even to `log.md`; the report is shown to the user (and saved only if they ask). Never say "verified" for something that needed judgment: use the statuses below.

## Scope

Ask (or take from the command): one page, one category, or all. For "all" on a large wiki, state the number of pages and citations first and get confirmation: the cost grows with them. Always say what was and was not covered.

## Phases

**A — Uncited claims (judgment).** Read each page. List factual statements with no footnote. Ignore headings, navigation and links. Report as `UNCITED` with page and the sentence.

**B — Citations.**
- Mechanical (the quote exists): if a shell is available, run `scripts/verify_quotes.py <root> [pages]`; otherwise open each cited raw file and look for the quote (whitespace differences ignored, nothing else). Statuses: `OK`, `NOT_FOUND`, `FILE_MISSING`, `UNSUPPORTED_TYPE` (e.g. PDF, image: read the source and judge), `MALFORMED`, `OUTSIDE_ROOT`.
- Judgment (the quote supports the claim): for each `OK` quote read the sentence it is attached to and decide: `SUPPORTED`, `OVERREACH` (claim says more than the quote), `UNRELATED`. For `[synthesis]` footnotes: `SYNTHESIS_SUPPORTED`, `SYNTHESIS_WEAK`, `SYNTHESIS_UNSUPPORTED`, judged on the listed sources.
- The script only proves the text exists. Say so in the report.

**C — Contradictions (judgment).** Within the scope, find statements about the same thing that disagree and are not already in a `CONTRADDIZIONE` block. Report as `POSSIBLE_CONTRADICTION` with both quotes/pages. Also list existing `CONTRADDIZIONE` and `DA VERIFICARE` blocks as open items.

## Report format

```
Audit <date> — scope: <pages/categories> — <n pages, n citations>
Mechanical: OK n | NOT_FOUND n | FILE_MISSING n | UNSUPPORTED_TYPE n | MALFORMED n
Judgment:   SUPPORTED n | OVERREACH n | UNRELATED n | synthesis ok/weak/unsupported n/n/n
Uncited claims: n | Possible contradictions: n | Open items: n
Not covered: <list>

<one section per problem: page, footnote, status, evidence>
```

Findings are proposals: this command never edits pages. Offer `wiki-update` (when available) or manual fixes. Do not claim the wiki is "correct": say which checks passed.
