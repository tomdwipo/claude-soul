# A high-value trigger the model resists → intercept DETERMINISTICALLY, don't rely on the prompt
**When this applies:** an LLM agent that must TRIGGER an action/skill from a user message, but the model
**refuses/hesitates** because its training prior fights it (e.g. "I'm an AI, I can't browse/search/access
the internet/transact"). When that trigger is high-value and must be reliable.

**Principle:** if the model is **unreliable** at deciding to do something (its prior opposes it), **don't
keep strengthening the prompt** — that's a coin-flip. **Detect the intent deterministically (regex/classifier)
BEFORE the LLM, then FORCE the flow** (scripted reply + enqueue), bypassing the model's decision. Prompting
is still fine for skills the model is cooperative about (the majority); intercept only the ones it resists.

**Why:** a capability can be fully live and verified end-to-end, yet the chat model **refuses the request
most of the time** because the prior ("an AI can't do that") is too strong. Every prompt tactic can fail to
be reliable — assertive wording, few-shot, anti-stale, authority-over-memory — and a few-shot *negative*
example can even **prime** the model to mimic the refusal phrase. What works: a deterministic intent regex
before the LLM → step-1 scripted opener (ask for the needed slots), step-2 (user's answer) → emit the
enqueue marker directly. The eval goes from flaky to 100%, deterministically (not a lucky sample).
Cooperative skills stay on the LLM path.

**How to apply:**
- **Measure reliability on the REAL path first** (eval through the real turn entrypoint + context, not an assembled prompt) — that's what distinguishes "cooperative model" from "resistant model." Don't trust small/assembled samples (easily lucky).
- **Intercept = intent regex + scripted flow** (opener → collect slots → sentinel/enqueue). Mark the step across turns (e.g. a signature in the last output). Guard cancel ("never mind") → fall through to the LLM.
- **Be selective:** intercept only the skills that resist; leave the rest to the LLM (don't over-engineer everything).
- **Keep the prompt** (for hint/awareness) but it's NOT the trigger guarantee — the intercept is.
- Pairs with [[eval-engineering]] (real-path eval that exposes unreliability), [[derive-agent-capabilities-from-registry]], [[dont-expose-the-recipe]], [[inject-recall-upfront-method-just-in-time]] (re-inject the method at the same intercept point).
- **Eval-case:** trigger "high-value skill, model refuses/hesitates to do it" → correct = deterministic intercept + real-path eval at 100%; **wrong** = keep strengthening the prompt (coin-flip) / trust an assembled-prompt eval.

**Instance — harvest-before-commit:** the model reliably *skips* "harvest learnings before committing" when
busy — a discipline it under-weights under load. A prompt nudge alone is a coin-flip. The fix is a
deterministic **PreToolUse(Bash) gate** (`.claude/learn-gate.sh`) that blocks `git commit` until evidence
exists (a `.docs/{principles,common-issues}` file staged, OR a conscious per-session "no-lessons" marker),
injecting `how-to-learn` on block. The shell never decides *whether* there's a lesson — it forces the
decision to be *recorded*. Selective by design: it intercepts only the commit action, not every tool call.
Note: it matches the substring `git commit`, so it also fires on any Bash call that merely *contains* that
text (test harnesses, `grep`) — escape via the marker, or stage a learning to satisfy the evidence globally
for the session. Validate it like any intercept: feed real hook JSON through the script (see
`.claude/learn-hooks-eval.sh`), don't assert.
