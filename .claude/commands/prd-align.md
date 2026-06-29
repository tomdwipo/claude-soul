# PRD Alignment Tracker

Analyze, sync, and track PRD/TRD alignment with codebase: $ARGUMENTS

## Instructions

### Step 0: Mode Detection

Determine which mode to run based on $ARGUMENTS:

**Rule 1 — CHECK mode:**
If $ARGUMENTS contains a Confluence URL, page ID, or feature name:
→ Go to Step 3 (CHECK mode)

**Rule 2 — SYNC mode (forced):**
If $ARGUMENTS contains `--sync`:
→ Go to Step 4 (SYNC mode)

**Rule 3 — STATUS mode (forced):**
If $ARGUMENTS contains `--status`:
→ Go to Step 5 (STATUS mode)

**Rule 4 — Auto-detect (no arguments):**
If $ARGUMENTS is empty:
1. Read `.docs/prd-registry/index.json`
2. Get `lastSyncCommit` value
3. Run `git rev-parse HEAD` to get current HEAD
4. If lastSyncCommit != HEAD → SYNC mode (Step 4)
5. If lastSyncCommit == HEAD → STATUS mode (Step 5)
6. If index.json doesn't exist → BOOTSTRAP (Step 1 first, then SYNC)

### Step 1: Bootstrap Registry (First Run Only)

Only run if `.docs/prd-registry/index.json` does not exist.

1. Create `.docs/prd-registry/` directory
2. Create `index.json` with empty entries and tree configs:
   - cloudId: "your-org.atlassian.net"
   - prdTrees: general (<page-id>), lending (<page-id>), cms (<page-id>)
   - trdTrees: lending (<page-id>), funding (<page-id>)
3. Create `module-map.json` with empty object
4. Crawl each tree using `mcp__atlassian__confluence_get_page_children`:
   - For each tree in prdTrees and trdTrees
   - Paginate if needed (limit: 50)
   - For each child page: create an entry with pageId, title, type (PRD/TRD based on tree), tree, parentId
   - Set status: "UNSCANNED"
5. Save all entries to `index.json`
6. Log: "Bootstrap complete. {N} PRD/TRD entries indexed. Run /prd-align --sync to scan codebase."
7. Proceed to SYNC mode (Step 4) automatically

### Step 2: Entity Extraction (Shared Helper)

For a given Confluence page, extract alignment entities:

1. Fetch page content using `mcp__atlassian__confluence_get_page` (includeBody: true)
2. Extract from content:
   - **Screen names**: Look for screen/page references (e.g., "Halaman KYC", "Upload Document Screen")
   - **API endpoints**: Look for URL patterns, endpoint mentions (e.g., `/api/v1/account-opening`, `POST /upload`)
   - **Data models**: Look for entity/model names (e.g., "UBO data", "beneficiary", "account type")
   - **Feature flags**: Look for remote config mentions (e.g., `SHOW_CMS_FEATURE`, `SHOW_LOAN_FEATURE`)
   - **Business rules**: Look for validation rules, conditions, limits
   - **Keywords**: Extract top 10 domain-specific nouns for fuzzy matching
3. Return extracted entities as structured data

### Step 3: CHECK Mode — New PRD Impact Analysis

**Input:** Confluence URL or feature name

#### 3a. Fetch the New PRD
- If URL: extract page ID, fetch with `mcp__atlassian__confluence_get_page`
- If feature name: search with `mcp__atlassian__confluence_search` (cql: `title ~ "{name}" AND space = "<SPACE>"`)
- Run Entity Extraction (Step 2) on the PRD content

#### 3b. Load Registry
- Read `.docs/prd-registry/index.json`
- Read `.docs/prd-registry/module-map.json`
- If registry is empty/missing → run Bootstrap (Step 1) first

#### 3c. Find Overlapping PRDs/TRDs
For each entry in registry where status != "DEPRECATED":
- Compare extracted keywords with entry keywords → score keyword overlap
- Compare extracted APIs with entry APIs → score API overlap
- Compare extracted screens with entry screens → score screen overlap
- Calculate total overlap score (weighted: API match = 3, screen match = 2, keyword match = 1)
- Sort by score descending
- Take top 15 entries with score > 0

#### 3d. Find Impacted Codebase Modules
Using extracted entities from the new PRD:
- Grep codebase for screen names, API endpoint paths, model class names
- Use module-map.json to find which PRDs already touch those modules
- Identify files that will likely need modification

#### 3e. Read Existing Confluence Alignment Comments
For top 5 overlapping PRDs:
- Use `mcp__atlassian__confluence_get_comments` to read comments
- Look for comments containing `PRD-ALIGN-DATA` marker
- Extract alignment date, status, and module info from structured data
- Compare alignment date with page lastUpdated and code lastChanged

#### 3f. Generate Gap Prediction
Based on overlaps, identify potential gaps:
- Shared modules that may have conflicting changes
- APIs that may need new fields/validation
- Screens that may need UI updates for both old and new PRD
- Feature flags that may interact
- Business rules that may conflict

#### 3g. Output Impact Analysis
Create file at `.docs/prd-registry/analysis/{feature-name}-impact.md` with:
- High-risk overlaps (shared code + stale alignment)
- Medium-risk overlaps (shared APIs/screens)
- Low-risk overlaps (same domain, minimal code overlap)
- Predicted feature gaps with specific file paths
- Impacted codebase modules with file counts
- Recommendations for which old PRDs to review before implementing

Format:
```markdown
# Impact Analysis: {PRD Title}
**Date:** {date}  **PRD:** {confluence link}

## High-Risk Overlaps
| Related PRD | Shared Modules | Alignment Date | Risk |
|---|---|---|---|

## Medium-Risk Overlaps
| Related PRD | Shared APIs/Screens | Notes |
|---|---|---|

## Predicted Feature Gaps
1. ...

## Codebase Modules Impacted
- `module/path` — N files
```

Keep analysis reports under 15000 characters.

#### 3h. Update Memory
Save key relationships to Claude memory for future conversations.

### Step 4: SYNC Mode — Update Alignment After Code Ships

#### 4a. Detect Changed Modules
1. Read `lastSyncCommit` from `.docs/prd-registry/index.json`
2. If empty (first sync): scan all modules
3. If set: run `git diff {lastSyncCommit}..HEAD --name-only` to get changed files
4. Group changed files by module (e.g., `feature-modules/feature_kyc/`, `core-data/`)
5. For each changed module, get the latest commit hash and date

#### 4b. Map Changes to PRDs/TRDs
For each changed module:
1. Read module-map.json to find associated PRDs/TRDs
2. If module not in module-map yet:
   - Grep module code for screen names, API calls, model classes
   - Search registry entries for matching entities
   - Add module → PRD/TRD mappings to module-map.json
3. Update `lastCodeChange` and `lastCodeChangeCommit` in module-map.json

#### 4c. Update Registry Entries
For each affected PRD/TRD entry:
- If alignment comment exists and code changed after alignment date → status = "DRIFTED"
- If no alignment comment exists → status = "UNSCANNED"
- Update entry's modules list if new module associations found

#### 4d. Update Confluence Alignment Comments
For each affected PRD/TRD (max 10 per sync to avoid spam):
1. Check if alignment comment already exists:
   - Use `mcp__atlassian__confluence_get_comments`
   - Look for comment with `PRD-ALIGN-DATA` marker
2. Build comment content:
   ```
   CODEBASE ALIGNMENT (auto-updated {date})
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Modules: {list of codebase modules}
   Related PRDs: {list of related PRD titles}
   Related TRDs: {list of related TRD titles}
   Status: {ACTIVE|STALE|DRIFTED}
   Last code change: {date} ({commit message summary})
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   <!-- PRD-ALIGN-DATA:{"v":"1.0","sync":"{date}","modules":[...],"related":[...],"status":"...","commit":"{hash}"} -->
   ```
3. Create new comment using `mcp__atlassian__confluence_add_comment`
4. Update entry's alignmentCommentId and alignmentDate

#### 4e. Run Doc Update Logic (Absorbed from /update-doc)
Execute the same logic as `/update-doc`:
1. For each changed module: update its README.md if needed
   - Ensure navigation section exists
   - Ensure endpoint section is documented
   - Keep consistent across all modules
2. Update CLAUDE.md memory references (link to READMEs, don't duplicate)
3. Update DEPRECATION_ANALYSIS.md if any deprecated patterns found
4. Update .docs/c4/ diagrams if architecture changed
5. Update DESIGN_SYSTEM_RULES.md if UI patterns changed
6. Keep all files under 39k characters

#### 4f. Save Sync Checkpoint
1. Update `lastSyncCommit` to current HEAD in index.json
2. Update `lastSyncDate` to current date
3. Save index.json and module-map.json

#### 4g. Update Claude Memory
Save/update memory entries:
- Updated PRD relationships
- New module → PRD mappings discovered
- Any deprecated entries found

#### 4h. Output Sync Summary
Print summary:
- N modules changed since last sync
- N PRD/TRD entries updated
- N Confluence comments added/updated
- N README files updated
- Any staleness warnings

### Step 5: STATUS Mode — Alignment Health Report

#### 5a. Load Registry
- Read index.json and module-map.json
- If registry empty → suggest running `/prd-align --sync` first

#### 5b. Calculate Staleness
For each entry in registry:
1. Get page lastUpdated from Confluence (batch using CQL search)
2. Get alignmentDate from entry
3. Get lastCodeChange for related modules from module-map.json
4. Apply staleness rules:
   - `ACTIVE`: alignmentDate > pageLastUpdated AND alignmentDate > lastCodeChange
   - `STALE`: pageLastUpdated > alignmentDate (PRD updated, alignment outdated)
   - `DRIFTED`: lastCodeChange > alignmentDate (code changed, alignment outdated)
   - `DEPRECATED`: no code references found in codebase AND last update > 12 months

#### 5c. Output Health Report
Print formatted report:

```
PRD/TRD ALIGNMENT HEALTH REPORT — {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTIVE:     {N} entries — code and docs aligned
STALE:      {N} entries — PRD updated, needs re-sync
DRIFTED:    {N} entries — code changed, alignment outdated
DEPRECATED: {N} entries — no code references, likely obsolete
UNSCANNED:  {N} entries — never analyzed

TOP 5 STALE (action needed):
  1. {Title} (PRD updated {date}, last aligned {date})

TOP 5 DRIFTED (code changed):
  1. {Title} (code changed {date}, last aligned {date})

DEPRECATED CANDIDATES:
  1. {Title} (no code refs, last updated {date})
```

### Step 6: Jira Integration (When Jira ID Provided)

If $ARGUMENTS contains a Jira ticket ID (e.g., PROJ-1234):
1. Use `mcp__atlassian__jira_get_issue` to fetch ticket details
2. Use `mcp__jira-attachment__list_attachments` to list all attachments
3. Use `mcp__jira-attachment__download_all_images` to download image attachments
4. Use `mcp__jira-attachment__download_all_videos` to download video attachments
5. If videos found: use `mcp__video-to-image__extract_frames_by_count` (count: 5) to extract key frames
6. Analyze images/frames for UI context
7. Use ticket's linked issues and epic to find related PRDs
8. Feed all context into CHECK mode analysis

## Guidelines

- Registry files (index.json, module-map.json) are gitignored — they're local tooling, not source code
- Analysis reports (.docs/prd-registry/analysis/*.md) ARE committed for team visibility
- Max 10 Confluence comments per sync run to avoid noise
- Always show detected mode at start of output: "[MODE: CHECK|SYNC|STATUS]"
- If bootstrap needed, inform user: "First run detected. Building registry..."
- Confluence comment format must include `PRD-ALIGN-DATA` marker for machine reading
- Keep analysis reports under 15000 characters
- When updating memory, reference README files instead of duplicating content
- Follow existing commit message conventions from CLAUDE.md
- Do not create files beyond what's specified (YAGNI)
- All /update-doc logic is now part of SYNC mode — /update-doc is superseded
