"""Render a tailored resume PDF from candidate.py + one tailoring in tailorings.py.

    python3 generate_resume.py <tailoring_key>     # -> out/resume_<key>.pdf

Only the SUMMARY and SKILLS come from the tailoring; every employer, date, bullet, and
credential comes from candidate.py, unchanged. Run verify.py on the output before you send it.
"""
import os
import sys
from fpdf import FPDF
import candidate as C
import tailorings as T

DARK = (34, 34, 34); GRAY = (110, 110, 110); BLACK = (17, 17, 17)


class Resume(FPDF):
    def bar(self, text):
        self.ln(1.0)
        self.set_fill_color(*DARK); self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8.5)
        self.cell(0, 4.5, "  " + text, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*BLACK); self.ln(1.2)


def build(key):
    if key not in T.TAILORINGS:
        raise SystemExit(f"unknown tailoring '{key}'. Options: {', '.join(T.TAILORINGS)}")
    t = T.TAILORINGS[key]
    summary = t.get("summary", C.SUMMARY)
    skills = t.get("skills", C.SKILLS)

    pdf = Resume(format="letter", unit="mm")
    pdf.set_margins(11, 10, 11)
    pdf.set_auto_page_break(True, margin=9)
    pdf.add_page()
    W = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_font("Helvetica", "B", 20); pdf.set_text_color(*BLACK)
    pdf.cell(0, 8, C.HEADER["name"], new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8.5); pdf.set_text_color(*GRAY)
    pdf.cell(0, 4.5, C.HEADER["contact"], new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1); pdf.set_draw_color(*BLACK); pdf.set_line_width(0.4)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y()); pdf.ln(2)

    pdf.set_font("Helvetica", "", 8.6); pdf.set_text_color(*BLACK)
    pdf.multi_cell(W, 3.5, summary, align="J", new_x="LMARGIN", new_y="NEXT")

    pdf.bar("SKILLS & AREAS OF EXPERTISE")
    pdf.set_font("Helvetica", "", 8.4); colw = W / 4
    GUTTER = 1.5
    for row in skills:
        for c in row:
            if c and pdf.get_string_width(c) > colw - GUTTER:
                raise SystemExit(
                    f"SKILLS cell overflows column: {c!r} is {pdf.get_string_width(c):.1f}mm, "
                    f"budget {colw - GUTTER:.1f}mm. Shorten the label.")
    for row in skills:
        for c in row:
            pdf.cell(colw, 4.0, c)
        pdf.ln(4.0)

    pdf.bar("EXPERIENCE")
    PAGE_BREAK_Y = pdf.h - pdf.b_margin
    for company, dates, title, blocks in C.EXPERIENCE:
        if pdf.get_y() + 22 > PAGE_BREAK_Y:   # keep-together: never orphan a header
            pdf.add_page()
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 9.6); pdf.set_text_color(*BLACK)
        pdf.cell(W * 0.72, 4.4, company, new_x="RIGHT", new_y="TOP")
        pdf.set_font("Helvetica", "", 8.4); pdf.set_text_color(*GRAY)
        pdf.cell(W * 0.28, 4.4, dates, align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*BLACK)
        if title:
            pdf.set_font("Helvetica", "I", 8.6)
            pdf.cell(0, 3.9, title, new_x="LMARGIN", new_y="NEXT")
        for kind, text in blocks:
            pdf.set_x(pdf.l_margin)
            if kind == "para":
                pdf.set_font("Helvetica", "I", 7.9); pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(W, 3.4, text, align="J", new_x="LMARGIN", new_y="NEXT")
                pdf.set_text_color(*BLACK)
            elif kind == "sub":
                pdf.ln(0.5); pdf.set_font("Helvetica", "B", 8.4)
                pdf.multi_cell(W, 3.9, text, new_x="LMARGIN", new_y="NEXT")
            elif kind == "bul":
                pdf.set_font("Helvetica", "", 8.1)
                pdf.set_x(pdf.l_margin + 1.5)
                pdf.multi_cell(W - 1.5, 3.4, chr(183) + "  " + text, align="L", new_x="LMARGIN", new_y="NEXT")
            elif kind == "used":
                pdf.set_font("Helvetica", "I", 7.3); pdf.set_text_color(*GRAY)
                pdf.multi_cell(W, 3.2, "   " + text, new_x="LMARGIN", new_y="NEXT")
                pdf.set_text_color(*BLACK)
        pdf.ln(0.8)

    pdf.bar("CERTIFICATIONS & EDUCATION")
    pdf.set_font("Helvetica", "", 8.2); pdf.set_x(pdf.l_margin)
    pdf.multi_cell(W, 3.9, C.CERTS, new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(W, 3.9, C.EDU, new_x="LMARGIN", new_y="NEXT")

    os.makedirs("out", exist_ok=True)
    out = f"out/resume_{key}.pdf"
    pdf.output(out)
    print(f"wrote {out}  ({pdf.page_no()} pages)")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "cloud_security")
