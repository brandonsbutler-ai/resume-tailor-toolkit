# resume-tailor-toolkit

**Tailor a resume and cover letter to each job from one truthful source of facts — and refuse to ship anything you can't back up.**

Most resume tools (and most AI resume tools) optimize for keyword match. They will happily
invent a certification, inflate a title, or bury a gap. This toolkit optimizes for the opposite:
**every line on the page traces to a source-of-truth facts file, tailoring can only reframe what
is already true, and a verification gate fails the build if a banned or unbacked claim slips in.**

It generates:

- a clean **2-page resume** PDF, per-role tailored;
- a matching **1-page cover letter** PDF;
- an interactive **application tracker** (single self-contained HTML file).

## Why it's different

| Typical resume tool | This toolkit |
|---|---|
| Free-text edits per job; easy to drift into fiction | One `candidate.py` holds the facts; tailoring **only** overrides the summary and skills framing |
| "Add keywords to pass the ATS" | Add keywords **only if they're true**; the gate blocks the rest |
| Hides gaps | Cover letters name gaps in their own paragraph — honesty as strategy |
| No safety net | `verify.py` scans every generated PDF for banned claims + layout defects and **exits non-zero** on failure |

The verification gate is the point. It's a CI-friendly script: wire it into a pre-commit hook
or a GitHub Action and a fabricated credential can't reach a PDF you send out.

## Quick start

```bash
pip install fpdf2            # PDF rendering; pdftotext/pdfinfo (poppler-utils) for verify
./build.sh                   # generates + verifies all tailorings into out/
```

Or step by step:

```bash
python3 generate_resume.py       cloud_security     # -> out/resume_cloud_security.pdf
python3 generate_cover_letter.py cloud_security     # -> out/cover_cloud_security.pdf
python3 verify.py                out/resume_cloud_security.pdf   # honesty + layout gate
python3 generate_tracker.py                          # -> out/tracker.html
```

## How it works

1. **`candidate.py`** — the single source of truth: summary, skills, experience, and
   `NEVER_CLAIM` (credentials the candidate does *not* hold). Edit this to make it yours.
2. **`tailorings.py`** — one entry per target job. A tailoring may override the `summary` and the
   `skills` grid to speak the posting's language. It **cannot** add experience or certs — those
   come only from `candidate.py`.
3. **`generate_resume.py` / `generate_cover_letter.py`** — render the PDFs from (1) + (2).
4. **`verify.py`** — the gate. Extracts the PDF text and fails if it contains any `NEVER_CLAIM`
   term, any phrase in `BANNED_PHRASES`, non-ASCII where ASCII is required, or an orphan/blank
   page. Run it before every send.
5. **`generate_tracker.py`** — builds an interactive HTML board to track which roles you've
   applied to (progress persists in the browser).

## Design notes

- PDFs use Helvetica (latin-1) — write `--`, not em dashes; the gate flags stray non-ASCII.
- Resume target is 2 pages, cover letter 1; the gate checks page counts and guards against the
  classic fpdf "orphan header on a near-blank page" bug.
- Sample data describes a **fictional** candidate ("Alex Morgan"). Replace it with your own.

## License

MIT — see [LICENSE](LICENSE).
