# Healthcheck DOWN = unreachable / liveness-dead, NOT degraded / under-load

**When this applies:** wiring a dead-man's-switch or external healthcheck/uptime monitor, and deciding which conditions should flip its status to DOWN.

**Principle:** a DOWN signal from an external dead-man/healthcheck must mean **the service can't serve** (liveness dead / unreachable) — **not** "it's under pressure" (RAM/disk/budget tight). If you fold soft resource pressure into DOWN, you produce **false-DOWN**: the alarm fires while the service is actually healthy (just momentarily busy), and responders learn to ignore the channel -> when a REAL outage arrives, the alarm is noise they've already muted. Classify signals by **severity**:
- **SOFT** (resource/budget: high memory, disk full, budget near limit) -> notify a side-channel (chat/log), **healthcheck stays UP**. The service still runs.
- **HARD** (function broken: error-rate, delivery failure, dead worker, stuck job) -> **flag DOWN**.

**Why:** a healthcheck DOWN usually drives escalation (email/page/on-call). Escalation must be proportional to "something is dead", not "something is busy" — especially on a small box where resource spikes are *normal and momentary* (e.g. a heavy batch job passing through, then settling). A false-DOWN that immediately recovers (a flap) is the clearest tell that your threshold is flagging *load*, not *liveness*. The wrong severity costs more than a missing signal: an alarm that often lies is an alarm that gets ignored.

**How to apply:**
- Separate the **liveness** axis (can it serve at all?) from the **capacity/pressure** axis (how much headroom?). Both deserve observation, but only liveness may lower status to "DOWN".
- Still alert SOFT to a side-channel — don't swallow it (disk/budget running out matters), just don't escalate it to "service dead".
- Use a **deny-list** for the SOFT set, NOT an allow-list for HARD -> a new/unexpected signal defaults to **HARD** (fail-safe toward *still* flagging DOWN). See the deny-list nuance below.
- A flap (DOWN -> UP within 1-2 cycles) with no real damage is evidence your signal is on the wrong axis -> reclassify, don't raise the threshold (raising it just masks the real pressure).

**Deny-list nuance (bridge to [[scope-gate-needs-positive-definition-not-denylist]]).** That principle says deny-lists are bad for scope/safety-refusal because the unlisted item **passes** (permissive default = dangerous direction). Here a deny-list is the *right* choice because the unlisted default = **HARD/DOWN** = the *conservative/loud* direction. The rule: **a deny-list is safe when the default (unlisted item) falls on the fail-safe side; dangerous when the default is the permissive side.** Choose the list shape based on where "the thing you forgot to list" lands.

Complements [[gate-on-signal-available-at-decision-time]] (pick the right signal at the decision point) — this one is about mapping a signal to the right *severity/action*.
