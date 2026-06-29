# Surface the result, never the recipe — exposing the engine arms the "just DIY it" critique

**When this applies:** adding "evidence" to a product surface (API/tool output, marketing/landing copy,
even error messages) to defend a product's value.

**Principle:** show *what it produced* (output samples, usage count, version cadence) — never *how it's
built* (which model, the prompt, the pipeline, the internal steps). The build recipe is the moat. Worse
than leaking it: exposing the engine **strengthens** the skeptic's "I could just do this myself"
argument instead of disarming it.

**Why:** a skeptic's strongest attack on a thin wrapper is "this is just a prompt to model X — I'll do
it myself for free." If your evidence layer *reveals* model X (or the pipeline steps), you've handed them
the recipe and proven their point. If instead you show only the **result** (here's the output, it's
versioned, it's been used N times), the DIY argument has nothing to grab: they can see it works without
learning how to replicate it. The same move that defuses the critique also protects the secret.

**How to apply:** Before surfacing any field, ask "does this reveal *how it's made* or *that it works*?"
Surface the latter (samples, counts, version numbers, cost-to-you). Keep the former (model id, system
prompt, runtime, provider, internal step-by-step) **internal-only** — usable by operators, never returned
via the public surface. Lock it with a test asserting the secret field is **absent**, not just that safe
fields are present.

- **Applies to marketing/landing UI too, not just API fields.** Showing a use-case as a "step rail"
  pipeline (`topic → Q&A → outline → render`) to look transparent is *showing the machine* on your most
  public surface — it invites "I'll just DIY that" and bores users who only want the result. Reframe as
  **prompt → artifact** ("Make a deck on retention." → "📑 8-slide PDF, ready to present"): show the
  result, hide the engine. Internal *process/steps* are recipe too — don't display them as "features."

- **Same rule for ERRORS (security/recon).** A failed job that returns its raw error can leak internal
  infra to the caller — server paths, the exact command line. That arms an attacker (infra recon) and
  leaks the recipe via the error path. User-facing error = generic ("Sorry, that failed — try again");
  keep the detailed error (path/cmd/stack) **server-side only** (DB + logs, for the operator).

Related: [[eval-engineering]] (measure the result), [[calibrate-to-the-real-audience]].
