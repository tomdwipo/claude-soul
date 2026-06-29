# Before designing a "missing/deferred" feature, ground it in the existing code first — often most of it is already built via current flows; design the DELTA, don't re-invent

**When this applies:** about to build a feature that "looks like it doesn't exist yet" or was deferred ("Phase 2", "later", "not handled yet") — especially anything touching auth, identity, recovery, billing, or notifications, or anything that **may already have a partial pipeline**. The moment you enter a design/planning step for a feature like this.

**Principle:** **Verify how large the gap to the actual code really is before designing.** A mature system has often **already covered 80%** of a "new" feature through existing flows it reuses — what's genuinely missing is only a **thin delta** (frequently UX/discoverability/copy, not logic). If you design from the premise "this doesn't exist", you **re-invent** what already works (wasted effort, risk, duplication, drift). Map the full path in the code, mark what EXISTS vs what is GENUINELY missing, then design ONLY the delta. This is the feature-design side of detecting work that's already done, plus the spirit of a reality check before proposing a fix for something already handled.

**Why:** consider a planned "login/recovery for returning users on a new device", premised on "a user can't get back into their account on a new device, so we need a new login system". Grounding in the code reveals the verify step **already reuses by identity** (a known user gets their existing account token back, not a fresh one) and the session-link step already re-points the session. So the register -> verify -> claim chain **already** restores the account — what's missing is only **discoverability** (no visible "Sign in" entry point and copy). The feature shrinks from "a new auth system" to "one sub-link + one line of copy + one locking test", with zero new backend. Without grounding, a duplicate login flow would have been built for nothing.

**How to apply:**
- Before writing a "new/deferred" feature design: **trace the full flow in the code** (grep the relevant auth/identity/billing functions, read their return paths). Ask: "which part is GENUINELY absent vs just not surfaced/wired?"
- Write the finding explicitly in the design ("backend X already exists via Y; gap = Z"). Design **only the delta** (YAGNI).
- If it turns out to already work end-to-end -> **don't build a feature**; just add UX/copy/a locking test and tell the user (honest, frugal).
- **Write a regression-guard test** for the existing behavior you now depend on (e.g. reuse-by-identity) — so your delta doesn't silently break the foundation you're leaning on.
- Complements [[current-state-overrides-stale-memory]] (trust the disk/code, not assumptions in docs).
