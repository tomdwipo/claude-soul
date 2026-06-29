# A limit-failure has two fixes — restrict the load or raise the capacity; that's the owner's call

**When this applies:** something dies at a limit (timeout, quota, cap, size bound) and you're about to
write the fix.

**Principle:** there are always two families of fix: **guard the gate** (reject/shrink the input so it
fits the limit) or **raise the ceiling** (scale the limit to the load, salvage partial results). Which
one is right is a *product* decision about who the system serves — not a technical default. Present both;
don't silently pick the guard because it's cheaper to build.

**Why:** engineer-instinct defaults to protecting the infrastructure (reject the big input → the timeout
never fires). But if the owner's actual use case *is* the heavy load, the guard "fixes" the error by
deleting the product's purpose. Example shape: a batch job times out on long inputs; the diagnosed fix is
a duration guard at submit time, but the owner's correction is the opposite — dynamic timeouts (budget ∝
load) + partial salvage, because long inputs are the point. Both plans are "correct" for the same
incident; only the owner knows which.

**How to apply:** When a failure is a limit-hit, before writing the plan ask (or surface): "is the input
wrong, or is the limit wrong?" Offer the guard AND the ceiling-raise with trade-offs (guard = cheap,
predictable, but caps the product; ceiling = serves heavy use, but needs a hard upper bound so a hang
can't lock the worker, plus salvage so partial work isn't wasted). If raising the ceiling: keep *some*
cap (unbounded = one hang locks everything — a worse failure mode than timeout), scale budgets to a
*measured* cost-driver (and remember a miscalibrated constant fails the SHORT inputs first), and salvage
whatever finished. Related: [[calibrate-to-the-real-audience]] (serve the actual user, not the test
signal), [[explore-before-acting]] (a diagnosis is not a mandate to pick the fix).
