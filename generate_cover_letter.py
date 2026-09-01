"""Render a tailored cover-letter PDF from candidate.py + a tailoring's `cover` paragraphs.

    python3 generate_cover_letter.py <tailoring_key>    # -> out/cover_<key>.pdf

The cover paragraphs are where you name honest gaps in plain words -- that candor is the
strategy, not a weakness. Run verify.py on the output before you send it.
"""
import os
import sys
from datetime import date
from fpdf import FPDF
import candidate as C
import tailorings as T


class Cover(FPDF):
    def header(self): pass
    def footer(self): pass


def build(key):
    if key not in T.TAILORINGS:
        raise SystemExit(f"unknown tailoring '{key}'. Options: {', '.join(T.TAILORINGS)}")
    t = T.TAILORINGS[key]
    paras = t.get("cover", ["(add a `cover` list of paragraphs to this tailoring.)"])

    pdf = Cover(orientation="P", unit="mm", format="Letter")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    left = right = 25
    pdf.set_left_margin(left); pdf.set_right_margin(right)
    usable = 215.9 - left - right

    pdf.set_font("Helvetica", "B", 22); pdf.set_x(left)
    pdf.cell(usable, 10, C.HEADER["name"], new_x="LMARGIN", new_y="NEXT"); pdf.ln(1)
    pdf.set_font("Helvetica", "", 10); pdf.set_text_color(80, 80, 80); pdf.set_x(left)
    pdf.cell(usable, 5, f'{C.HEADER["city"]}  |  {C.HEADER["email"]}', new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2); pdf.set_draw_color(0, 0, 0); pdf.set_line_width(0.5)
    pdf.line(left, pdf.get_y(), 215.9 - right, pdf.get_y()); pdf.ln(5)

    pdf.set_font("Helvetica", "", 11); pdf.set_x(left)
    pdf.cell(usable, 6, date.today().strftime("%B %d, %Y"), new_x="LMARGIN", new_y="NEXT"); pdf.ln(3)
    for line in [t.get("company", ""), f'Re: {t.get("job_title", "")}']:
        pdf.set_x(left); pdf.cell(usable, 5.5, line, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_x(left); pdf.cell(usable, 6, "Dear Hiring Team,", new_x="LMARGIN", new_y="NEXT"); pdf.ln(3)

    for p in paras:
        pdf.set_font("Helvetica", "", 10.5); pdf.set_x(left)
        pdf.multi_cell(usable, 4.9, p, new_x="LMARGIN", new_y="NEXT"); pdf.ln(2.0)

    pdf.set_font("Helvetica", "", 10.5); pdf.set_x(left)
    pdf.cell(usable, 6, "Respectfully,", new_x="LMARGIN", new_y="NEXT"); pdf.ln(5)
    pdf.set_font("Helvetica", "B", 10.5); pdf.set_x(left)
    pdf.cell(usable, 6, C.HEADER["name"], new_x="LMARGIN", new_y="NEXT")

    os.makedirs("out", exist_ok=True)
    out = f"out/cover_{key}.pdf"
    pdf.output(out)
    print(f"wrote {out}  ({pdf.page_no()} pages)")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "cloud_security")
