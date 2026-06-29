# Quality Publish to Confluence

You are publishing a weekly quality report to Confluence.

## Context

- Parent page ID: <parent-page-id> (Weekly Quality Reports)
- Space ID: <your-space-id>
- Cloud ID: your-org.atlassian.net
- Report source: build/reports/quality-report.md
- Summary source: build/reports/quality-summary.json

## Instructions

### 1. Read and validate the quality report

Read `build/reports/quality-report.md` and `build/reports/quality-summary.json` from the project directory.

If neither file exists, output:
```json
{"action":"quality-publish","result":"error","message":"No quality report found"}
```
and stop.

**CRITICAL validation:** Check that the report contains real data:
- Coverage must show modules (not "0/0 modules")
- APK size must be > 0
- If the report has empty/zero data, output:
```json
{"action":"quality-publish","result":"error","message":"Report contains incomplete data (0/0 coverage). Run quality-report.sh with full Gradle first."}
```
and stop. Do NOT publish incomplete reports — they will overwrite good data.

**Freshness guard (prevents silent overwrite of prior week):** Compare `quality-summary.json.date` to today's date. If the report is more than 1 day old (e.g. summary says `2026-04-17` but today is `2026-04-24`), the previous `quality-report.sh` run failed and left last week's files on disk. Output:
```json
{"action":"quality-publish","result":"error","message":"Stale report: summary.date={date}, today={today}. Previous quality-report.sh run failed — do not publish or it will overwrite the prior week's page."}
```
and stop. Do NOT compute week number from `summary.weekNumber` or from the report header when stale — you would silently overwrite the existing Week-N child page with re-stamped data.

### 2. Calculate week metadata

Using today's date:
- **Week number**: ISO week number (e.g., Week 15)
- **Date range**: Monday to Friday of the current week (e.g., "Apr 7-11, 2026")
- **Year**: Current year

### 3. Check for existing child page

Use `mcp__atlassian__confluence_get_page_children` on parent page <parent-page-id>.
If a child page title already contains "Week {N}" for the current week number AND year, you will update it instead of creating a new one.

### 4. Create (or update) child page

**Title format:** `Quality Report — Week {N} ({Mon date}-{Fri date}, {Year})`
Example: `Quality Report — Week 16 (Apr 14-18, 2026)`

**Body:** Use the FULL content of `build/reports/quality-report.md` as-is. Do NOT summarize, reformat, or simplify. The markdown file is already formatted correctly — publish it verbatim.

To create: use `mcp__atlassian__confluence_create_page` with:
- cloudId: your-org.atlassian.net
- spaceId: "<your-space-id>"
- parentId: "<parent-page-id>"
- title: (formatted as above)
- contentFormat: "markdown"
- body: (the FULL verbatim content of quality-report.md)

To update existing: use `mcp__atlassian__confluence_update_page` with the found pageId and same body.

> **Why Step 5 is strict:** The parent page is hand-curated (intro, reports table, optimization trends, measurement definitions, ops runbook). A previous markdown round-trip flattened fenced code blocks into `Defaultbash#…` artifacts. Section order and code fences are both load-bearing — treat this step as a surgical edit, not a rewrite.

### 5. Update parent page Reports table

Use `mcp__atlassian__confluence_get_page` to read parent page <parent-page-id> with `contentFormat: "markdown"`.

**CRITICAL — preservation contract:** You must preserve the ENTIRE parent page content exactly as-is. Only modify the Reports table. Do NOT reformat code blocks, links, or any other section.

**Section order (must remain in this exact order, top to bottom):**
1. `# Weekly Quality Reports` (title + intro blockquote)
2. `## Reports`                          ← the table you will edit
3. `## Optimization Priorities (from Week 15 baseline)`
4. `## What Gets Measured`
5. `## How to Run`
6. `## Auto-Create Jira Tickets from Report`
7. `## Output Files`
8. `## How to Publish`
9. Trailing italic footer line beginning with `_Started: Week 15 (Apr 8, 2026) | Script:_` followed by inline code `scripts/quality-report.sh`

Do NOT rename, merge, split, or reorder these sections. Do NOT remove the `---` horizontal rules that separate blocks.

**Fenced-code rules (regression guard):**
- Every ` ```bash ` block MUST stay wrapped in triple-backticks with the `bash` language tag.
- Do NOT flatten fenced code into a single line (this is what produced `Defaultbash#…` artifacts in past runs).
- Do NOT collapse inline comments (`# comment`) into the same line as the command above them.
- If the markdown you read has any such artifact already, FIX it while you are here (replace with a proper fenced `bash` block). Otherwise leave untouched.

Find the `## Reports` section. It contains a markdown table:

```
| Week | Date | Branch | Coverage | Lint | Play Policy | Link |
| --- | --- | --- | --- | --- | --- | --- |
| Week 15 | Apr 8, 2026 | regress | 12/12 pass | 0 errors | 0 errors, 292 warnings | [Report](...) |
```

If a row for "Week {N}" of the current year already exists, **replace that row** with updated data.
Otherwise, add a new row at the TOP of the table data (right after the header + separator rows).

Row data:
- Week: Week {N}
- Date: today's date (e.g., Apr 18, 2026)
- Branch: regress
- Coverage: extract "{passed}/{total} pass" from quality-summary.json (e.g., "12/12 pass")
- Lint: extract new error count (e.g., "0 errors")
- Play Policy: extract error + warning counts (e.g., "0 errors, 292 warnings")
- Link: `[Report](https://your-org.atlassian.net/wiki/spaces/<SPACE>/pages/{new_page_id})`

**Pre-flight verification (run BEFORE calling `confluence_update_page`):**

Check your new body string satisfies ALL of the following. If any fails, do NOT publish — output the error JSON below and stop.

1. Contains the line `# Weekly Quality Reports` exactly once.
2. Contains all 8 `##` section headers listed in the order contract above, in that order (use string-index comparison, not regex).
3. Contains at least two ` ```bash ` fenced blocks (How to Run + Auto-Create).
4. Does NOT contain the string `Defaultbash` or any variant of flattened-fence artifact.
5. The Reports table has: header row + separator row + at least one data row, and the FIRST data row is the week you just added/updated.
6. Body length is within ±20% of the original body length you read in (guards against accidental truncation).

If all checks pass, call `mcp__atlassian__confluence_update_page` with:
- `pageId`: <parent-page-id>
- `contentFormat`: "markdown"
- `versionMessage`: "Add Week {N} quality report"
- `body`: the full verified body

**IMPORTANT:** Send the FULL page body back — not just the changed section. The API replaces the entire page content.

If verification fails, output:

```json
{"action":"quality-publish","result":"error","message":"Parent page pre-flight failed: <which check>"}
```

and stop. Do NOT call `confluence_update_page`.

### 5b. Add Runtime Signals section to child page

If `/tmp/auto-workflow/production/production-summary.json` exists, append a "## Runtime Signals — dev/staging/prod" section to the child page body with:
- Findings where labels include `"runtime-signal"` grouped by environment
- Pre-release regressions (label `"pre-release-regression"`) highlighted at the top
- Week-over-week trend vs `/tmp/auto-workflow/production/previous-summary.json` if it exists

### 6. Output result

Output a single JSON line:
```json
{"action":"quality-publish","result":"ok","page_id":"{id}","title":"{title}","url":"{webUrl}"}
```
