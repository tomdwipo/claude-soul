# Gate/rate-limit on the signal you HAVE at decision time, not the one you only learn after the cost

**When this applies:** designing a rate-limit / quota / budget guard / circuit-breaker; choosing the limiting *unit* (count vs cost vs size); placing the check in a pipeline (pre-enqueue vs post-run).

**Principle:** a guard must decide using a signal that is **already certain at the decision point**. If the "true" signal (e.g. real cost) is only known **after** the work runs and the money is spent, gating on it is inherently laggy and leaky — the first round of abuse slips through before the number even appears. Pick a proxy that is **known upfront** (request count, input size) and block **before** the spend, even if the proxy is coarser. Timely-and-good-enough beats precise-but-late.

**Why:** imagine a guard meant to stop a single user draining a shared external-API budget. A "cost-based cap" looks the most precise — but the provider's cost is only known after the job finishes (the result size isn't certain upfront), so a cost cap can only lean on historical spend, and the first day of abuse still gets through. A "count-based cap" (requests today >= N) is known at enqueue time, so it blocks before any money burns, deterministically. Count wins not because it is more accurate, but because it is available at the right moment.

**How to apply:**
- Ask: "at the point where I decide block/allow, which number is already certain?" Gate on that.
- Put the check at the **cheapest point that still has the signal** — pre-enqueue / pre-spend if possible, so anything blocked leaves no downstream cost (external API, LLM, worker) at all.
- A coarse-but-timely proxy (count/size) beats a precise-but-late metric (post-run cost). Document the proxy and its trade-off.
- An expensive signal that only appears later is still useful for **observability/alerting** (per-job cost, a global budget stop) — as a **backstop**, not the primary per-request gate.
- Complements [[untrusted-text-into-prompt-is-injection-surface]] (deterministic guard at the boundary) and [[eval-engineering]] (measure a signal you can actually check).
