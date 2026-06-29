# How to Learn (Distillation Engine)

Turn a single correction into a transferable principle — not a brittle rule.
Run this whenever the user corrects me, says "take lesson", or `/learn` is invoked.

## The 7 steps
1. **Identify** — state concretely what went wrong (or right). Quote the correction.
2. **Why** — find the underlying cause, not the surface symptom.
3. **Pattern** — would this apply in 3+ situations? If no → drop it; don't file noise.
4. **Check existing** — scan [`./README.md`](./README.md) AND [`../common-issues/README.md`](../common-issues/README.md). Prefer to **sharpen / merge** an existing entry over adding a sibling.
5. **Write as a principle** — describe *how to think*, not a fixed *what to do*.
   - Rule (brittle): "Never end a diff answer with 'want me to sync?'".
   - Principle (transfers): "A question about a diff is exploration; wait for an action verb."
6. **Place it (principle-default fork)** —
   - a compile / test / lint / build result settles it → **RULE** → `.docs/common-issues/` (+ catalog row).
   - judgment / taste / when-to-act → **PRINCIPLE** → `.docs/principles/` (+ index row).
   - unsure → default to a **PRINCIPLE** (principle over rule).
7. **Commit tight** — one fact per file; link related via the index; keep each file small.

## Anti-patterns (from the Warp reply-learning essay)
- Turning every correction into a new rule (overfitting → brittle exceptions).
- Keeping stale principles (never sharpening/merging → accretion).
- Codifying a one-off preference as a durable principle.

## Principle file shape
- `# <Title — how to think>`
- `**When this applies:**` the trigger a future reader recognises.
- `**Principle:**` the durable idea.
- `**Why:**` the correction / root cause that produced it.
- `**How to apply:**` 2–4 concrete bullets.
