# Confirm the POSITIVE signal before teardown — empty / no-error output ≠ pass

**Symptom:** you run an end-to-end verification (smoke test, clean-clone install check, handshake),
it prints **nothing** (no error, no result), and you're about to read that as "fine" — or you've
already deleted the test fixture (dummy repo, clone, temp dir) before confirming it actually passed.

**Cause:** a run that produces **no output is not a pass** — it's *unknown*. The most common reason is
a **harness/script bug**, not the thing under test. Real example: verifying a clean clone could install
an MCP, the handshake produced zero output → looked like the MCP failed; the actual cause was a shell
bug (an unquoted `$CMD` that didn't word-split — see [[zsh-no-word-split-unquoted-var]]). The MCP was
fine; the test was broken.

**Fix / discipline:**
1. **Assert the EXPECTED positive signal**, never just "no error / no output." A verification must check
   for a concrete success marker (`✅ tools/list: 31 tools`, `status: healthy`, exit 0 **and** the
   expected line) — absence of failure is not presence of success.
2. **Don't teardown until the result is confirmed.** Delete the dummy/clone/temp **after** the pass
   prints, not before — else a false-negative (or your own bug) destroys the artifact you'd debug with.
   Verify → confirm pass → then clean up.

**Trust the output, not the process signal** — a script can exit 0 having done nothing, and a CLI can
return an error in stdout while leaving stderr empty. For the specific zsh word-split mechanics, see
[[zsh-no-word-split-unquoted-var]]. Complements the verify-at-the-real-entry-point principle.
