# QA Alignment Command (Phase 3: QA Handoff)

Generate a standalone QA alignment analysis for: $ARGUMENTS

## Instructions

### Step 1: Gather QA & Dev Data

If $ARGUMENTS contains a Jira ticket ID (e.g., PROJ-1234):
1. Use `mcp__atlassian__getJiraIssue` to fetch the ticket details
2. Use `mcp__jira-attachment__list_attachments` to list all attachments
3. Use `mcp__jira-attachment__download_all_images` to download screenshots/mockups
4. Use `mcp__jira-attachment__download_all_videos` to download video attachments
5. If videos found, use `mcp__video-to-image__extract_frames_by_count` (count: 5) to extract key frames
6. Look for QA TRD Confluence link in ticket links/description — fetch with `mcp__atlassian__getConfluencePage`
7. Look for BE TRD Confluence link — fetch with `mcp__atlassian__getConfluencePage`
8. Look for PRD Confluence link — fetch with `mcp__atlassian__getConfluencePage`

### Step 2: Read Existing Documentation

1. Check if TRD exists at `.docs/trd/TRD-{Feature-Name}.md` — read it
2. Check if feature report exists at `.docs/feature-report/{feature-name}/` — read all files
3. Check if COMPLIANCE_MATRIX.md already exists — use as input for gap analysis
4. Read actual implemented code files to understand what was built

### Step 3: Analyze QA TRD Against Implementation

1. Map every QA test scenario to an implemented code path
2. Identify gaps: scenarios in QA TRD not covered by implementation
3. Identify gaps: implementation behaviors not covered by QA TRD
4. Cross-reference with PRD requirements
5. Assess automation feasibility for each gap

### Step 4: Generate QA Alignment Document

If feature report exists, update: `.docs/feature-report/{feature-name}/QA_ALIGNMENT.md`
Otherwise create standalone: `.docs/qa-alignment/QA-{Feature-Name}.md`

Max 10000 characters.

## QA Alignment Template

```markdown
# QA Alignment: {Feature Name}

## Reference Documents

| Document | Location | Status |
|----------|----------|--------|
| **PRD** | {Confluence link} | {Available|N/A} |
| **TRD (Dev)** | {TRD file path or Confluence link} | {Available|N/A} |
| **TRD (BE)** | {Confluence link} | {Available|N/A} |
| **TRD (QA)** | {Confluence link} | {Available|N/A} |
| **Feature Report** | {feature-report path} | {Available|N/A} |
| **Design** | {Figma link} | {Available|N/A} |
| **QA Engineer** | {name from QA TRD or TBD} |
| **Review Assessment** | {name or TBD} |
| **Analysis Date** | {current date YYYY-MM-DD} |

---

## 1. QA TRD Status

{Current status: Draft/In Review/Approved/Not Available}
{List sections marked "Will provide later" or incomplete}

---

## 2. QA Test Cases Mapping

### Automation Scenarios (New)

| # | Scenario | Type | Dev Coverage | Status |
|---|----------|------|-------------|--------|
| A1 | {scenario description} | {Happy path|Negative|Navigation|Validation|Edge case} | {Code path covered + file ref} | {Aligned|Gap|Partial} |

### Automation Scenarios (Updated Existing)

| # | File | Change | Impact |
|---|------|--------|--------|
| U1 | {test file name} | {what changed} | {affected scenarios} |

### New Step Definitions

| # | Step Definition | Mapped To |
|---|-----------------|-----------|
| S1 | {step definition text} | {Screen/Component it tests} |

### Manual Test Scenarios

| # | Scenario | Precondition | Expected Result | Automatable |
|---|----------|-------------|-----------------|-------------|
| M1 | {scenario} | {setup needed} | {what should happen} | {Yes|No|Partial} |

---

## 3. Gap Analysis

### Gaps: QA TRD Missing Coverage

| # | Gap | Severity | Implementation Reference | Suggested Test |
|---|-----|----------|------------------------|----------------|
| G1 | {what QA TRD doesn't cover but implementation has} | {Critical|High|Medium|Low} | {file:line or component} | {brief Gherkin scenario} |

### Gaps: Implementation Deviations from PRD

| # | PRD Requirement | Expected | Actual | Reason |
|---|----------------|----------|--------|--------|
| D1 | {requirement} | {what PRD says} | {what was implemented} | {why different — tech constraint, BE limitation, deferred} |

### Gaps: BE TRD vs Mobile Implementation

| # | Area | BE TRD Says | Mobile Does | Action Needed |
|---|------|------------|-------------|---------------|
| B1 | {area} | {BE contract} | {mobile implementation} | {Confirm with BE|Align|OK} |

---

## 4. Suggested Additional Test Scenarios

{Gherkin-style scenarios for each gap found. Number them matching gap IDs.}

### Scenario G1: {descriptive title}
```gherkin
Feature: {feature name}

  Scenario: {scenario title}
    Given {precondition}
    And {additional setup}
    When {user action}
    Then {expected outcome}
    And {additional verification}
```

---

## 5. Risk Areas for QA

| # | Area | Risk | Recommended Testing |
|---|------|------|-------------------|
| R1 | {component/flow} | {what could go wrong} | {type of testing needed} |

---

## 6. Environment & Data Requirements

| Requirement | Details | Owner |
|-------------|---------|-------|
| {test data needed} | {specifics} | {Mobile|BE|QA} |

---

## 7. Alignment Summary

| Metric | Count |
|--------|-------|
| Total QA Scenarios | {N} |
| Fully Aligned | {N} |
| Partial Alignment | {N} |
| Gaps Found | {N} |
| Suggested New Scenarios | {N} |
| **Alignment Score** | {percentage}% |

### Recommended Actions
1. {action item for QA team}
2. {action item for dev team}
3. {action item for BE team if applicable}
```

## Guidelines

- Be honest about gaps — the purpose is to catch issues BEFORE QA testing
- Always cross-reference three sources: PRD, Dev TRD/implementation, QA TRD
- Include actual file paths and line numbers for implementation references
- Write Gherkin scenarios that QA can directly use in their automation
- If QA TRD is not available, generate suggested test scenarios from the implementation
- If BE TRD is available, verify mobile implementation matches BE contracts
- Severity levels: Critical (blocks release), High (must fix before QA), Medium (should fix), Low (nice to have)
- The alignment score should reflect reality — 100% is rare and that's OK
- Focus on actionable gaps, not theoretical edge cases