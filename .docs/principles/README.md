# Principles Index

Judgment-and-taste guidance for working in this workspace. **Principles, not rules** —
they describe *how to think*, not a fixed *what to do*. Rules (deterministic, settled by a
build/test/lint result) live in [`.docs/common-issues/`](../common-issues/README.md) instead.

> **Principle vs rule:** if a compiler / test / lint / build result can settle it, it is a
> RULE → catalog. If it is a judgment call (when to ask, how concise, scope, tone, what
> "done" means), it is a PRINCIPLE → here. When unsure, write a principle (principle-over-rule default).

These are the durable source of truth, version-controlled so every device and session inherits
them. The distilled essence is mirrored into the **Operating Soul** block at the top of
[`CLAUDE.md`](../../CLAUDE.md) so it is in context every session.

## How to add or refine a principle
Run the engine: [`how-to-learn.md`](./how-to-learn.md) (7 steps). Never append a raw correction
verbatim — distil it to a transferable principle first.

## Active principles (workspace-wide, any project type)

| # | Principle | Detail |
|---|-----------|--------|
| 1 | Explore before acting — a "?" is "tell me more", not "do it" | [explore-before-acting.md](./explore-before-acting.md) |
| 2 | Harvest session learnings before any commit | [learnings-before-commit.md](./learnings-before-commit.md) |
| 3 | Lessons go to the shared catalog, not only personal memory | [lessons-to-catalog.md](./lessons-to-catalog.md) |
| 4 | Look up before answering — every first message | [catalog-lookup-every-first.md](./catalog-lookup-every-first.md) |
| 5 | Atomic AND independent commits/tickets | [atomic-independent-tickets.md](./atomic-independent-tickets.md) |
| 6 | Already-done work → advance it, don't retry to failure | [smart-detect-done.md](./smart-detect-done.md) |
| 7 | Measure the agent, don't just coach it (eval engineering) | [eval-engineering.md](./eval-engineering.md) |
| 8 | Verify a source-of-truth "conflict" is real (same dimension) before flagging it | [name-conflicts-with-source-of-truth.md](./name-conflicts-with-source-of-truth.md) |
| 9 | Adapt an inherited command/template to the actual stack; N/A the rest with a reason | [adapt-template-to-stack.md](./adapt-template-to-stack.md) |
| 10 | Validate integrations in the real runtime context (non-login service/container), not just interactively | [validate-in-real-runtime-context.md](./validate-in-real-runtime-context.md) |
| 11 | A schema change isn't done until its ERD matches the live DB (generate + verify, don't hand-trust) | [erd-tracks-schema-changes.md](./erd-tracks-schema-changes.md) |
| 12 | Surface the result, never the recipe — exposing the engine arms the "just DIY it" critique | [dont-expose-the-recipe.md](./dont-expose-the-recipe.md) |
| 13 | Calibrate to the target audience, not the loudest test signal | [calibrate-to-the-real-audience.md](./calibrate-to-the-real-audience.md) |
| 14 | Tolerate heterogeneous agent/MCP clients that coerce args — accept loose types, fallback, recovery tool | [tolerate-client-arg-coercion.md](./tolerate-client-arg-coercion.md) |
| 15 | A limit-failure has two fixes (guard the gate vs raise the ceiling) — which one is the owner's call | [limit-or-capacity-is-owner-call.md](./limit-or-capacity-is-owner-call.md) |
| 16 | Match the delegation level to the consumer — default LLM-facing interfaces to "Tell" (exact, copy-paste-ready) | [delegation-level-match-consumer.md](./delegation-level-match-consumer.md) |
| 17 | On-brand visual assets → reuse the existing deterministic render pipeline, not AI image-gen (exact font/color = one identity). Umbrella: reproduce identity-bearing artifacts deterministically (reuse exact source, never regenerate/redesign); animation case = [[recreate-live-animation-deterministically]] #33 | [reuse-brand-render-pipeline-not-ai-gen.md](./reuse-brand-render-pipeline-not-ai-gen.md) |
| 18 | Need a new capability → search + vendor read-only (review first), don't run the installer; gate = it sharpens the use-case output | [vendor-external-skill-readonly.md](./vendor-external-skill-readonly.md) |
| 19 | Discovery before prioritization — a funnel filters candidates, doesn't generate them; validate on behavior not stated intent; moat = pre-PMF tie-breaker | [discovery-before-prioritization.md](./discovery-before-prioritization.md) |
| 20 | Probe the real contract (input-schema + 1 test call) before integrating; "popular/cheap" ≠ "works for your job on your tier" | [probe-contract-before-integrating.md](./probe-contract-before-integrating.md) |
| 21 | Store the external response WHOLE (not mapped) when it feeds a moat/eval — what you drop can't return without paying again | [store-raw-complete-for-flywheel.md](./store-raw-complete-for-flywheel.md) |
| 22 | Search in the PRODUCER's language not the seeker's; unstructured = a source, your value = filter→extract→match | [search-in-producers-language.md](./search-in-producers-language.md) |
| 23 | Derive an agent's self-knowledge (what it can do) from the registry, don't hardcode it in the prompt — else drift (refuses what it can do) + manual tax | [derive-agent-capabilities-from-registry.md](./derive-agent-capabilities-from-registry.md) |
| 24 | Current state = authority ABOVE stale memory; ship a new feature → agent says "this works now", don't delete context | [current-state-overrides-stale-memory.md](./current-state-overrides-stale-memory.md) |
| 25 | A high-value trigger the model resists (prior fights it) → intercept DETERMINISTICALLY before the LLM, don't rely on the prompt (coin-flip) | [intercept-deterministically-when-model-resists.md](./intercept-deterministically-when-model-resists.md) |
| 26 | A feature only counts if it lands on the path prod actually runs — flag-gated branch: check which prod runs + keep shared behavior in ONE source; eval in prod's config | [feature-must-land-on-the-prod-path.md](./feature-must-land-on-the-prod-path.md) |
| 27 | Front-load RECALL at session start; re-inject the METHOD just-in-time at the moment of use (front-loaded method dilutes in long sessions exactly when it fires) | [inject-recall-upfront-method-just-in-time.md](./inject-recall-upfront-method-just-in-time.md) |
| 28 | Enforce a guardrail at the most UNIVERSAL layer that survives the consumer switching tools (git pre-commit > one agent's hook; AGENTS.md > one tool's rules file) | [enforce-at-the-most-universal-layer.md](./enforce-at-the-most-universal-layer.md) |
| 29 | Make the entry point mirror the pitch — surface the claims where the traffic lands (promo names 3 differentiators → the README shows those 3 up front, not buried in sub-files) | [entry-point-mirrors-the-pitch.md](./entry-point-mirrors-the-pitch.md) |
| 30 | Genericize + leak-scan private-origin content BEFORE pushing to a public repo — verbatim-copy = exfiltration even when it "looks generic"; don't trust self-report, scan yourself; separate legit attribution (LICENSE) from leaks | [genericize-private-content-before-public-push.md](./genericize-private-content-before-public-push.md) |
| 31 | Same content on many surfaces → ONE source + per-item placement flags + optional fields (progressive) + fallback; don't fork an array/copy per surface (drift) | [one-source-many-surfaces-progressive.md](./one-source-many-surfaces-progressive.md) |
| 32 | A structured field (persona/query/keyword) → EXTRACT intent from the user's message first; don't echo raw text into the field (works when the user is verbose, shatters when terse). Fallback = clarify, not a raw search | [extract-intent-dont-echo-user-input.md](./extract-intent-dont-echo-user-input.md) |
| 33 | A live animation on one surface → recreate it DETERMINISTICALLY (a pure function of t), reuse the visuals + rebuild the timing; don't re-port setTimeout, don't redesign (broken identity). The animation case of the umbrella "reproduce identity-bearing artifacts deterministically"; static-visual case = [[reuse-brand-render-pipeline-not-ai-gen]] #17 | [recreate-live-animation-deterministically.md](./recreate-live-animation-deterministically.md) |
| 34 | Moving real footage with PII (scroll/pan) → SELECT a clean window (set in/out beats in PII-free gaps), don't chase a static blur box (guaranteed leak/over-blur). Blur = fallback for stationary PII; verify frame-by-frame; stuck → synthetic data | [select-clean-footage-over-masking-pii.md](./select-clean-footage-over-masking-pii.md) |
| 35 | A public mirror of a private source-of-truth drifts BOTH ways — sync = a two-way diff, not a push; content authored directly in the mirror must be reconciled back into the source (the thing read every session), else the source silently falls behind its own public face | [public-mirror-sync-is-bidirectional.md](./public-mirror-sync-is-bidirectional.md) |
| 36 | Capture consent at the POINT of collection, record it as proof (who/when/which policy version + server-side gate), and reframe risky disclosure — never hide it (hiding raises risk; disclosure is what makes the transfer legal) | [consent-at-collection-recorded-not-hidden.md](./consent-at-collection-recorded-not-hidden.md) |
| 37 | Match the control mechanism to the model's disposition — cooperative behavior → self-describing instruction (let the model decide); resisted behavior → deterministic intercept before the LLM. A detector on a signal that isn't the deciding one is brittle | [control-follows-model-disposition.md](./control-follows-model-disposition.md) |
| 38 | A feature-filter verdict is provisional until you pull behavioral telemetry — the same candidate flips "discovery-first ↔ build" purely from whether you opened the data; pull signal BEFORE you rule | [discovery-flips-a-feature-verdict.md](./discovery-flips-a-feature-verdict.md) |
| 39 | Docs/system-design MUST track actual code/prod — confirmed drift = fix the doc on the spot (same change-set), don't stack a "this is stale" note over the old text; "don't trust the doc" is only half, REPAIR is the other half | [doc-must-track-actual-code-fix-drift-on-sight.md](./doc-must-track-actual-code-fix-drift-on-sight.md) |
| 40 | Gate/rate-limit on the signal you HAVE at decision time, not the one you only learn after paying the cost — pre-cost proxy you can read now beats the exact-but-too-late number | [gate-on-signal-available-at-decision-time.md](./gate-on-signal-available-at-decision-time.md) |
| 41 | Before designing a "missing/deferred" feature, ground it in the existing code first — design the DELTA against what's already there, don't re-invent a capability that may partly exist | [ground-the-gap-before-designing-a-missing-feature.md](./ground-the-gap-before-designing-a-missing-feature.md) |
| 42 | Healthcheck DOWN = unreachable / liveness-dead, NOT degraded-under-load — a dead-man's switch measures process liveness; don't read "no ping" as "slow" (or "DB grew" as "alive") | [healthcheck-down-means-unreachable-not-degraded.md](./healthcheck-down-means-unreachable-not-degraded.md) |
| 43 | Keep learned/adaptive state as portable DATA decoupled from the model that consumes it — store it in a table/store, not baked into one model's weights/prompt, so swapping models doesn't lose it | [learned-state-portable-decoupled-from-model.md](./learned-state-portable-decoupled-from-model.md) |
| 44 | Localize a "missing/wrong" symptom to its LAYER before designing a fix — probe each layer (store → endpoint → render) to find where it actually breaks; don't fix the layer you guessed | [localize-symptom-to-layer-before-fixing.md](./localize-symptom-to-layer-before-fixing.md) |
| 45 | A new channel that reuses the core engine MUST replicate the reference handler's full contract (not just call the engine) — markers, delivery, capability boundary; a partial copy ships a subtly-broken channel | [new-channel-must-replicate-reference-handler-contract.md](./new-channel-must-replicate-reference-handler-contract.md) |
| 46 | Account recovery anchors on a factor that SURVIVES the loss, and any abusable re-bind must be OBSERVABLE (logged + notified) — don't anchor recovery on the thing being recovered | [recovery-anchors-on-surviving-factor-and-is-observable.md](./recovery-anchors-on-surviving-factor-and-is-observable.md) |
| 47 | A scope/safety gate by enumerated examples only covers what you listed — domain-refusal needs a POSITIVE scope definition plus enough weight to beat the "you can do anything" framing | [scope-gate-needs-positive-definition-not-denylist.md](./scope-gate-needs-positive-definition-not-denylist.md) |
| 48 | A security guarantee lives in the structural capability boundary (network/mounts/privilege/authz, independently verified), NOT in prompt refusal — prompt-gate is the soft outer layer, isolation is the backstop | [security-guarantee-lives-in-capability-boundary-not-prompt.md](./security-guarantee-lives-in-capability-boundary-not-prompt.md) |
| 49 | A shortcut/intercept must gate on READINESS, not just on the trigger — fire only when the inputs it needs are actually present, else it short-circuits into a broken path | [shortcut-gates-on-readiness-not-just-trigger.md](./shortcut-gates-on-readiness-not-just-trigger.md) |
| 50 | Threat-model a feature across EVERY OWASP family matching its surfaces (LLM + Web + API), not just the LLM Top 10 — at design time, because a chat agent is also a web/API endpoint | [threat-model-covers-every-surface-not-just-llm.md](./threat-model-covers-every-surface-not-just-llm.md) |
| 51 | User text that flows into a prompt (or a store that later feeds a prompt) is an injection surface — guard deterministically at the write/inject boundary; stored content is a delayed injection vector too | [untrusted-text-into-prompt-is-injection-surface.md](./untrusted-text-into-prompt-is-injection-surface.md) |
| 52 | We can both be wrong → verify an uncertain factual claim against the strongest source (test > read > web > memory) BEFORE acting; verify by trying to BREAK it; scale depth to stakes; tag provenance in chat | [verify-uncertain-claims-against-trusted-source.md](./verify-uncertain-claims-against-trusted-source.md) |
| 53 | Overruled by the owner (you said defer, owner says build) → comply (invest = owner's call), BUT bake the risk you flagged in as a guardrail + surface the limitation; don't tokenize/sabotage/silently-comply | [execute-overruled-decision-with-guardrail-baked-in.md](./execute-overruled-decision-with-guardrail-baked-in.md) |
| 54 | Ground a claim in literature ONLY when it's empirical+general (LLM/agent behaviour, methodology, measurable facts = level-3 #52); judgment/taste/in-project-incident → the incident IS the evidence, a citation = false authority (cherry-pick + misattribution + dilutes the "why"). Most principles are the second kind → don't paper-back them. A specific number from a weak source (vendor blog) → upgrade peer-reviewed OR caveat "unverified". Retrieval isn't trustworthy raw (keyword+citation-sort returns off-topic high-citation noise) → verify relevance per-record. Domain-specific application of [[verify-uncertain-claims-against-trusted-source]] #52 | [ground-empirical-claims-not-judgment-in-literature.md](./ground-empirical-claims-not-judgment-in-literature.md) |
| 55 | Default to a critical, evidence-aware stance — not validation: silently check what's wrong/weakly-assumed & surface the top weakness first; kill empty validation ("you're right"/"great question"/"perfect"); label confidence [High/Med/Low]; hold position under pushback (insistence ≠ new info); skip warm-up preamble; mirror the user's language | [critical-stance-not-validation.md](./critical-stance-not-validation.md) |

## Reference-only — Android/your organization origin ([`android/`](./android/))

Kept for when a sub-project here actually is an Android/your organization app. **Do not apply outside that
context** — they assume Gradle, Timber, DataStore, Crashlytics, or the your organization Jira pipeline.

`use-timber-not-log` · `datastore-load-before-use` · `crash-triage-default` ·
`as-gradle-daemon-lock` · `auto-transition-gate` · `jira-default-backlog`
