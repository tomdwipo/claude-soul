# TRD Command (Phase 1: Pre-Implementation)

Generate a Technical Requirement Document for: $ARGUMENTS

This command produces a mobile-side TRD grounded in **PRD + Figma (decoded) + codebase + (optional) BE TRD + QA TRD**, following the 14-section structure proven across the 2026-05-25 batch (FDS V3 Biller / Account Opening Legality / HyperVerge POC).

## Instructions

### Step 1: Gather inputs

**Primary inputs**: PRD (Confluence) · Figma · existing codebase. **NOT Jira** (Jira is tracking, not requirements).

#### 1a. PRD — Confluence (source of truth)
- URL or page ID in `$ARGUMENTS` → `mcp__atlassian__getConfluencePage` (markdown contentFormat).
- Feature name only → `mcp__atlassian__searchConfluenceUsingCql` then fetch.
- Extract: requirements table, acceptance criteria, business rules, user flows, document/data tables, event-tracker spec, exact Indonesian copy.

#### 1b. Figma — drill the flow, don't guess
**Priority order:**
1. **Local `.fig` + fig-decode** — check `~/Downloads/*.fig` and `~/Downloads/fig-decoded/` (and `$TMPDIR/fig-decode-*` as fallback). If the file is available:
   - Re-decode to a **durable** output: `~/.claude/skills/fig-decode/decode.sh "<path>" --out=~/Downloads/fig-decoded/<name>` (per the gotchas catalog — `$TMPDIR` is wiped on reboot).
   - For files >150 MB use `NODE_OPTIONS="--max-old-space-size=6144"`.
   - Drill the node-id from the Figma URL via `~/.claude/skills/fig-decode/scripts/find_node.py <node-id> --out=<decoded-dir>`. URL form `12894-95543` and colon form `12894:95543` both work.
   - Extract child SECTION/FRAME names, decision-diamond text labels, connector labels (Yes/No/Already-Exist/Service-Error).
   - **Record re-drillable node IDs** in the TRD appendix for future maintenance.
2. **`mcp__figma__get_file_nodes`** as fallback when no local `.fig` exists.
3. **User-provided screenshot** as last resort.

#### 1c. BE TRD — only if explicitly supplied
- `--be-trd <url>` or BE TRD page id → fetch with `getConfluencePage`.
- If BE TRD is **empty stubs** (Enum/REST tables blank) — flag explicitly in §6 and write the **mobile-recommended proposal** as the BE contract (extend-first, see §6 pattern below).
- If no BE TRD link is given, search the Confluence space for `parent = <feature-PRD-parent>` and confirm with the user before proceeding.

#### 1d. QA TRD — fold into §9 if present
- `--qa-trd <url>` → fetch. Extract test-case range (e.g. `TC_FDS_001-056`), risk-band model, GAP-list. Align §9 with TC ranges per test class.

#### 1e. Jira (optional context, not a source)
- Ticket ID in `$ARGUMENTS` → `getJiraIssue` for summary/epic context. Attachments via `mcp__jira-attachment__*`; videos → `mcp__video-to-image__extract_frames_by_count`.

### Step 2: Analyze the codebase (ground-truth before writing)

1. Identify affected modules from the PRD context.
2. Read relevant module `README.md` files.
3. Grep across all modules for:
   - Existing entry points (ViewModels, Screens, Repositories, API services, DTOs)
   - Current navigation paths (Composable nav, Pages.* routes, BackHandler / popBackStack patterns)
   - Existing wire enums and DTO fields (for extend-first API proposal)
4. **Verify symbols exist** — grep before writing. Plan docs are intent, code is truth (see common-issues `doc-from-shipped-tree-not-plan`).
5. Map current → target with concrete file paths + line numbers in `§3.4 Affected Components`.

### Step 3: Generate TRD

Path: `.docs/trd/TRD-{Feature-Name}.md` — kebab-case feature name.

**Length policy:** Target ~25–30 KB. **If grounded content exceeds 30,000 characters, leave as is — do not truncate critical sections** (the cap is a guideline; concrete TRDs land 25–40 KB in practice. Trim verbosity, never substance — current/target ASCII flows, §6.5 end-to-end contract, and §14 ticket breakdown are load-bearing).

### Step 4: Publish to Confluence
After writing the local file, publish under the daily TD parent (`TD MOB YYYY-MM-DD`):
- `mcp__atlassian__createConfluencePage` with `cloudId=your-org.atlassian.net`, `spaceId=<your-space-id>` (your space), `parentId=<TD MOB page id>`, `contentFormat=markdown`.
- **Expect a cosmetic "exceeds maximum allowed tokens" error on large docs** — per `confluence-mcp-large-page-publish-gotchas.md`, the page IS created (grep the saved tool-result file for `"id":"..."` + `_links.webui`). Verify via `getConfluencePage` by id, NOT via search (search has ~1-minute index lag).

### Step 5: Commit + push
- Commit conventional: `docs(<feature-scope>): add <Feature> TRD — <one-line highlight>`.
- Author: `<your name>` `<you@example.com>`. No AI attribution.
- Push to current branch (default `regress` unless on an epic).

## TRD Template (14 sections — proven structure)

```markdown
# Technical Requirement Document (TRD)
## {Feature Name} — {one-line scope}

**Document Version:** 1.0
**Date:** {YYYY-MM-DD}
**Author:** Technical Team (Mobile)
**Status:** Draft
**Jira:** {ticket ID and link} or N/A (PRD-driven)
**Confluence (PRD):** [{title}]({url}) — {status/owner}
**Confluence (BE TRD):** {link or "⚠️ **Not authored** — proposal in §6"}
**Confluence (QA TRD):** {link or "N/A"}
**Figma:** [{file name}]({url}) — canvas `{NNNN:NNNN}` "{canvas name}"
- `{NODE_ID}` SECTION **{name}** ({one-line scope})

---

## 1. Executive Summary

### 1.1 Overview
{2-3 sentences — what + why}

### 1.2 Current Implementation (verified in code)
{Bullets with file:line refs from §3.4. Quote actual constants/enums. Call out what does NOT exist today.}

### 1.3 Target Implementation
{Numbered list — each item maps to one or more §3.4 components}

### 1.4 Business Justification
{Regulatory / UX / drop-off / cost / vendor-diversification etc.}

### 1.5 Scope Condition
{Rollout flag, cohort gating, KYC-only, etc.}

---

## 2. Scope

### 2.1 In Scope (Mobile)
{Bulleted, atomic}

### 2.2 Out of Scope
{Explicitly call out adjacent work that ISN'T this TRD}

---

## 3. Current Architecture Analysis

### 3.1 Current Flow — Codebase Today
{ASCII diagram with real file paths, real wire strings, real prod-lock behavior. Box-drawing OK in code fences — Confluence preserves alignment.}

### 3.2 Target Flow — Figma Expectation (node `NNNN:NNNN`)
{ASCII diagram with real decision-diamond TEXT from fig-decode. Label each path (yes/no/declined/in-review).}

### 3.3 (optional) Target Flow — Sub-scope variant
{e.g. a separate behavior path}

### 3.4 Affected Components
For each:
#### 3.4.N `{path/to/File.kt}` ({MODIFY|CREATE|DELETE})
Today: {snippet quoting actual code with `as?` / `BackHandler { popBackTo(N) }` etc.}
Target: {what changes}

---

## 4. Data Model
{Enums, request fields, validation rules, exact PRD spec values}
{Cross-reference §6.5–6.6 for where data comes from}

---

## 5. Screen Specifications
{Per screen: header/body/CTA, decoded from Figma. Quote Figma frame names and node IDs.}

---

## 6. API Contract — Proposed (extend FDS/existing first, new only as fallback)

> ⚠️ {If BE TRD missing}: BE TRD is an empty stub / not authored. This is the mobile-recommended contract.
> Priority: **extend the existing surface; add a new endpoint only where none fits.**

### 6.1 Existing surface today
{Table: Endpoint | Today's payload | Module — grounded in actual `*ApiService.kt` reads.}

### 6.2 Proposed changes — ✅ EXTEND · ♻️ REUSE · ➕ NEW
{Table: # | Need | Proposal | Type}

### 6.3 Request / response delta (proposed — mirrors existing DTOs)
```kotlin
// EXTEND {DtoName}
@SerializedName("...") val ...: ... = ...
```

### 6.4 Field Mapping (BE ↔ Mobile ↔ UI)
{Table mapping wire string → mobile enum → UI label}

### 6.5 Proposed BE contract — end-to-end (when BE TRD missing)
Legend: **✓exist** field already returned today (verified in DTO) · **➕add** BE must add · **♻️reuse** endpoint unchanged.
{Per endpoint: JSONC request/response with ✓/➕ annotation per field. Anchor on real DTO fields.}

### 6.6 End-to-end mobile coverage — every screen has a data source
{Table: Mobile step → Endpoint → Field mobile reads → BE need (✓exist / ➕add / ♻️reuse). Concludes with "Net BE work = N field-adds".}

---

## 7. File Structure
{Tree diagram of new/modified files organized by module — annotate MODIFY/CREATE per file}

---

## 8. State Management
```kotlin
data class {Feature}State(...)
sealed interface {Feature}Result { ... }
```
{State-flow narrative: initial → action → outcomes.}

---

## 9. Testing Requirements
Aligns with [QA TRD]({link}) — **{N} TC ({status})**: {TC range mapping per test class}.
- **Unit:** {test classes + coverage scope}
- **UI/Screenshot** (baseline PNG in same commit — repo rule): {test names with scenarios}
- **Hilt UI** (if applicable): {happy/sad path E2E}

---

## 10. Risk Assessment / Open Questions
{Table: Risk/Question | Impact | Mitigation — fold QA gaps if a QA TRD provided}

---

## 11. Implementation Checklist
{Organized by layer (Data/Domain · Presentation · Integration · Testing). Each item a checkbox.}

---

## 12. Success Metrics
{Table: Metric | Baseline | Target. For POCs include cohort ramp plan with parity guardrails.}

---

## 13. Dependencies
{Table: Dependency | Owner | Status (Shipped / In-repo / Pending / **Empty stub — blocker**)}

---

## 14. Proposed Tickets (Jira)

Per `/create-jira-task` convention — <PROJECT_KEY> project · `Task` · **Story Points** = `customfield_<story_points_ui>` · **Benchmark** = *Choose Appendix (v3)* (`customfield_<appendix>`, complexity AN- code) · status stays **Backlog** (not auto-transitioned). **These are proposals — not yet created.** {Reference V2/V3 analog if applicable.}

> ⚠️ **Gate:** {Which tickets are BE-blocked vs free to start in parallel}

### 14.1 Ticket breakdown
| # | Summary (conventional prefix) | Layer | SP | Benchmark — Appendix (v3) | {V2/V3 analog?} |
|---|---|---|---|---|---|
| T1 | `feat: ...` | Domain/Data/Presentation/Integration/Testing/Analytics | N | AN-X {Low/Medium/High} ({description}) | ... |
| | **Total** | | **N SP** | | |

### 14.2 Wave split (optional — for multi-wave features)
- **Wave A — {scope} (~N SP):** T1 · T2 · ... — *one-line "why this slot"*
- **Wave B — {scope} (~N SP):** ...

### 14.3 Dependency graph
```
T1 → T2 ─┬─▶ T3 → T4
         └─▶ T5
T6 ── independent
```

> **Benchmark sanity:** {comparison to V2 / similar shipped TRD for SP justification}

---

## Appendix — Decoded Figma reference (fig-decode)

Canvas `{NNNN:NNNN}` "{canvas name}" — **{N} sections**: {list with node IDs + frame counts + scope (target/reference/OOS)}.

{Key frames per section.}

**Re-drillable frame IDs (extracted {YYYY-MM-DD}):**
| Frame | Node ID |
|---|---|
| {Frame name} | `{NODE_ID}` |

Decoded output: `~/Downloads/fig-decoded/{name}/` ({stats: N nodes, N pages, file MB}). Re-drill: `find_node.py <node> --out=<dir>`.

---
*Generated mobile TRD from PRD + decoded Figma + codebase analysis{+ QA TRD if used}.*
```

## Guidelines

### Grounding rules (non-negotiable)
- **Read module READMEs** before writing the TRD.
- **Quote actual code** in §1.2 / §3.4 — include file paths + line numbers + the verbatim snippet (e.g. `BackHandler { navController.popBackTo(2) }` at `KycComposable.kt:67`).
- **Verify every symbol exists** before writing it as "modify". Plan docs and Confluence summaries are intent; the tree is truth (`doc-from-shipped-tree-not-plan`).
- **Decode Figma**, don't infer — drill the node-id and record the decoded section/frame names + decision-diamond text.

### §6 — Extend-first API proposal pattern
- If BE TRD exists with real contracts: lift them verbatim into §6.
- If BE TRD is missing/empty: write the **mobile-recommended contract** as §6.5–6.6:
  - List existing endpoints (§6.1) anchored on real `*ApiService.kt` reads.
  - Propose changes as **♻️ REUSE → ✅ EXTEND → ➕ NEW**, prioritising reuse.
  - Field-level JSONC per endpoint in §6.5 with ✓exist / ➕add legend.
  - §6.6 mobile-coverage table proves every screen has a data source.
  - Conclude with **"Net BE work = N field-adds"** as the headline.

### §14 — Proposed Tickets per `/create-jira-task` convention
- Atomic tickets, conventional prefix (`feat:` / `fix:` / `refactor:` / `test:` / `chore:` for spikes/devops).
- Story Points + AN-benchmark from Choose Appendix (v3) — AN-1/2/...etc with Low/Medium/High complexity. Reference `.claude/commands/create-jira-task.md` for the codes.
- Note V2/V3 analog when applicable for SP justification.
- Dependency graph as ASCII.
- Tickets stay in Backlog (per standing rule — `feedback_jira_status.md`).

### Confluence publish
- `mcp__atlassian__createConfluencePage` with `spaceId=<your-space-id>` (your space) and `parentId=<TD MOB <date>>`.
- Expect cosmetic token-cap error on docs >~30 KB → page IS created; verify via the saved tool-result file (grep `"id":"..."`).
- After publish, optionally update the TD MOB parent index with the new TRD link + SP total.

### Naming + character cap
- File: `.docs/trd/TRD-{Feature-Name}.md` (kebab-case).
- Char target ~25–30 KB. **Over-cap is acceptable** — `wc -c` informational only; do NOT truncate substance to chase the cap.
- Confluence storage HTML is ~1.5× the markdown source size — a 40 KB md ≈ 60 KB storage; that's fine for readability, only matters for response-echo cap.

### What ALWAYS goes in
- **§3.1 current ASCII flow + §3.2 target ASCII flow** — both with real symbols.
- **§6.5–6.6 end-to-end coverage** when BE TRD is missing.
- **§14 with AN-benchmarks** and a dependency graph.
- **Appendix re-drillable node IDs** when Figma was decoded.

### What does NOT go in
- Speculation about BE behavior without grounding ("the BE probably returns X" — instead say "OPEN — BE to confirm").
- Plan-doc text claiming work shipped when `grep` says otherwise.
- Screen specs inferred from low-resolution renders when the Figma frame is empty (call out the gap, see `figma-pixel-spec-needs-designer-tokens`).
