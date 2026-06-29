# Probe the real contract before integrating — "popular/cheap" ≠ "works for your job on your tier"
**When this applies:** wiring a third-party dependency whose contract you don't control — a REST API,
scraper/actor, SDK, MCP tool, LLM-judge schema. When writing the payload/parser, or choosing a vendor/actor.

**Principle:** don't code to a contract **guessed from documentation**. Third-party integration contracts
drift and their docs are often incomplete. **Probe the real contract first** — fetch the actual input
schema + make ONE test call and inspect the real output keys — *before* writing a mapper on top. And when
choosing a dependency: **"popular" and "cheap" are not "works for your job on your access tier."** What
decides is (a) it actually returns data on the plan/tier you have, and (b) its working-shape matches what you need.

**Why:** guessing fields/vendors burns cycles and credits. Common shapes:
- A payload field guessed from a blog is wrong; the real name is in the input schema, not the docs.
- A **popular, highly-rated** actor returns `noResults`/demo data (needs a paid rental) while a less-famous pay-per-result one actually returns data. *Popular ≠ working.*
- The **cheapest** option takes URLs (scrape-by-URL) when you need keyword *search* → wrong work-shape; a pricier one actually does search. *Cheapest ≠ fit.*
- Real-world output is messy: a date field is a dict not a string, counts are nested under another key, keys are snake_case — a guessed mapper will miss.

**How to apply:**
- **Get the schema from the source, not a blog.** Many platforms expose an input/`OpenAPI`/`/schema` endpoint. Then **one test call** → inspect `list(item.keys())` before writing the mapper.
- **Choose dependencies by evidence, not reputation.** Validate: does it return data on my tier? Is its work-shape what I need (search vs URL-scrape vs profile)? See also [[vendor-external-skill-readonly]] (the OSS twin of this).
- **Mappers stay defensive + re-verify per new source.** Multi-key fallback, handle nested/dict, mark "VERIFY on first run."
- **Probing first is cheap, not wasteful.** One probe (or reading the schema) is far cheaper than a full run that fails silently + debugging. Read secret tokens from env when probing; **don't echo them**.
- **Eval-case (regression):** trigger "wiring a new actor/API" → correct = fetch input-schema + 1 probe → map from real keys; **wrong** = write payload+parser from memory/docs then full-run.
