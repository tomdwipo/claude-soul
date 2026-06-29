# Already-done work → move to Code Review, don't fail
**When this applies:** context-gathering finds the work is already complete (PR exists, code committed).
**Principle:** detect completion and advance the ticket instead of retrying a no-op to failure.
**Why:** re-progressed complete tickets used to fail with "no prompt.md created" and waste 3 retry attempts.
**How to apply:**
- Mark `.done` locally, transition Jira to "Code Review", add a comment explaining why.
- Detect via keywords ("already completed", "PR exists", "all criteria passed") in context-result.json.
