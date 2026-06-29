# Validate integrations in the real runtime context, not just interactively
**When this applies:** wiring an external CLI/tool/credential into a service (systemd, container, cron,
subprocess) — anything that will run **non-interactively** / non-login, not in your terminal.
**Principle:** "works when I type it" ≠ "works in the service." Reproduce in the *actual* runtime context
(non-login shell, the service's env, the container) **early**, because PATH, auth/keyring, shell init,
and tool flags behave differently there. Bisect by changing one variable at a time.
**Why:** a CLI can work perfectly in your interactive SSH terminal yet the service fails with something
like "Not logged in." Reproducing in a *non-login* shell often reveals several distinct context gaps at
once: a wrapper that only resolves on a login-shell PATH, a flag whose name hides a side effect (e.g. it
silently skips auth), and interactive keyring creds that a background service simply can't see (so it
needs an explicit token env var). Each only surfaces by testing as the service runs, not as you-in-a-terminal.
**How to apply:**
- Reproduce with `ssh host 'cmd'` (non-login) or `systemd-run`/the container, not just an interactive shell.
- When interactive≠service, bisect one variable: login vs non-login, each flag, env present vs absent.
- For auth: prefer an explicit token/env over ambient interactive creds (keyring/session) a service can't reach.
- Don't trust a tool flag's name — verify its real effect in context.
- Pairs with [[name-conflicts-with-source-of-truth]] (verify before assuming) + the deploy gotchas in `.docs/common-issues/`.
