# Account recovery anchors on a factor that SURVIVES the loss, and an abusable re-bind must be OBSERVABLE

**When this applies:** designing a recovery / re-bind / "switch device" path for an identity tied to a channel/device that can be lost (a chat account, a phone number, an authenticator, a session token); deciding "who is allowed to sever the old binding".

**Principle:** two things are often conflated:
1. **Anchor recovery on a factor that still exists when the other is lost.** If the premise of recovery is "the user lost X", the recovery path **must not** require X. Anchor on a surviving factor (e.g. email when the chat account is lost). A path that demands proof from the lost thing isn't recovery — it's a dead end dressed up as recovery.
2. **A destructive re-bind that's abusable if the anchor is compromised → make it OBSERVABLE, not silent.** Recovery that severs the old binding means: if the anchor (email) is hijacked, an attacker can take over. The mitigation isn't to block recovery (that locks out the legitimate user) but to **raise an alarm** to the party being harmed: notify the OLD channel (before it's severed) plus a second factor (email notice). A takeover becomes *visible* rather than silent. Order matters: alarm the old channel **before** unlinking (after unlink the old channel is unreachable).

**Why:** A user loses access to the channel their identity is bound to. The most-secure option ("re-link from the old channel") is impossible to use precisely because the old channel is gone — it fails requirement #1. The winning option re-binds via a token sent to the surviving factor (email), because email is the factor that survives. But that touches the "email compromised = takeover" attack surface → mitigation #2: send an alert to the old channel AND THEN clear the binding, plus an email notice that the binding changed. Not blocking (the legitimate user needs it), but making hijack visible. The existing single-binding guard is deliberately kept intact; the re-bind clears server-side first (defense in depth).

**How to apply:**
- Map every identity factor; ask "if this factor is lost, what does the recovery path require?" — ensure it doesn't require the factor just lost.
- For a destructive recovery path: alarm the **thing being replaced** (the old channel) plus another factor, **before** severing. Best-effort (degrade-safe) — a failed alarm shouldn't fail recovery, but at least one alarm must fire.
- Don't loosen an invariant (e.g. one-account-one-binding) for recovery's sake; do it as an explicit operation (clear-then-bind) so the guard stays a defense.
- An explicit confirmation ("this will sever the old one") guards against misuse.
- Complements [[consent-at-collection-recorded-not-hidden]] (anchoring email-as-identity) and security hardening (single-use codes, anti-takeover).
