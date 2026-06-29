# Production-to-Jira Command

Read Production Intelligence agent output, deduplicate findings against existing
Jira tickets, and create actionable Task tickets in Backlog with full field mapping.

This is a focused subset of `/quality-to-jira` that ONLY processes the production
data sink, used by `~/w production run` so every production scan (Tue + Fri) files
its own tickets — without depending on the Friday Quality Scan handoff.

Arguments: $ARGUMENTS

## Prerequisites

1. Check that `/tmp/auto-workflow/production/production-summary.json` exists.
   If it does NOT exist, stop and tell the user:
   "No production summary found. Run `~/w production run` first."

2. Read the `generated_at` field. If older than 24 hours, WARN:
   "Production summary is from {generated_at} (>24h old). Run `~/w production run` for fresh data?"
   Continue if running non-interactively.

## Step 1: Read Production Summary

Read `/tmp/auto-workflow/production/production-summary.json` — JSON with a `findings[]`
array. Each finding has at least: `title`, `severity`, `category`, `evidence`, plus
category-specific fields (e.g., `affected_users`, `event_count`, `version`, `screen`).

Production categories surfaced by the AI agent:
- **CRASH** — Crashlytics-derived crash issues (FATAL or NON_FATAL)
- **ANR** — Application Not Responding patterns
- **PERFORMANCE** — App start latency, slow screen traces, slow network calls
- **USER_FEEDBACK** — Play Console review themes
- **FUNNEL_DROP** — Registration / KYC / transaction funnel drop-offs
- **REMOTE_CONFIG** — Stale or deprecated Remote Config flags still shipped

If the AI agent emitted other categories (e.g., `INSTALL_CHURN`, `WAU_REGRESSION`),
map them to the closest match above (likely `FUNNEL_DROP` or `PERFORMANCE`); if
truly unmappable, treat as `USER_FEEDBACK` so it still files.

## Step 2: Group Findings Into Candidate Tickets

Each finding in `production-summary.json` is already grouped by the AI prompt
(one finding = one candidate ticket). Use these summary formats:

| Category | Group By | Ticket Summary Format |
|----------|----------|----------------------|
| CRASH | per crash issue | `fix: crash in {screenOrFile} affecting {N} users` (or AI-emitted title verbatim if more specific, e.g. `fix: FATAL Compose null-check on v1.39.1 (1 user)`) |
| ANR | per ANR pattern | `fix: ANR in {screenOrFile} ({anrRate}%)` |
| PERFORMANCE | per trace/screen | `fix: slow {screen} ({p95}ms)` or `fix: app start p95 {p95}ms on v{version}` |
| USER_FEEDBACK | per review theme | `fix: user complaint — {theme} ({N} reviews)` |
| FUNNEL_DROP | per funnel step | `fix: {funnelStep} drop-off ({dropPct}% loss)` |
| REMOTE_CONFIG | per stale-flag cluster | `chore: remove deprecated Remote Config flags ({N} keys)` |

For each candidate ticket, record:
- `category`: one of the 6 above
- `summary`: formatted summary string
- `severity`: HIGH/MEDIUM/LOW from the AI finding
- `evidence`: the AI-provided evidence text (file paths, event counts, versions)
- `dedupKey`: `"{category}::{primary_identifier}"` — for CRASH use issue_id or stack-frame; for FUNNEL use the funnel step name; for REMOTE_CONFIG use the flag-prefix

## Step 3: Deduplicate Against Jira

Search for existing production-scan + quality-scan tickets:

```
mcp__atlassian__jira_search:
  jql: project = <PROJECT_KEY> AND labels IN ("quality-scan", "production-scan") AND status NOT IN (Done, Closed)
  fields: "summary,status,labels,description,created"
  limit: 100
```

Paginate via `nextPageToken` if > 100 results.

### Dedup Logic

For each candidate:

1. **MATCH by label + keyword**: existing ticket matches if it has:
   - Category label (e.g. `crash` or `production-scan`) AND
   - Same screen/file/feature keyword in its summary

2. **Decision**:
   - **No match** → mark as **CREATE**
   - **Match, numbers unchanged** → mark as **SKIP** (already tracked)
   - **Match, numbers changed (event count, affected users, p95)** → mark as **UPDATE** (add comment with new numbers)

## Step 4: Auto-Classify Jira Fields

Use this static mapping table. Same fields as `/quality-to-jira` for consistency.

> `<id>` and `customfield_<...>` are placeholders — replace them with your own Jira instance's option/field IDs (the AN-code label on each row shows which option it maps to). Discover them once via the field/option metadata APIs and keep them in `~/.claude/workflow-config.yaml`.

| Finding Type | SP | Choose Appendix v3 IDs (multi-select) |
|---|---|---|
| CRASH (HIGH — >100 users OR FATAL ≥10 users) | 3 | `[{id: "<id>"}]` AN-2 High |
| CRASH (MEDIUM — 10-100 users) | 2 | `[{id: "<id>"}]` AN-1 Low |
| CRASH (LOW — <10 users) | 1 | `[{id: "<id>"}]` AN-1 Low |
| ANR | 3 | `[{id: "<id>"}, {id: "<id>"}]` AN-2 High + AN-10 |
| PERFORMANCE (app start) | 2 | `[{id: "<id>"}]` AN-9 Medium |
| PERFORMANCE (screen render) | 2 | `[{id: "<id>"}]` AN-9 Medium |
| USER_FEEDBACK | 2 | `[{id: "<id>"}]` AN-1 Low |
| FUNNEL_DROP | 2 | `[{id: "<id>"}]` AN-1 Low |
| REMOTE_CONFIG | 1 | `[{id: "<id>"}]` AN-1 Low |

### Fixed Fields (all tickets)
- Story Points Type (`customfield_<sp_type>`): `{id: "<id>"}` (SP Tech Debt)
- Story Point Type v2 (`customfield_<sp_type_v2>`): `{parent: {id: "<id>"}}` (Technical)
- **Assignee (top-level `assignee` kwarg)**: Resolve at runtime — use the `Read` tool to open `~/.claude/workflow-config.yaml`, take the value at `issue_tracker.assignee` (an email), and pass that string as the top-level `assignee` kwarg. This MUST equal the ticket's reporter (the API token owner). Do NOT hardcode an email — the framework is portable across deploys/operators. NEVER pass `assignee_account_id`, NEVER nest under `additional_fields`. VPS `mcp__atlassian__jira_create_issue` silently drops `assignee_account_id` → empty Assignee.
- Project: `<PROJECT_KEY>`
- Issue Type: `Task` (use `Bug` for CRASH HIGH severity)
- Content format: `markdown`
- **Choose Appendix v3 (`customfield_<appendix>`): REQUIRED — never empty.** Use the mapping table in Step 4 above; default to `[{id: "<id>"}]` (AN-1 Low) if no match.

### Scope filter (this product only)
Before creating any ticket, skip findings whose `service` / `endpoint` / `affected_files` / `host` belong to a **separate product line / out-of-scope service**. Define the out-of-scope patterns in `~/.claude/workflow-config.yaml` (e.g. `issue_tracker.scope_exclude: [<service>, <gateway>]`) and skip any finding whose fields match them — even if the production-summary.json includes such rows.

## Step 5: Create Jira Tickets

For each candidate marked as **CREATE**:

### 5a. Create the ticket

Use `mcp__atlassian__jira_create_issue` with:
- `projectKey`: `<PROJECT_KEY>`
- `issueTypeName`: `Task` (or `Bug` for CRASH HIGH)
- `summary`: from Step 2
- `assignee`: `<email from ~/.claude/workflow-config.yaml :: issue_tracker.assignee>` — top-level kwarg, NOT `assignee_account_id`, NOT nested under `additional_fields`
- `contentFormat`: `markdown`
- `description` (template — fill with actual data):

```
## Production Finding

**Category:** {category}
**Severity:** {severity}
**Source:** Production Intelligence Scan ({generated_at_or_today})
**Detection:** {Crashlytics BigQuery | Firebase Analytics BQ | Firebase Performance BQ | Play Console reviews | Remote Config inspection}

## Details

{evidence text from production-summary.json finding — verbatim, includes affected users / event counts / version / file paths}

## Suggested Fix

{Use the appropriate template below based on category}

## Acceptance Criteria

- [ ] Root cause identified and fix applied
- [ ] Crashlytics no longer reports this issue (or count drops to 0) in next scan
- [ ] No new related issues introduced
- [ ] (CRASH/ANR only) Reproduce locally before claiming fix

---
*Auto-generated by /production-to-jira from production scan {today}*
```

- `additional_fields`:
  - `customfield_<story_point_estimate>`: {SP value}
  - `customfield_<appendix>`: {Appendix array}
  - `customfield_<sp_type>`: `{id: "<id>"}`
  - `customfield_<sp_type_v2>`: `{parent: {id: "<id>"}}`
  - `labels`: `["production-scan", "{category-in-kebab-case}"]`
  - `priority`: `{name: "High"}` for HIGH severity, `{name: "Medium"}` for MEDIUM, `{name: "Low"}` for LOW

### Suggested Fix by Category

- **CRASH**: Investigate stack trace in Firebase Crashlytics console for issue `{issue_id}`. Common causes: lifecycle race, null-state in coroutine, missing API guard. Reproduce on `{version}` build then patch the offending site. Add Timber log + crash unit test before merging.
- **ANR**: Profile main-thread blocking with Android Studio CPU profiler. Move `{detected_pattern}` off main thread (Dispatchers.IO / WorkManager). Verify p99 ANR rate drops in next scan.
- **PERFORMANCE (app start)**: Trace cold-start with `adb shell am start -W`. Defer non-critical init from Application.onCreate to lazy initializers or App Startup library.
- **PERFORMANCE (screen render)**: Upload ProGuard/R8 mapping for `{version}` to deobfuscate trace `{trace_name}`. If trace is intentionally obfuscated, rename it. If render is genuinely slow, profile with Layout Inspector.
- **USER_FEEDBACK**: Triage review themes. If recurring complaint matches existing ticket, link as duplicate. Otherwise create reproduction steps + targeted fix.
- **FUNNEL_DROP**: Inspect Firebase Analytics for the funnel step. Drop > 30% indicates UX or technical blocker. Cross-reference Crashlytics for crashes at the same step.
- **REMOTE_CONFIG**: Audit each flag for actual usage in code. Delete unused keys from Firebase console + remove default values from `RemoteConfigDefaults.xml`. Bump app version after cleanup.

### 5b. Set Story Points UI field (HARD REQUIREMENT — verify, do NOT skip)

`customfield_<story_points_ui>` ("Story Points" UI column the board renders) is NOT on the
<PROJECT_KEY> project create screen, so the create call in 5a CANNOT set it. You MUST run a
follow-up `editJiraIssue` immediately after each create. This call must NOT be
collapsed into 5a, summarised away, or skipped because "the SP field is already
set on customfield_<story_point_estimate>" — those are TWO DIFFERENT FIELDS:

- `customfield_<story_point_estimate>` (Story point estimate) — API/system field, settable on create
- `customfield_<story_points_ui>` (Story Points UI) — board column field, requires post-create edit

For EVERY ticket created in 5a (without exception, even if the LLM thinks the
field is already populated), do BOTH steps below:

**Step 5b-i — set the field**

```
mcp__atlassian__jira_update_issue:
  issue_key: <key from 5a>
  fields: '{"customfield_<story_points_ui>": <SP value, same number passed to customfield_<story_point_estimate>>}'
```

**Step 5b-ii — verify and re-emit if null**

```
mcp__atlassian__jira_get_issue:
  issue_key: <key from 5a>
  fields: "customfield_<story_points_ui>,customfield_<story_point_estimate>"
```

If the response shows `customfield_<story_points_ui>` is null/missing, re-emit step 5b-i.
If it is still null after the second attempt, log a WARNING in the output
summary table (column "SP UI Set: NO — manual fix needed") so the operator
sees the gap. NEVER claim a ticket is "complete" with `customfield_<story_points_ui>` null
in your output table — Sprint Mover's capacity calc reads this field, not 10604.

### 5c. Processing order

1. CRASH (HIGH first, then MEDIUM, then LOW)
2. ANR
3. FUNNEL_DROP (revenue/conversion)
4. PERFORMANCE
5. USER_FEEDBACK
6. REMOTE_CONFIG (lowest priority)

## Step 6: Update Existing Tickets

For each candidate marked as **UPDATE**:

```
mcp__atlassian__jira_add_comment:
  issue_key: <matching ticket key>
  comment: |
    **Production Scan Update — {today}**

    | Metric | Previous | Current | Delta |
    |--------|----------|---------|-------|
    | {metric_name} | {old} | {new} | {diff} |

    {If worsened: "Issue is growing — consider re-prioritizing."}
    {If improved: "Partial improvement detected — keep going."}

    ---
    *Auto-updated by /production-to-jira*
```

## Step 7: Output Summary

```
## Production to Jira Results ({today})

| Action | Ticket | Category | SP |
|--------|--------|----------|----|
| CREATED | [<PROJECT_KEY>-XXXX](url) {summary} | {category} | {sp} |
| SKIPPED | <PROJECT_KEY>-XXXX (already exists, unchanged) | {category} | – |
| UPDATED | <PROJECT_KEY>-XXXX (numbers changed, comment added) | {category} | – |

**Totals:** {N} created ({total_sp} SP), {N} updated, {N} skipped

All new tickets are in Backlog. Move to "Selected for Development" when ready
for auto-workflow to pick them up.
```

If 0 findings: `"No actionable production findings. All clean!"`

## Tools

This command is invoked from `~/w` on VPS with the snake_case Atlassian MCP tools. Use **only** these names:

- `mcp__atlassian__jira_search`
- `mcp__atlassian__jira_create_issue`
- `mcp__atlassian__jira_update_issue`
- `mcp__atlassian__jira_add_comment`
- `mcp__atlassian__jira_get_issue`
- `mcp__atlassian__jira_get_field_options` — only if a field-id lookup fails at runtime
- `Read` — used to fetch the dynamic assignee email from `~/.claude/workflow-config.yaml`
- `Glob`, `Grep`

The Mac-style camelCase names (`createJiraIssue`, `editJiraIssue`, `searchJiraIssuesUsingJql`, `addCommentToJiraIssue`, `atlassianUserInfo`, etc.) DO NOT EXIST on the VPS server. `--strict-mcp-config` blocks fallback, so using a camelCase name yields a silent no-op.
