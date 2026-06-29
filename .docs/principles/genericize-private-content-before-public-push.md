# Genericize + leak-scan private-origin content before pushing to a PUBLIC repo

**When this applies:** copying / backporting / publishing anything from a private repo or workspace
into a **public** destination (OSS template, gist, marketplace, shared repo) — including "generic-looking"
docs, principles, agent/skill definitions, or config.

**Principle:** verbatim-copying private-origin content into a public repo **exfiltrates internals even
when it reads as generic**. Genericize FIRST (strip org / employer / product / personal / internal-project
/ infra identifiers), then run an **independent** leak-scan before the push. Don't trust "it's just a
principle file", a subagent's self-report, or the destination already looking clean.

**Why:** backporting private-workspace principles into a public template surfaced two failures. (1) An
auto-mode classifier **blocked the verbatim copy** — correctly: the files carried prod paths, an internal
sandbox env-flag name, and competitive-moat strategy. (2) An independent `grep` found the public repo
**already leaked** earlier — a founding strategy journal (moat / private-repo name), an employer's
regulated-industry specifics, an internal project codename, and a personal name — all pre-existing and
unnoticed. "Generic-looking" ≠ safe; a clean-looking destination can already be dirty.

**How to apply:**
- Before ANY push to a public repo, `grep -rniE` for identifier tokens: company, product, employer,
  regulators, prod IPs/hosts, env-flag names, internal project names, people's names, internal
  workspace/repo names.
- Genericize, don't copy: replace identifiers with neutral equivalents ("your organization", "a feature
  flag", "the applicable regulation"); rewrite war-story examples to neutral ones; keep the lesson intact.
- Re-scan **yourself** — never trust the author's or a subagent's "it's clean"; run the grep again.
- Separate **legit public attribution** (LICENSE copyright, the repo's own URL, author frontmatter) from
  leaks — don't strip those.
- If a tool/classifier blocks a cross-repo copy citing exfiltration, treat it as a **signal**, not an
  obstacle: STOP, check the destination's visibility (public/private) and the content, surface to the user.
- Pairs with [[validate-in-real-runtime-context]] (verify against reality, not assumptions).
