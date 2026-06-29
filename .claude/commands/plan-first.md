# Feature Planning First Command

Think Hard and Give me a few options for a $ARGUMENTS,
starting with the simplest first. Don't code yet - just
outline the approach and ask me which direction to take.

**Investigate the codebase. Diagnose before prescribing.**
Before proposing options, read the relevant files, trace call sites, and confirm the actual current behavior. Never propose a fix based on assumptions — ground every option in what the code actually does today. State your diagnosis (root cause + evidence) before listing options.

add Philosophy behind with max 15 words.
add pros and cons.
add comparison matrix with other approaches.
add expectation cost token generation.
if from jira task get all information by using mcp atlassian, jira-attachment, video-to-image frame per second, include comments if have.
if have link jira get detail all description and all comments if any.
if the option can use the ascii diagram, do it.

## Ticket Reality Check (when chat includes a Jira link)

Before proposing options, verify whether the ticket's issue still applies to the current codebase:

1. **Reproduce the issue against the current code.** Read the relevant files / trace the code path described in the ticket and confirm whether the bug/gap is still present.
2. **Check for existing mitigation.** Search for any guard, feature flag, defensive code, or recent commit that already addresses the issue (use `git log`, grep, and the `.docs/common-issues/` catalog).
3. **Decide one of three outcomes:**
   - **Still broken, no mitigation** → proceed with the normal `/plan-first` flow (options, diagnosis, etc.) — the plan should include the fix.
   - **Already fixed or mitigated in the current codebase** → do NOT propose options. Instead:
     - State this finding in chat with evidence (file paths + line numbers + commit SHA if relevant).
     - Use `mcp__atlassian__transitionJiraIssue` to move the ticket to **Done** (or the equivalent closed state).
     - Use `mcp__atlassian__addCommentToJiraIssue` (with `contentFormat: "adf"`) to add a comment summarising what mitigates it, with file/line evidence.
   - **Partial mitigation** → call this out explicitly, then propose options only for the uncovered gap.

Never silently propose a fix for something the codebase already handles.

## Avoid Repeating Mistakes

Before planning, read the **Common Issues** section in CLAUDE.md for known gotchas.

If you encounter a new mistake during planning, add it to CLAUDE.md Common Issues section with:
- What went wrong
- How it was fixed

Keep it short. This helps future sessions not repeat the same mistake.
