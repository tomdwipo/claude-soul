# On-brand visual assets: reuse the existing deterministic render pipeline, not AI image-gen

**When this applies:** you need a new on-brand asset (a banner, a card, a wordmark image) and a brand
already has finished identity assets + a deterministic pipeline that produces them.

## Principle
If the brand already has **finished identity assets** (profile image, wordmark) + a **deterministic
pipeline** that emits them (e.g. HTML/CSS + a brand stylesheet + a headless-browser screenshot), make the
**new asset go through that same pipeline** — don't reach for AI image-gen.

**Why:**
1. **One identity, exact.** AI image-gen can't guarantee exact font/color — a specific display font drifts
   to a lookalike, brand hex values shift. The pipeline uses literal brand tokens → byte-for-byte
   consistent with the existing profile/site assets.
2. **Deterministic & re-generatable.** Change the tagline → edit the template, re-render, identical result.
   AI = different every generation.
3. **Reuse infra, zero duplication.** The static server + capture + brand stylesheet already exist; you
   just add one template.

AI image-gen is still right for things that need *illustration/composition* (hero art, mockups) — not for
**typographic/identity** assets that must match existing assets exactly.

## How to apply
1. Before making a new brand asset, find a similar existing asset + the script/pipeline that produces it.
2. Add a new template using the same brand tokens (the shared stylesheet), not a re-spec of color/font from scratch.
3. Verify visually side-by-side against the existing assets — font, color, vibe.

**Umbrella (the static-visual case of a more general principle):** an existing **identity-bearing
artifact** → reproduce it **DETERMINISTICALLY** by **reusing the exact source** (pipeline + brand
tokens), never via a **stochastic/regenerate/redesign** path that breaks identity. The **animation**
case of the same principle: [[recreate-live-animation-deterministically]] (reuse the CSS, rebuild the
timeline as a pure function of `t`, don't re-port `setTimeout`/redesign).

Pairs with [[adapt-template-to-stack]] (reuse what exists, adapt it; don't build a parallel path).
