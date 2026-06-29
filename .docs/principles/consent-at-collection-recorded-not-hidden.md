# Capture consent at the point of collection, record it as proof, and reframe disclosure rather than hide it

**When this applies:** building or changing a flow that collects personal data (signup/register form,
upload, OAuth); writing legal copy (privacy/terms); or fielding a request to "hide / soften" part of a
disclosure (subprocessors, cross-border transfer, third parties) so users "trust it more" or it "looks
less scary."

**Principle:** three things that are easy to confuse:
1. **The consent point IS the collection point.** Consent is asked **at or before** the first piece of
   personal data enters (the email input), NOT after the fact (e.g. after verification, before a
   redirect). Once the data is already in, the consent is late.
2. **Consent only becomes proof if it is RECORDED.** A checkbox in the UI alone is not compliance — what
   counts during an audit or incident is a persisted record of **who + when + which policy version they
   agreed to** (a consent timestamp + policy version), plus a **server-side** gate (an HTML `required`
   attribute can be bypassed from the front end).
3. **Risky disclosure should be REFRAMED, never hidden.** Hiding the subprocessor list or the cross-border
   transfer wording so it "looks safe" is counterproductive and raises risk: the facts don't change (data
   still goes to external servers), transparency is a **legal obligation** (the applicable data-protection
   law), and what actually makes the transfer **lawful** is the disclosure plus consent. Soften the tone
   ("our trusted providers"), reframe it into a trust signal — don't delete it.

**Why:** a signup/consent flow shipped with the form collecting only email then submit — zero consent,
zero link to Terms/Privacy. The initial request was to "hide" the subprocessor section and the
cross-border-transfer section so the data would seem safe. That fails: hiding violates the transparency
duty of the applicable privacy regulation, is internally inconsistent (another section still names the
third-party providers), and misleads. The path chosen instead: reframe the subprocessor section
("world-class trusted companies, bound by data-protection agreements, data shared only as needed") while
keeping the full list; add an **explicit checkbox**, un-ticked and required, at the collection point; add
a server-side gate (reject with an error if consent is empty); and record the consent timestamp + policy
version (consent must be provable). The inline cross-border phrasing could be dropped ONLY because consent
was now an explicit checkbox with a clickable policy link that contains the transfer clause (incorporation
by reference) plus a footer linking Terms/Privacy — not because the disclosure disappeared.

**How to apply:**
- Map each piece of personal data to its **collection point**; place consent there, not in a later step.
- An **un-ticked + required** checkbox (affirmative, not pre-ticked/bundled) beats implicit clickwrap for
  sensitive data / cross-border transfer. Pair it with a **server-side gate**; don't rely on HTML attributes.
- **Record the consent**: timestamp + policy version, keyed to the user/email. This is the part most often
  skipped and exactly the part used during audit/incident. (See also [[learned-state-portable-decoupled-from-model]]
  — important state lives as portable DATA in the store.)
- Disclosure that makes you nervous → **reframe/soften the wording**, don't hide it. Removing disclosure
  raises risk, not lowers it. If it's dropped from one surface, make sure it's still accessible on another
  (clickable policy) and consistent across sections. This is the honesty side of [[dont-expose-the-recipe]]
  (here: don't hide what you're obligated to disclose) and parallels status-honesty tagging of assumptions.
- Double opt-in (email verification link) is a bonus piece of consent evidence, not a new consent point —
  the email need only link the policy, no second checkbox required.
