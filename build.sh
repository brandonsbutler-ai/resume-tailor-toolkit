#!/usr/bin/env bash
# Generate every tailoring's resume + cover letter, run the honesty gate on all of them,
# and build the tracker. Fails (non-zero) if any PDF trips the gate.
set -euo pipefail
cd "$(dirname "$0")"

KEYS=$(python3 -c "import tailorings as t; print(' '.join(t.TAILORINGS))")

for k in $KEYS; do
  python3 generate_resume.py "$k"
  python3 generate_cover_letter.py "$k"
done

python3 generate_tracker.py

echo "--- honesty + layout gate ---"
python3 verify.py out/resume_*.pdf out/cover_*.pdf

echo "--- done: out/ ---"
ls -1 out/
