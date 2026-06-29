# A feature only counts if it lands on the path prod actually runs

**When this applies:** behavior split across two code paths gated by a flag/env (e.g. mode A vs mode B,
v1 vs v2, feature-flag on/off, sync vs async) — and you're adding or changing behavior in one of them.

**Principle:** before putting a rule in a branch, confirm **which branch prod executes**, and keep
shared behavior in **one source** that both branches assemble from. A feature added to the branch prod
doesn't run is **dead in prod** — silently, because nothing errors. Two hand-maintained copies of the
"same" behavior **will** drift; the drift surfaces as "I changed it but nothing happened in prod."

**Why:** a system can have two implementations of the "same" behavior behind a flag — say a default
in-process path and a flagged alternate path. A new rule gets added to the default path, but **prod runs
with the flag on** → it uses the alternate path, which still has the old behavior. Result: the feature
looks done (code + tests pass) yet users in prod never see it. Fix = collapse both into one shared source
(a common core + a per-path tail, assembled by one function) so the shared rule can't live on only one side.

**The eval trap (pairs with [[eval-engineering]]):** the eval ran with the flag at its **default** while
prod ran the alternate. It was green because it tested the branch prod doesn't use. An eval that doesn't
reproduce prod's config validates the wrong thing. Either run the eval in prod's config, or assert the
**shared source** is identical across branches (a parity test that fails if the shared core diverges).

**How to apply:**
- Before editing one branch of a flag-gated split: grep the flag/env in prod (`.env`/systemd/config) to learn which branch is live. Don't assume the "main-looking" path is the one that runs.
- Factor shared behavior into a single constant/function both branches call; let each branch add only its genuinely-specific tail. Duplicated prose across branches is a drift bug waiting to happen.
- Make the eval/test run prod's flag value, or lock the shared source with a parity test that breaks on divergence — not just a behavioral test on the default branch.
- Pairs with [[validate-in-real-runtime-context]] (test as the thing actually runs) and [[derive-agent-capabilities-from-registry]] (one source of truth, not per-copy hardcode).
- **Same move across a different kind of multi-path system:** [[new-channel-must-replicate-reference-handler-contract]] — there the paths are *channels* reusing one engine; here they're *flag-branches*. Both: lift shared behavior into ONE module every path assembles from, or the paths silently diverge.
