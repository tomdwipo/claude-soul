# Adapt an inherited command/template to the actual stack
**When this applies:** running an inherited command/template (a `/mini-prd`, `/breakdown-design`,
`/plan-first`, etc. that was authored for one stack) inside a sub-project on a *different* stack.
**Principle:** honor the template's *intent*, translate it to the current stack, and mark the parts
that genuinely don't apply as `N/A — <one-line reason>`. Don't force-fit idioms from the template's
origin stack where they don't belong, and don't silently drop sections (a reviewer can't tell
"considered & N/A" from "forgotten").
**Why:** a template carries hidden assumptions from the stack it was born in (build tool, logging lib,
test/screenshot framework, design tool, ticketing). Run it unmodified on a different stack and you get
boilerplate that doesn't fit — or invented scope (e.g. UI/screenshot sections for a headless backend).
The honest output translates each idea to the target stack and explicitly N/As the rest with reasons,
so the doc stays accurate and reviewable.
**How to apply:**
- Spot the template's stack assumptions before filling it; list what it silently expects.
- Translate intent → current stack: logging levels → your logging lib; before/after snippets → your
  language; the origin test framework → your test runner; UI sections → "no UI" if headless.
- Sections that don't apply → `N/A — <reason>`; never fabricate scope, never delete the heading silently.
- Pairs with [[name-conflicts-with-source-of-truth]] (verify before assuming).
