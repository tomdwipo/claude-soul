# Push and PR Command

Execute the complete PR workflow: commit all changes, push to remote, create PR, and transition Jira ticket.

## Arguments Format
```
$ARGUMENTS = <target-branch> [ticket-id] [reviewers]
```

**Examples:**
- `/push-pr epic/PROJ-1234` - Auto-detect ticket from current branch
- `/push-pr epic/PROJ-1234 PROJ-1240` - Explicit ticket override
- `/push-pr epic/PROJ-1234 PROJ-1240 alice,bob` - With reviewers

## Workflow Steps

### Step 1: Parse Arguments
Extract from `$ARGUMENTS`:
- **target-branch** (required): The destination branch for PR (e.g., `epic/PROJ-1234`, `master`)
- **ticket-id** (optional): Jira ticket ID. If not provided, extract from current branch name (e.g., `task/PROJ-1240` → `PROJ-1240`)
- **reviewers** (optional): Comma-separated list of reviewer names

### Step 2: Git Status Check
Run `git status` to verify there are changes to commit. If no changes, skip to PR creation if branch has unpushed commits.

### Step 3: Commit All Changes
1. Run `git add -A` to stage all changes
2. Generate commit message based on:
   - Jira ticket ID
   - Summary of changed files
   - Use format: `feat(<module>): <description>`
3. Commit with a Conventional Commit message (no AI/tool attribution trailer)

### Step 4: Push to Remote
Run `git push -u origin <current-branch>` to push changes to remote.

### Step 5: Create Pull Request
Use Bitbucket MCP tool to create PR:
- **workspace**: `<your-workspace>`
- **repoSlug**: `<your-repo>`
- **sourceBranch**: Current branch
- **destinationBranch**: Target branch from arguments
- **title**: Same as the commit message
- **description**: Include Jira link, summary, and test plan

**Missing Figma references hook** — before composing the description, grep the
staged AC.md for a `### Figma Reference Notes` section. If present and it
contains any `⚠️` lines, copy them verbatim into the PR description under a
`## Missing Figma References` heading (place it BEFORE the test plan so the
reviewer sees it on first scroll). Each line names the screen, state, reason,
and Figma URL (when known) so the reviewer can open Figma directly. If the
section is empty or absent, omit the heading entirely — do not insert an
empty block.

### Step 6: Add Reviewers (if provided)
If reviewers argument is provided, note them for manual addition (Bitbucket API limitation).

### Step 7: Transition Jira Ticket
1. **First**, call `getTransitionsForJiraIssue` to get all available transitions for the ticket
2. **Search by name**: Find the transition where `name` equals "Code Review DEV" (case-insensitive)
3. **Extract the ID** from the found transition object
4. Execute transition using the dynamically found ID
5. If "Code Review DEV" transition not found, list available transitions and ask user

**Important**: Never hardcode transition IDs. Always look up by name since IDs may vary across projects.

### Step 8: Output Summary
Display:
- Commit hash
- PR URL
- Jira ticket URL with new status
- Reviewers to add (if any)

## Error Handling
- If no target branch provided: Show usage help
- If branch has no changes and no unpushed commits: Inform user
- If PR creation fails: Show error and manual PR link
- If Jira transition fails: Show error but don't fail entire workflow

## Smart Detection Rules
- Branch pattern `task/PROJ-XXXX` → Extract `PROJ-XXXX` as ticket
- Branch pattern `feature/PROJ-XXXX-*` → Extract `PROJ-XXXX` as ticket
- Branch pattern `bugfix/PROJ-XXXX-*` → Extract `PROJ-XXXX` as ticket
- If no pattern matches and no ticket provided: Ask user for ticket ID

## Jira Transition Reference

Common transition names (IDs may vary, always lookup dynamically):
| Name | Description |
|------|-------------|
| Backlog | Move to backlog |
| Selected for Development | Ready for dev work |
| In Progress | Currently being worked on |
| **Code Review DEV** | PR created, awaiting review |
| READY TO TEST (DEV) | Ready for QA testing on dev |
| Ready To Staging | Merged to staging branch |
| Ready to Test | Ready for QA on staging |
| Done | Completed |
| Release | Released to production |
| Blocked | Blocked by dependency |
| Declined | Rejected/cancelled |

**Lookup Example:**
```
1. getTransitionsForJiraIssue(cloudId, issueIdOrKey)
2. Find: transitions.find(t => t.name.toLowerCase() === "code review dev")
3. Use: transition.id
```
