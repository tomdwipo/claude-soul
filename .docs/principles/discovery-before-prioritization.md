# Discovery before prioritization — a decision funnel filters candidates, it doesn't generate them
**When this applies:** deciding whether a new product/feature is worth building; designing or judging a
"product decision framework"; weighing a validation gate (proceed to the next phase / commit to build).

**Principle:** scoring & filtering (RICE/ICE, or any custom funnel) are tools for **sequencing after
discovery**, not tools for deciding *what is worth building*. A funnel only filters candidates already in
hand — if those candidates were born from a solution you'd already imagined, the funnel just becomes a
machine for **rationalizing a pre-baked feature**. So in front of the funnel there must be a **generator**:
problem-discovery that produces candidates from problems, not from solutions. And validate on **behavior**,
not **stated intent**.

**Why:** the consensus of top product practitioners (Cagan/SVPG, Teresa Torres, Amazon Working Backwards,
Paul Graham, Reforge):
- **Teams jump to solutions ~98% of the time** — the #1 mistake. Locking a feature at roadmap level skips discovery.
- **Scoring formulas are demoted** — "product is judgment, not a template/formula"; match rigor to consequence (small, reversible bets shouldn't get heavy process).
- **Stated intent is unreliable** — people saying "I need this" / "I'd pay" is not proof. Validate via *do things that don't scale*: recruit users by hand, concierge MVP, unscalable founder effort.
- Recommended discovery frame: **Continuous Discovery + Opportunity Solution Tree** — anchor to an *outcome* (North Star) → map *opportunities* → then *solutions* → experiment.

**How to apply:**
- **Always put a step-0 Discovery in front of any funnel.** Tie an Opportunity Solution Tree to your North Star outcome → opportunities first, solutions later.
- **A decision funnel filters, it doesn't generate.** Pair a generator step (discovery, pulls signals from telemetry + interviews + funnels → opportunities out) with a filter step (gates → verdict). The framework is scaffolding, not an oracle — every opportunity must trace to a real signal; don't invent them.
- **Moat is a tie-breaker, not a kill-switch, pre-PMF.** Pre-PMF the job is to *find* PMF; moat comes after. Don't kill a PMF-seeking experiment just because it doesn't yet deepen the moat. (See [[eval-engineering]].)
- **Gates must be behavior, not stated-intent.** Check: did users actually do the workflow? come back? did the North Star move? — not "≥N people said they want it." Parallels [[calibrate-to-the-real-audience]].
- **Eval-case (regression):** trigger "decide/prioritize a new feature/product" → correct behavior = run problem-discovery first & check behavioral evidence; **wrong** = immediately score/rank a feature list with no discovery.
