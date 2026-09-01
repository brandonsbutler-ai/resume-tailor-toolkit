"""The honesty + layout gate. Run it on every generated PDF before you send it.

    python3 verify.py out/resume_cloud_security.pdf [more.pdf ...]

Exits NON-ZERO if a PDF contains:
  - any credential in candidate.NEVER_CLAIM (the thing this whole toolkit exists to prevent),
  - any phrase in BANNED_PHRASES (resume-inflation tells you never want),
  - non-ASCII text where the layout assumes latin-1 (stray smart quotes / em dashes),
  - a page count outside the expected range (guards the orphan/blank-page bug).

Wire it into a pre-commit hook or CI so a fabricated claim can't reach a PDF you send.
Requires poppler-utils (`pdftotext`, `pdfinfo`).
"""
import re
import subprocess
import sys
import candidate as C

# Generic inflation tells -- extend for your own taste.
BANNED_PHRASES = [
    "results-driven", "synergy", "ninja", "rockstar", "guru",
    "single-handedly", "world-class", "10x engineer",
]

# Page-count expectations by filename prefix.
PAGE_RULES = {"resume_": (1, 2), "cover_": (1, 1)}

# The only non-ASCII code point the resume layout intends (middle-dot bullet, U+00B7).
ALLOWED_NONASCII = {"·"}


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def check(path):
    fails = []
    text = run(["pdftotext", "-layout", path, "-"])
    low = text.lower()

    for claim in C.NEVER_CLAIM:
        # allow it only inside an explicit "do not / no <claim>" honesty sentence
        for m in re.finditer(re.escape(claim.lower()), low):
            ctx = low[max(0, m.start() - 24):m.start()]
            if not re.search(r"\b(no|not|don'?t|without|never)\b[^.]*$", ctx):
                fails.append(f"NEVER_CLAIM leaked: {claim!r}")
                break

    for phrase in BANNED_PHRASES:
        if phrase.lower() in low:
            fails.append(f"banned phrase: {phrase!r}")

    for ch in set(text):
        if ord(ch) > 127 and ch not in ALLOWED_NONASCII and not ch.isspace():
            fails.append(f"non-ASCII char {ch!r} (U+{ord(ch):04X}) -- use plain ASCII / '--'")
            break

    info = run(["pdfinfo", path])
    mp = re.search(r"^Pages:\s+(\d+)", info, re.M)
    pages = int(mp.group(1)) if mp else 0
    for prefix, (lo, hi) in PAGE_RULES.items():
        if prefix in path and not (lo <= pages <= hi):
            fails.append(f"page count {pages} outside expected {lo}-{hi}")
    return pages, fails


def main(paths):
    if not paths:
        raise SystemExit("usage: python3 verify.py <pdf> [pdf ...]")
    bad = 0
    for p in paths:
        pages, fails = check(p)
        if fails:
            bad += 1
            print(f"FAIL  {p}  ({pages}pp)")
            for f in fails:
                print(f"        - {f}")
        else:
            print(f"PASS  {p}  ({pages}pp)")
    if bad:
        print(f"\n{bad} file(s) failed the gate. Fix the source, do not ship.")
        sys.exit(1)
    print("\nAll clear.")


if __name__ == "__main__":
    main(sys.argv[1:])
