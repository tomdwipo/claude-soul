# Create Jira Task Command

Create a Jira task ticket in the <PROJECT_KEY> project for: $ARGUMENTS

## Instructions

1. Parse the arguments to extract:
   - **Summary**: Short task title (prefix with `fix:`, `feat:`, `refactor:`, `test:`, `docs:` as appropriate)
   - **Description**: Detailed description (if provided)
   - **Story Points**: Numeric value (default: 2 if not specified)
   - **Choose Appendix (v3)**: Benchmark IDs (if provided, e.g. "AN-1, AN-9")
   - **Sprint**: `active` (default — adds to the currently running sprint), `backlog` (skip sprint assignment), or an explicit sprint id

2. If arguments are unclear, ask the user for clarification before creating.

3. Create the ticket using the Jira MCP tools with these EXACT field mappings:

## Field Mapping (DO NOT SEARCH — use these directly)

| Field | API Field | Type | Required |
|-------|-----------|------|----------|
| Project | `<PROJECT_KEY>` | projectKey | Yes |
| Issue Type | `Task` | issueTypeName | Yes |
| Assignee | `<caller_account_id>` (runtime lookup via `mcp__atlassian__atlassianUserInfo` — never hardcode another engineer's id) | assignee_account_id | Yes |
| **Story Points** (UI) | `customfield_<story_points_ui>` | number | Yes |
| Story point estimate | `customfield_<story_point_estimate>` | number | Yes (same value as Story Points) |
| Choose Appendix (v3) | `customfield_<appendix>` | multi-select array of `{id}` | **Required (never empty)** — default `[{id: "<id>"}]` (AN-1 Low) if uncertain |
| Story Points Type | `customfield_<sp_type>` | select | Optional |
| Story Point Type (v2) | `customfield_<sp_type_v2>` | cascading select | Optional |
| **Sprint** | `customfield_<sprint>` | number (sprint id) | Optional — **note: the Sprint field id varies per Jira instance (often `_10010` / `_10020`); discover yours via the Active Sprint Discovery step below, do not assume** |

### Active Sprint Discovery (use when sprint:active is requested)

The active sprint id changes every ~2 weeks, so look it up at runtime:

1. Run `mcp__atlassian__searchJiraIssuesUsingJql` with `jql = "project = <PROJECT_KEY> AND sprint in openSprints()"`, `fields = ["*all"]`, `maxResults = 1` (VPS: `mcp__atlassian__jira_search`).
2. From the response, read `fields.customfield_<sprint>[0].id` — that's the active sprint id (an integer like `<sprint-id>`).
3. Pass that integer to `customfield_<sprint>` when assigning. The field accepts a single id (not an array) on edit.

Example active sprint payload shape:
```json
"customfield_<sprint>": [{"id": <sprint-id>, "name": "<active-sprint-name>", "state": "active", "boardId": <board-id>}]
```

If multiple open sprints exist (rare — usually means a forgotten sprint), prefer the one whose `endDate` is closest to today.

### Choose Appendix (v3) — Common AN- Benchmark IDs

> Every `(id: <id>)` below is a placeholder for your own Jira instance's option ID — the AN-code + description is the portable framework; look up the real IDs once and substitute them.

**Low complexity:**
- AN-1 (id: <id>): Adjust single stand-alone logic function
- AN-2 (id: <id>): Create screen with max 5 static component (without integration)
- AN-3 (id: <id>): Create single usecase data layer (remote data source) to API calling
- AN-4 (id: <id>): Create single use case domain layer (usecase class) to data layer
- AN-5 (id: <id>): Reproduce legacy crash from crashlytics
- AN-6 (id: <id>): Event tracker in single screen
- AN-7 (id: <id>): Create UI state logic with max 5 states
- AN-8 (id: <id>): Integrate screens' navigation (max 3 screens)
- AN-9 (id: <id>): Refactor or add 1 generic function
- AN-10 (id: <id>): Refactor generic function unit test

**Medium complexity:**
- AN-1 (id: <id>): Create custom component (max 5 custom attribute)
- AN-2 (id: <id>): Create single screen with 1 recyclerview (max 3 component)
- AN-3 (id: <id>): Create generic style of a component
- AN-4 (id: <id>): Create a usecase from domain to data layer
- AN-5 (id: <id>): Create data source class unit test (max 3 function)
- AN-6 (id: <id>): Create repository unit test (max 3 function)
- AN-7 (id: <id>): Integrate 1 class for webview (without research)

**High complexity:**
- AN-1 (id: <id>): Create single screen with 1 recyclerview and components (max 3)
- AN-2 (id: <id>): Create single screen of form (max 5 input field and 1 button)
- AN-3 (id: <id>): Create custom component with logic and attributes (max 3)
- AN-4 (id: <id>): Research simple technology
- AN-5 (id: <id>): Research medium-big new technology (Medium complexity)
- AN-6 (id: <id>): Install new technology after research
- AN-7 (id: <id>): Create single screen with more than 1 dynamic view group

### Story Points Type Options (customfield_<sp_type>)
- SP Product (id: <id>)
- SP Tech Debt (id: <id>)

### Story Point Type (v2) Options (customfield_<sp_type_v2>)
- Product (id: <id>)
- Domain User (id: <id>)
- Technical (id: <id>)
- Meeting (id: <id>)
- Other (id: <id>)

## Creation Steps

1. **Resolve assignee** — call `mcp__atlassian__atlassianUserInfo` once and use the returned `account_id`. Never hardcode another engineer's id.

2. **Resolve active sprint** (skip if user passed `sprint:backlog` or an explicit id) — call `mcp__atlassian__searchJiraIssuesUsingJql` with the query in §Active Sprint Discovery and read `customfield_<sprint>[0].id`.

3. Use `mcp__atlassian__createJiraIssue` with:
   - `cloudId`: `your-org.atlassian.net`
   - `projectKey`: `<PROJECT_KEY>`
   - `issueTypeName`: `Task`
   - `summary`: parsed from arguments
   - `assignee_account_id`: from step 1
   - `description`: parsed from arguments (use markdown contentFormat)
   - `contentFormat`: `markdown`
   - `additional_fields`: include `customfield_<story_points_ui>`, `customfield_<story_point_estimate>`, and `customfield_<appendix>` (required — never empty)

4. Then use `mcp__atlassian__editJiraIssue` to set:
   - `customfield_<story_points_ui>` (Story Points) — may not be available on the create screen.
   - `customfield_<sprint>` (Sprint) — pass the sprint id as a number (e.g. `<sprint-id>`), not an array. Skip this if user passed `sprint:backlog`.

5. Return the ticket URL and summary of fields set.

## VPS variant (snake_case)

This slash command is intended for local Mac use where the Atlassian MCP exposes camelCase tools (`createJiraIssue`, `editJiraIssue`, `atlassianUserInfo`, `assignee_account_id`). The same fields apply on VPS, but the **tool/param names differ**:

| Mac (camelCase) | VPS (snake_case) |
|---|---|
| `mcp__atlassian__createJiraIssue` | `mcp__atlassian__jira_create_issue` |
| `mcp__atlassian__editJiraIssue` | `mcp__atlassian__jira_update_issue` |
| `mcp__atlassian__getJiraIssue` | `mcp__atlassian__jira_get_issue` |
| `mcp__atlassian__searchJiraIssuesUsingJql` | `mcp__atlassian__jira_search` |
| `mcp__atlassian__addCommentToJiraIssue` | `mcp__atlassian__jira_add_comment` |
| `mcp__atlassian__atlassianUserInfo` | *(no equivalent)* — resolve assignee from `~/.claude/workflow-config.yaml :: issue_tracker.assignee` |
| top-level kwarg `assignee_account_id` | top-level kwarg **`assignee`** (string: email / displayName / accountId) |

The VPS API silently drops `assignee_account_id` (unknown kwarg) → empty Assignee on the ticket. Always use the table above when authoring agent prompts that run via `claude -p` on VPS.

## Example Usage

```
/create-jira-task fix: align RT/RW fields on KYC screen | sp:2 | appendix: AN-1(Low), AN-9(Low)
/create-jira-task feat: add balance validation to transfer | sp:3 | sprint:active
/create-jira-task refactor: extract common OTP module | sp:5 | appendix: AN-9(Low), AN-4(Medium) | sprint:backlog
/create-jira-task chore: bump Hilt to 2.59 | sp:1 | sprint:<sprint-id>
```

Default behaviour when `sprint:` is omitted: **add to the active sprint** (`sprint:active`).
Use `sprint:backlog` to leave it in the backlog.

## Output Format

After creating, display:
```
Ticket: <PROJECT_KEY>-XXXX (link)
Summary: ...
Story Points: X
Choose Appendix (v3): ...
Sprint: <sprint name> (id <N>) | or "Backlog (no sprint)"
Status: Backlog
```

> Note: status stays at **Backlog** even when added to an active sprint — sprint membership and workflow status are independent in this org's Jira. Only "Selected for Development" auto-enters the dev pipeline; do not auto-transition new tickets out of Backlog.
