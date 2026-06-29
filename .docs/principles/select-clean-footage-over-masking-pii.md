# PII in footage → SELECT a clean window, don't chase a blur over moving PII

**When this applies:** building a demo/clip from a real **screen recording** that contains PII (email / phone
/ messaging handle / name / verification code / notification) that **scrolls or pans** across the screen — a
chat that scrolls, a spreadsheet dragged horizontally, a moving list.

**Principle:** **selection > masking.** First choose *which footage you sample* (the in/out beats) so PII
**never enters the frame** — rather than covering moving PII with a static blur box. A static blur is a
**fallback** for the leftover *stationary* PII, not the primary tool. Moving footage → PII changes position →
a static mask is guaranteed to do one of two things: **leak** (PII scrolls out from under the box) or
**over-blur** (it covers the content you wanted to show). Moving the beat cut-points to a "clean window" is
far more robust than fitting a box to a moving target.

**Why:** two recordings — a chat (recruiter email + phone, vertical scroll) and a spreadsheet (an "apply"
column with emails, horizontal scroll). The first instinct, static blur boxes, missed repeatedly (the band
rendered over empty area while PII stayed readable) and needed re-render after re-render. What finally worked:
**re-scope the beats** to clean windows — the "detail" column *before* the apply column came into view, the
"why it fits" column *after* it had passed — so the sheet's PII was never in frame, zero blur. Blur was used
only on the relatively static chat (and even there it needed a generous band). PII is a **release blocker**;
this is the tactic when the footage is *real* (the sibling tactic, when you control the content, is to use
synthetic data so it's zero-PII by construction — [[recreate-live-animation-deterministically]]).

**How to apply:**
- **Map first** when PII enters/leaves the frame (a timestamped contact-sheet), then set in/out beats in the
  clean gaps between — skip PII-bearing ranges, don't sample there.
- **Static blur only when PII is relatively stationary** and unavoidable; give the band a **generous** margin
  (top/bottom) because even small scroll shifts the text; blur coordinates are in the **final OUTPUT frame**
  (after crop+pad), not the source frame.
- **Verify frame-by-frame** on every PII-bearing beat (sample the output every ~0.3s + zoom in); don't trust
  a band that "looks like it covers it" — a one-pixel leak is still a blocker.
- If the real footage is mostly moving PII with no clean window → fall back to **synthetic data / recreate**
  (no-PII by construction), don't force a blur.
