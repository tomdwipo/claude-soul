# Only "Selected for Development" enters the pipeline
**When this applies:** the auto-workflow picks up Jira tickets.
**Principle:** automation acts only on curated tickets — "To Do" / "Backlog" mean "later", not "start now".
**Why:** only deliberately-selected work should trigger automation; "To Do"/"Backlog" are intent-to-do-later, not now.
**How to apply:**
- JQL queries `status IN ('In Progress', 'Selected for Development')` only.
- Auto-transition targets `Selected for Development` Tasks only.
