# Feature Report Command (Phase 2: Post-Implementation)

Generate a compliance feature report for: $ARGUMENTS

## Instructions

### Step 1: Gather PRD & Design Inputs

**Primary inputs** for feature reports are PRD (Confluence), Figma design, and actual implemented codebase — NOT Jira tickets.

#### 1a. PRD from Confluence (Primary Source of Truth)
If $ARGUMENTS contains a Confluence URL or page ID:
- Use `mcp__atlassian__getConfluencePage` to fetch PRD content
- Extract: requirements, acceptance criteria, business rules — this is what implementation is compared against

If $ARGUMENTS describes a feature name (no URL):
- Use `mcp__atlassian__searchConfluenceUsingCql` to search for the PRD in Confluence
- Fetch the matching page with `mcp__atlassian__getConfluencePage`

#### 1b. Figma Design
If $ARGUMENTS contains a Figma URL:
- Use `mcp__figma__get_file_nodes` to fetch design details

If user provides screenshot images directly:
- Analyze the screenshots for UI compliance verification

#### 1c. QA TRD
If $ARGUMENTS contains `--qa-trd` or a QA TRD Confluence URL:
- Fetch QA TRD from Confluence to enrich QA_ALIGNMENT.md
- Map QA test scenarios against implementation

#### 1d. Jira (Optional — for ticketing/tracking only)
If $ARGUMENTS contains a Jira ticket ID (e.g., PROJ-1234):
- Use `mcp__atlassian__getJiraIssue` to fetch ticket summary, epic, linked issues
- Use `mcp__jira-attachment__list_attachments` + `download_all_images` + `download_all_videos` for attachments
- If videos found, use `mcp__video-to-image__extract_frames_by_count` (count: 5) to extract key frames
- **Note:** Jira is used for tracking context and ticket references only, not as primary requirement source

### Step 2: Analyze Implemented Code

1. Read the existing TRD at `.docs/trd/TRD-{Feature-Name}.md` if it exists
2. Search codebase for all files mentioned in the TRD or related to the feature
3. Read actual implemented files to verify what was built
4. Compare implementation against PRD requirements from Confluence
5. Identify any gaps or deviations from the original spec

### Step 3: Generate Feature Report

Create directory at: `.docs/feature-report/{feature-name}/`
Create these files:

1. `README.md` — Main report
2. `COMPLIANCE_MATRIX.md` — Requirement-by-requirement mapping
3. `RESPONSIBILITY_SPLIT.md` — Mobile vs Backend ownership
4. `QA_ALIGNMENT.md` — QA TRD gap analysis (if QA TRD available)
5. `TICKETS.md` — Ticket breakdown with benchmarks

Use kebab-case for the feature directory name.

---

## File 1: README.md Template

```markdown
# {Feature Name} - Feature Report

## Status: {Complete|In Progress|Partial|Blocked}

| Attribute | Value |
|-----------|-------|
| **Epic** | {Epic name} |
| **Ticket** | {Jira ticket ID} |
| **Confluence (Dev)** | {PRD link} |
| **Confluence (QA TRD)** | {QA TRD link or "N/A"} |
| **Module** | {affected modules} |
| **Report Date** | {current date YYYY-MM-DD} |
| **Implementation Date** | {date or range} |
| **Reviewed By** | Mobile Team |

## Quick Summary
{1-2 sentences describing the feature}

### Change Overview

| Previous Behavior | Current Behavior |
|-------------------|-----------------|
| {before} | {after} |

### Affected Screens

| Screen | Flow | Type | Location |
|--------|------|------|----------|
| {ScreenName} | {flow} | {NEW|MODIFY|DELETE} | {file path} |

### New Components

| Component | Description | Location |
|-----------|-------------|----------|
| {Name} | {description} | {file path} |

## Technical Analysis

### Architecture Decision
{Why the chosen approach was used}

### Key Implementation Patterns
{Code snippets showing important patterns used}

## Files in This Report

| File | Description |
|------|-------------|
| [COMPLIANCE_MATRIX.md](./COMPLIANCE_MATRIX.md) | Requirement mapping |
| [RESPONSIBILITY_SPLIT.md](./RESPONSIBILITY_SPLIT.md) | Mobile vs Backend |
| [QA_ALIGNMENT.md](./QA_ALIGNMENT.md) | QA gap analysis |
| [TICKETS.md](./TICKETS.md) | Ticket breakdown |

## Implementation Progress

| # | Priority | Task | Tickets | Status |
|---|----------|------|---------|--------|
```

---

## File 2: COMPLIANCE_MATRIX.md Template

```markdown
# Compliance Matrix: {Feature Name}

## Requirement Reference
- **Document**: {PRD title}
- **Confluence (Dev)**: {link}
- **Confluence (QA TRD)**: {link or N/A}
- **Status**: {Complete|In Progress}
- **Analysis Date**: {current date}

---

## Requirements Mapping

### N. {Requirement Group}

| Aspect | Implementation | QA Coverage | Status |
|--------|---------------|-------------|--------|
| {requirement} | {how it's implemented + file ref} | {QA scenario ID or "Gap"} | {Done|Pending|Gap} |
```

---

## File 3: RESPONSIBILITY_SPLIT.md Template

```markdown
# Responsibility Split: Mobile vs Backend

## Overview
Clear ownership boundaries for the {Feature Name} feature.

---

## Mobile Responsibilities

### UI/Presentation
| Component | Description | Location |
|-----------|-------------|----------|
| {Screen/Component} | {what it does} | {file path} |

### Business Logic
| Responsibility | Description |
|----------------|-------------|
| {logic area} | {what mobile handles} |

---

## Backend Responsibilities

### API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| {path} | {GET/POST} | {what it does} |

### Data Processing
| Responsibility | Description |
|----------------|-------------|
| {area} | {what backend handles} |

---

## Shared Responsibilities

| Area | Mobile | Backend |
|------|--------|---------|
| {area} | {mobile role} | {backend role} |
```

---

## File 4: QA_ALIGNMENT.md Template

```markdown
# QA Alignment: {Feature Name}

## Reference Documents

| Document | Location |
|----------|----------|
| **TRD (Dev)** | {TRD path} |
| **TRD QA** | {Confluence link or N/A} |
| **Compliance Matrix** | `COMPLIANCE_MATRIX.md` |
| **Design** | {Figma link} |
| **QA Engineer** | {name or TBD} |
| **Analysis Date** | {current date} |

---

## 1. QA TRD Status
{Current status of QA TRD — Draft/Ready/N/A}

---

## 2. QA Test Cases from Confluence
{If QA TRD available: list automation and manual scenarios}

### Automation Scenarios
| # | Scenario | Type |
|---|----------|------|
| A1 | {scenario} | {Happy path|Negative|Navigation|Validation} |

---

## 3. Gap Analysis

### Gaps Identified
| # | Gap | Severity | Suggested Test |
|---|-----|----------|----------------|
| G1 | {what's missing} | {High|Medium|Low} | {suggested Gherkin scenario} |

---

## 4. Suggested Additional Test Scenarios

{Gherkin-style scenarios for gaps found}

### Scenario G1: {title}
Given {precondition}
When {action}
Then {expected result}
```

---

## File 5: TICKETS.md Template

```markdown
# Ticket Breakdown: {Feature Name}

## Overview
{Brief overview of ticket organization}

### Progress

| Ticket | Title | Jira | Status |
|--------|-------|------|--------|
| 1 | {title} | {PROJ-XXXX} | {Done|In Progress|Pending} |

---

## Ticket N: {Title}

**Summary:** {what to implement}
**Scope:**
- {bullet points}

**Files to Create/Modify:**
- {file paths}

**Acceptance Criteria:**
- [ ] {criterion}

**Benchmark Mapping:**
| Benchmark | Description | Justification |
|-----------|-------------|---------------|
| {Low|Medium|High} AN-N | {benchmark desc} | {why this benchmark} |
```

## Guidelines

- Read ALL implemented files before writing the report — report on actual code, not planned code
- Cross-reference every PRD requirement against actual implementation
- Mark gaps honestly (not everything has to be "Done")
- Include actual file paths from the codebase (not guessed paths)
- Include actual code snippets for key implementation patterns
- If QA TRD is not available, still generate QA_ALIGNMENT.md with suggested scenarios based on the implementation
- Use the benchmark IDs from `.docs/benchmark/benchmark.md` for TICKETS.md
- Max 8000 characters per file
