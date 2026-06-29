# Match the control mechanism to the model's disposition — instructions when cooperative, deterministic intercept when it resists

**When this applies:** you want to steer one model behavior (output language, format, tone, whether or not
it invokes a tool/skill) and you're deciding: put a deterministic gate outside the LLM, or just write a
prompt instruction the model interprets itself.

**Principle:** the control mechanism follows the model's **disposition** toward that behavior.
- Model is **cooperative** (does what it's asked) → **gate via a self-describing instruction** and let the
  model decide. Adding a separate deterministic detector is fragile when the signal you detect is **not**
  the signal that determines the outcome (e.g. detecting the *input* language to decide the *output*
  language — a request like "write the proposal in English" can be phrased in another language while asking
  for English output → the detector is wrong, the model is right).
- Model **resists** (has a contrary prior, refuses even when asked) → **intercept DETERMINISTICALLY before
  the LLM**; relying on the prompt is a coin-flip ([[intercept-deterministically-when-model-resists]]).

**Why:** an anti-slop session had a house-style locale hard-coded across every surface, so output in
another language got forced through one locale's register rules (a regression). The tempting "proper" fix
was to build a language detector plus per-language rulesets. But the fragile part wasn't the ruleset — it
was the **detection**: output language is decided by the model at generation time, and input language ≠
output language. The winning fix was **self-gating** — the rule block opens with "these rules apply ONLY
when the output is in language X; for any other language, write in that language and ignore this" — one
edit, the model becomes the decider, robust. The mirror case is the resist scenario: when the model refuses
a task it WAS asked to do, a deterministic intercept is mandatory; here the model is cooperative (ask for
English, it writes English), so the instruction is enough and a detector only invents problems.

**How to apply:**
- Ask first: **does the model comply with this when asked plainly?** Cooperative → instruction. Resists →
  deterministic. Don't default to "detection infrastructure" just because it looks more "proper."
- If you're about to build a detector, check: **is the signal you detect == the signal that determines the
  outcome?** If not (input-lang vs output-lang, text-length vs complexity, etc.), the detector is fragile —
  the model reading full context is more accurate.
- Self-gating beats pre-classification for cooperative behavior: an instruction block that states its own
  precondition closes every call-site at once, with zero infrastructure.
- **Active** de-slop/enforcement per variant (e.g. one language's ruleset) is separate work from the
  **variant decision**; defer the active part until volume justifies it, but the variant decision (via the
  model) can ship first.
