#!/usr/bin/env python3
"""calib — calibration loop for Claude's factual claims .

Records each MATERIAL factual claim as a row {claim, confidence, provenance, verdict},
lets the verdict be filled when ground truth surfaces, then reports whether stated
confidence matches reality (is [High] actually ~right?).

This tool is DELIBERATELY honest about its own weakness: most claims never get a clean
verdict, so the sample is sparse + biased toward claims that happened to be checked.
`report` therefore measures verdict COVERAGE and refuses to present accuracy as reliable
until coverage is decent — it warns loudly instead of pretending sparse data is signal.

Store: log.jsonl (one JSON object per line, append-mostly, git-tracked, greppable).
Pure stdlib. Run: python3 calib.py <cmd> ...

Commands:
  log     --claim TXT --confidence High|Medium|Low --provenance TXT [--session ID]
  verdict ID correct|wrong|partial [--note TXT]
  list    [--open]              # all rows, or only those missing a verdict
  report                        # calibration table + coverage warning
  capture --transcript PATH     # extract <!--CALIB {...}--> markers from a transcript (Stop hook)
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

# Marker the assistant emits in chat for a material claim; the Stop hook greps these verbatim.
#   <!--CALIB {"claim":"...","confidence":"High","provenance":"..."}-->
MARKER_RE = re.compile(r"<!--\s*CALIB\s*(\{.*?\})\s*-->", re.DOTALL)

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.environ.get("CALIB_LOG") or os.path.join(HERE, "log.jsonl")

CONF = ("High", "Medium", "Low")
VERDICTS = ("correct", "wrong", "partial")
# weight a verdict contributes to "accuracy" (partial = half-credit)
WEIGHT = {"correct": 1.0, "wrong": 0.0, "partial": 0.5}
# rough calibration targets — what a well-calibrated forecaster's accuracy should land near
TARGET = {"High": "≥0.85", "Medium": "~0.55–0.75", "Low": "≤0.50"}
MIN_SAMPLE = 5      # below this per level, accuracy is noise
MIN_COVERAGE = 0.50  # below this overall, the whole report is unreliable


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load():
    if not os.path.exists(LOG):
        return []
    rows = []
    with open(LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _save(rows):
    with open(LOG, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _next_id(rows):
    n = 0
    for r in rows:
        try:
            n = max(n, int(str(r["id"]).lstrip("k")))
        except (ValueError, KeyError):
            pass
    return "k%03d" % (n + 1)


def _row_hash(claim, conf, prov):
    # Stable content hash → dedup. The Stop hook re-scans the WHOLE transcript every turn, so
    # without this the same claim would be re-logged on every assistant message.
    key = "%s|%s|%s" % ((claim or "").strip(), conf or "", (prov or "").strip())
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


def _append(rows, claim, conf, prov, session, src):
    """Append a claim row if its content hash isn't already present. Returns the row or None (dup)."""
    h = _row_hash(claim, conf, prov)
    if any(r.get("h") == h for r in rows):
        return None
    row = {
        "id": _next_id(rows), "ts": _now(), "session": session or "",
        "claim": claim, "confidence": conf, "provenance": prov,
        "verdict": None, "checked_ts": None, "note": None,
        "h": h, "src": src,
    }
    rows.append(row)
    return row


def cmd_log(a):
    if a.confidence not in CONF:
        sys.exit("confidence must be one of %s" % (CONF,))
    rows = _load()
    row = _append(rows, a.claim, a.confidence, a.provenance,
                  a.session or os.environ.get("CLAUDE_SESSION_ID", ""), "manual")
    if row is None:
        print("skip (already logged): %s" % a.claim)
        return
    _save(rows)
    print("logged %s  [%s]  %s" % (row["id"], a.confidence, a.claim))


def cmd_capture(a):
    """Read a transcript JSONL, extract <!--CALIB {...}--> markers, log new ones (dedup by hash)."""
    path = a.transcript
    if not path or not os.path.exists(path):
        return  # best-effort: no transcript → nothing to do (hook must never fail the turn)
    # Parse the JSONL and pull the assistant's CLEAN text. Reading raw won't work: each turn's text
    # is stored AS a JSON string, so a marker's quotes arrive escaped (\") and won't json.loads.
    # Going through json.loads per line un-escapes the text back to real quotes.
    text = ""
    try:
        for line in open(path, encoding="utf-8", errors="replace"):
            line = line.strip()
            if not line or "CALIB" not in line:
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            msg = obj.get("message", obj)
            content = msg.get("content")
            if isinstance(content, str):
                text += "\n" + content
            elif isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "text":
                        text += "\n" + b.get("text", "")
    except OSError:
        return
    rows = _load()
    added = 0
    for m in MARKER_RE.finditer(text):
        try:
            d = json.loads(m.group(1))
        except (ValueError, TypeError):
            continue
        claim, conf, prov = d.get("claim"), d.get("confidence"), d.get("provenance", "")
        if not claim or conf not in CONF:
            continue  # malformed marker → skip, don't pollute the log
        if _append(rows, claim, conf, prov, d.get("session", ""), "auto") is not None:
            added += 1
    if added:
        _save(rows)
    print("captured %d new claim(s)" % added)


def cmd_verdict(a):
    if a.status not in VERDICTS:
        sys.exit("verdict must be one of %s" % (VERDICTS,))
    rows = _load()
    for r in rows:
        if r["id"] == a.id:
            r["verdict"] = a.status
            r["checked_ts"] = _now()
            if a.note:
                r["note"] = a.note
            _save(rows)
            print("%s -> %s" % (a.id, a.status))
            return
    sys.exit("id not found: %s" % a.id)


def cmd_list(a):
    rows = _load()
    if a.open:
        rows = [r for r in rows if r["verdict"] is None]
    if not rows:
        print("(none)")
        return
    for r in rows:
        v = r["verdict"] or "?"
        print("%-5s %-7s %-9s %s" % (r["id"], r["confidence"], v, r["claim"][:80]))


def cmd_report(_a):
    rows = _load()
    total = len(rows)
    if total == 0:
        print("no claims logged yet — nothing to calibrate.")
        return
    judged = [r for r in rows if r["verdict"] in VERDICTS]
    coverage = len(judged) / total

    print("CALIBRATION REPORT")
    print("  claims logged : %d" % total)
    print("  with verdict  : %d  (coverage %.0f%%)" % (len(judged), coverage * 100))
    print()
    print("  %-8s %5s %8s %9s   target" % ("conf", "n", "judged", "accuracy"))
    for c in CONF:
        grp = [r for r in rows if r["confidence"] == c]
        jg = [r for r in grp if r["verdict"] in VERDICTS]
        if jg:
            acc = sum(WEIGHT[r["verdict"]] for r in jg) / len(jg)
            accs = "%.0f%%" % (acc * 100)
            if len(jg) < MIN_SAMPLE:
                accs += "*"  # too-small sample
        else:
            accs = "—"
        print("  %-8s %5d %8d %9s   %s" % (c, len(grp), len(jg), accs, TARGET[c]))
    print()
    print("  * = sample < %d; accuracy is noise, not signal." % MIN_SAMPLE)

    # Honest guardrail: don't let sparse/biased data masquerade as a calibration verdict.
    if coverage < MIN_COVERAGE:
        print()
        print("  ⚠️  COVERAGE %.0f%% < %.0f%% — DO NOT trust these accuracies." % (
            coverage * 100, MIN_COVERAGE * 100))
        print("      Only checked claims have verdicts, so the sample is biased toward")
        print("      claims that got verified. Fill more verdicts (calib.py list --open)")
        print("      before reading anything into the numbers.")


def main(argv=None):
    p = argparse.ArgumentParser(prog="calib.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("log", help="record a claim (verdict left open)")
    pl.add_argument("--claim", required=True)
    pl.add_argument("--confidence", required=True, choices=CONF)
    pl.add_argument("--provenance", required=True)
    pl.add_argument("--session", default="")
    pl.set_defaults(fn=cmd_log)

    pv = sub.add_parser("verdict", help="fill a claim's verdict")
    pv.add_argument("id")
    pv.add_argument("status", choices=VERDICTS)
    pv.add_argument("--note", default="")
    pv.set_defaults(fn=cmd_verdict)

    pls = sub.add_parser("list", help="list claims")
    pls.add_argument("--open", action="store_true", help="only claims missing a verdict")
    pls.set_defaults(fn=cmd_list)

    pr = sub.add_parser("report", help="calibration table + coverage warning")
    pr.set_defaults(fn=cmd_report)

    pc = sub.add_parser("capture", help="extract CALIB markers from a transcript (Stop hook)")
    pc.add_argument("--transcript", required=True)
    pc.set_defaults(fn=cmd_capture)

    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
