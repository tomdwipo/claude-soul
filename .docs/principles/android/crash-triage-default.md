# Crash triage without a tombstone → monitoring-only
**When this applies:** a Logcat-Analyzer-Agent auto-filed Crashlytics ticket with no tombstone fields (signal, fault_addr, abi, api_level, device, build_id, top_frames).
**Principle:** don't deep-triage placeholder text — verdict `H?` (insufficient data), close monitoring-only with a 24–72h re-scan trigger.
**Why:** there is no Crashlytics MCP; without the tombstone the competing hypotheses (GWP-ASan sampled-fatal, vendor `.so` bug, TLS abort, runtime null-deref) cannot be distinguished (confirmed PROJ-9476).
**How to apply:**
- Skip investigation steps that need the tombstone; record an `H?` catalog sub-note.
- Re-scan trigger: "if the issue grows beyond N events OR reproduces on a 2nd device within 3d, re-open with tombstone fields".
- Conditional follow-ups ship as SEPARATE tickets only when evidence justifies them.
