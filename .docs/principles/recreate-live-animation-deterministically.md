# A live animation on one surface → recreate it DETERMINISTICALLY (a pure function of t), don't re-port setTimeout / don't redesign

**When this applies:** you have an animation (HTML/CSS/JS) running on one surface (e.g. a web landing page)
and you're asked to show the *same* motion on another surface that renders **frame-by-frame** (e.g. a video
pipeline: a headless browser sets `__setFrame(t)` → PNG → mp4). Or, more generally: porting motion between a
real-time runtime and a deterministic one.

**Principle:** **don't re-port the real-time timeline** (`setTimeout`/`requestAnimationFrame` is
non-deterministic → janky and non-reproducible under capture), and **don't redesign from scratch** (a new
look = a broken identity). Take the **visual layer** (CSS + markup) as-is, then **convert the timeline into a
pure function of `t`**: build the timeline once (a list of events with an `at` time), and render *the state
at time t* on each frame. One look, two surfaces, one identity.

**Why:** a frame-by-frame pipeline needed a clip identical to an existing landing-page animation. The landing
used `setTimeout` — real-time, unusable directly in a pipeline that needs determinism (each frame = a
function of `t`). The fix: a new template that **copies the landing's CSS** but **rebuilds the timeline
deterministically** (events with an `at`, `opacity = easeOutCubic(clamp((t - at) / dur))`, a blink as a
function of `sin(t)`). Result: the look is identical to the landing, but reproducible and consistent with the
pipeline's conventions. Adding a surface ≠ forking the capture code: the capture path was made to **honor a
`template` field** (like its sibling already did), so a new variant = a new template + a manifest field, not
re-coding the renderer.

**How to apply:**
- **Reuse the visual, rebuild the timing.** Copy CSS/markup from the source surface; drop `setTimeout`/`rAF`,
  replace with a `__setFrame(t)` that reads a pre-computed timeline. Determinism = a pipeline invariant
  ([[validate-in-real-runtime-context]] is a neighbor: render in the real runtime).
- **Extension point, not a fork.** If the capture/route hardcodes one template, generalize via a field
  (`post.template || 'default'`) — in line with the pattern already in the repo (don't open a new path).
- **Data-driven manifest.** Content (chat/file/result/hook/endcard) lives in a data file, not the template —
  adding a post = editing data.
- **One identity across surfaces:** web + video + (later) others must read as one brand; recreate, don't
  reinterpret.
- **Umbrella (the animation case of a more general principle):** an existing **identity-bearing artifact** →
  reproduce it **DETERMINISTICALLY** by reusing the exact source, never via a stochastic/regenerate/redesign
  path that breaks identity. The **static-visual** case: [[reuse-brand-render-pipeline-not-ai-gen]] (brand
  assets via the render pipeline + exact tokens, not AI image-gen).
- Neighbors: [[validate-in-real-runtime-context]], [[adapt-template-to-stack]].
- **Eval-case:** "animation X already exists on web, want it in a video" → correct = extract CSS + a
  function-of-`t` timeline + an extension point; **wrong** = porting raw `setTimeout` (janky/non-deterministic)
  OR a fresh redesign (broken identity).
