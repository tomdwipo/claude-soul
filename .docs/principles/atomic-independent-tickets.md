# Atomic AND independent tickets
**When this applies:** proposing a Jira breakdown for feature work.
**Principle:** each ticket is one reviewable change that ships standalone; lean toward more tickets, not fewer.
**Why:** a "single combined ticket" proposal got corrected — the preference is per-concern splits so each PR reviews solo and merges in any order.
**How to apply:**
- One logical change per ticket; compiles + passes tests on its own.
- Split by module when files do not cross-reference.
- If two truly cannot ship independently, they are one ticket.
- Don't over-split docs: 1 doc ticket per epic.
