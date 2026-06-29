# Harvest learnings before any commit
**When this applies:** the user says "commit", "push", "commit all push", or any one-shot ship command.
**Principle:** capture the session's non-obvious learnings first, then commit — in the same response, without asking.
**Why:** learning should compound across sessions instead of being lost at merge — capture after each session, and don't ask first (standing rule).
**How to apply:**
- Scan the session for gotchas / surprising facts / validated judgment calls before `git add`.
- Default destination = team-shared (`.docs/`), not private memory.
- If there are genuinely no new learnings, say so in the commit summary.
- Do NOT ask permission — it is a standing rule.
