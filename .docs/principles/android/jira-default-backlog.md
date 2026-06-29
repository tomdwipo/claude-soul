# New Jira tickets stay in Backlog
**When this applies:** creating a Jira ticket.
**Principle:** leave new tickets in Backlog — status should reflect real work state, set by a human.
**Why:** auto-transitioning to In Progress misrepresents when work actually starts.
**How to apply:**
- After `createJiraIssue`, only `editJiraIssue` for Story Points.
- Skip `transitionJiraIssue` unless the user explicitly asks.
