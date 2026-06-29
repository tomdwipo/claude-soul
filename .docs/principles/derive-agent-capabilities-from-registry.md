# Derive an agent's self-knowledge (what it can do) from the registry — don't hardcode it in the prompt
**When this applies:** writing/maintaining the system prompt of an LLM agent that has registered
capabilities/skills/tools — a chat agent, MCP server, function-calling agent. When putting "you can do X,
Y, Z" + per-skill trigger instructions into the prompt.

**Principle:** the agent's capability list + per-capability trigger instructions must be **assembled from
the source of truth (catalog/manifest/registry)**, not hand-written strings. A hardcoded list **silently
drifts** from the skills actually registered → the agent **refuses things it can actually do** (or claims
ones it can't), and every new capability becomes a **manual prompt-tuning tax**. For a capability that
needs a special flow (interview/sentinel), store its recipe **as data in the registry**, not baked into a monolithic prompt.

**Why:** when the capability list is hardcoded in the prompt, adding a new skill to the registry doesn't
update the prompt — so the agent refuses the new skill ("that's outside what I can do") even though the
skill exists and its worker runs. Every new skill = a manual prompt edit + wording tuning. If one surface
(e.g. the tool API) is already manifest-driven while another (the chat prompt) is hardcoded, the chat side
falls behind. Fix: split into a static base (persona/format/rules) + a dynamic block assembled from the
registry each turn (description = capability, a `hint` field = trigger recipe) → the N+1th skill = zero prompt edits.

**How to apply:**
- **Split the prompt:** a static BASE (persona/format/rules, rarely changes) + a DYNAMIC block assembled from the registry each turn (cheap, 1 query/read).
- **Per-capability recipe = a data column** (e.g. a `hint` field), assembled automatically. Adding a sentinel skill = set one field, not edit the parent prompt.
- **Pick the right surface for the scope:** advertise from the registry that fits the consumer — an install-gated tool surface (user curates) ≠ a hosted chat (user doesn't curate → use the WHOLE catalog so nothing is forgotten). Wrong scope = regression (see [[delegation-level-match-consumer]]).
- **Be assertive against model refusal:** small models invent "outside my capabilities" for tasks that feel external — the prompt must say explicitly "you CAN do everything in the list, don't refuse."
- **Add eval-routing** (message → expected trigger) as a regression guard — trigger regressions pass unit tests; only eval/smoke catches them ([[eval-engineering]]).
- **Eval-case:** trigger "agent refuses a capability that is actually registered" / "adding a skill needs a manual prompt edit" → there's prompt↔registry drift; correct = prompt derived from the registry + eval-routing.

**Same mechanism (project the artifact from ONE source of truth; a hand-maintained parallel copy drifts):**
[[one-source-many-surfaces-progressive]] — multi-surface content from one source + flags, not per-surface
copies. Here: agent capabilities from the registry, not a hardcoded list. Different artifact, same anti-drift.
