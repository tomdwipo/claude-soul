# Tolerate agent/MCP clients that coerce arguments

**When this applies:** any tool/endpoint consumed by heterogeneous agent/LLM clients — strict output
schema + opaque args is an invitation to silent failure.

**Principle:** a tool called by many different agents/clients **must not depend hard on exact argument
values** — some clients silently coerce or mangle args. Design the tool to stay useful even when an arg
arrives "malformed."

**Why (the shape of the bug):** a status tool takes a string resource id; one client **coerces it to an
integer** even though the user passed a full string token (deterministic, repeatable). The validation
layer then rejects it (type error) and the user can't check status — even though the underlying job
succeeded. Not the user's fault, not yours — a client quirk.

**How to think (transferable):**
- **Accept loose types + coerce yourself.** `id: str | int` then `str(id)` — don't let the validation
  layer reject first.
- **Make the handle optional + a sensible fallback.** If the id is empty/not found → return the
  most-likely-intended state (e.g. the user's most recent resource). Many flows have only one active resource.
- **Provide a recovery path.** A list tool so an agent that "forgot"/mangled the id can find it again.
- **Separate the API handle from the security token.** If you need an opaque, unguessable id (capability
  URL), put it in its own field/path — don't force *that* to be the only handle the client must pass
  (and might corrupt). Security-by-opacity ≠ must be fragile client-side.

**Acknowledged tension:** opaque ids (anti-enumeration, capability URLs) are good for security but trip
some clients. Resolve it with tolerance + fallback, not by weakening the URL's security.
