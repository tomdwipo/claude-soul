# Calibrate to the target audience, not the loudest test signal

**When this applies:** about to redesign something (copy, UX, behavior) to fix a reaction you observed.

**Principle:** before you change X to satisfy a reaction, check whether the reactor *is* your target user
and whether the reaction is *representative*. A vivid, well-instrumented signal (your own account, a power
user, one loud complaint) is often the *least* representative of the people the product is actually for.
Don't de-tune the product for its real audience just to silence the signal you happen to see most.

**Why:** the most visible reaction is frequently an artifact of the test setup, not the audience. For
example, copy can get pulled toward "anti-skeptic / de-marketed" because a test prompt produced a
skeptical answer — but that skepticism came from *your own account-level critical-mode settings*, not from
the everyday non-expert the product targets. Optimizing for that one critical reader would make the copy
colder and more technical for everyone it's meant for.

**How to apply:** When one data point drives a change, ask two questions first: (1) *Is this reactor in my
target segment?* (2) *Is this reaction representative, or an artifact of how I tested (my settings, my
expertise, my edge case)?* If it's an artifact, treat it as one signal among many, not the spec. Separate
"a real user segment worth serving" from "the loudest thing in my console." Pairs with
[[dont-expose-the-recipe]] (claim ≤ evidence) and [[eval-engineering]] (measure across real users, not one anecdote).
