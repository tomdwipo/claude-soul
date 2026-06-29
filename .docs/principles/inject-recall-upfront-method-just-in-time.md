# Front-load RECALL at session start; re-inject the METHOD just-in-time at the moment of use

**When this applies:** designing what a hook/preamble injects into an agent's context. You have two
different kinds of knowledge to surface: **recall** ("what is already known" — prior facts, indexes,
catalogs) and **method** ("how to perform an action" — a procedure invoked at a specific later moment,
e.g. how-to-learn at commit time, a release checklist at cut time). The instinct is to dump both at
session start "so it's all there."

**Principle:** place injected knowledge where its **attention weight peaks at the moment it's needed**.
- **Recall** is needed *throughout* and especially *early* (so you don't re-discover) → **front-load at
  SessionStart**.
- **Method** is needed at a *specific later trigger* (usually the END of a session — commit, cut, handoff)
  → **re-inject just-in-time at that trigger**, fresh at the bottom of context, so it lands at full
  attention. Front-loading method is the *least* reliable placement: in a long session the top of context
  is the most attention-diluted (and most compaction-prone) exactly when the end-of-session method fires.

**Why:** the model reads the whole window but weights **recent/bottom** content higher; top-of-context
guidance fades as the session grows. A method injected only at session start can be present-but-dim right
when it matters. We hit this making `how-to-learn` available for harvest-before-commit: front-loading the
full engine at SessionStart helps short sessions but dilutes in long ones; the fix that actually *solves*
it is re-injecting the engine on commit/learn intent (UserPromptSubmit) and at the real `git commit`
(PreToolUse) — fresh, bottom, full weight. Belt-and-suspenders: front-load the *trigger reminder* (cheap,
re-fired every turn so never dilutes) + re-inject the *full method* only at the capture moment.

**How to apply:**
- Split the injection by kind: index/recall → SessionStart; action-method → just-in-time hook on the trigger.
- A per-turn nudge (UserPromptSubmit) never dilutes — use it to keep the *trigger* salient; carry the heavy
  *method* only when intent is detected, not every turn (cost + noise).
- The capture/use moment is usually the session END — so that's where on-demand reads get skipped and a
  deterministic re-inject pays off most. Pairs with [[intercept-deterministically-when-model-resists]]
  (gate + inject at the trigger) and [[learnings-before-commit]] (the discipline being supported). The
  **recall** half is the placement-strategy behind [[catalog-lookup-every-first]] (front-loaded index =
  why "look up first" actually happens).
- Don't conflate "it's in context" with "it's salient" — placement and recency decide salience.
