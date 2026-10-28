"""한국산학기술학회논문지 투고 원고 빌드: src/manuscript.md -> 워드(.docx)

사용법: python3 build/build.py <판 번호> <YYYY-MM-DD>
예:     python3 build/build.py v1.0 2026-10-24
"""
import re
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt

ROOT = Path(__file__).resolve().parent.parent
LATIN, HANGUL = "Times New Roman", "바탕"


def set_font(style, size, bold=None):
    style.font.name = LATIN
    style.font.size = Pt(size)
    if bold is not None:
        style.font.bold = bold
    rpr = style.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.insert(0, fonts)
    for k in ("w:ascii", "w:hAnsi", "w:cs"):
        fonts.set(qn(k), LATIN)
    fonts.set(qn("w:eastAsia"), HANGUL)
    for k in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        fonts.attrib.pop(qn(k), None)
    color = rpr.find(qn("w:color"))
    if color is not None:
        rpr.remove(color)


def para_style(doc, name, size, bold=None, align=None, before=0, after=4,
               line=1.5, indent_first=None, left=None, right=None):
    styles = doc.styles
    try:
        st = styles[name]
    except KeyError:
        st = styles.add_style(name, 1)
        st.base_style = styles["Normal"]
    set_font(st, size, bold)
    pf = st.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), line
    if align is not None:
        pf.alignment = align
    if indent_first is not None:
        pf.first_line_indent = Pt(indent_first)
    if left is not None:
        pf.left_indent = Mm(left)
    if right is not None:
        pf.right_indent = Mm(right)
    return st


def make_reference(path):
    raw = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                         capture_output=True, check=True).stdout
    path.write_bytes(raw)
    doc = Document(path)
    J, C = WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER
    para_style(doc, "Normal", 10, align=J)
    para_style(doc, "Body Text", 10, align=J, indent_first=10)
    para_style(doc, "First Paragraph", 10, align=J, indent_first=10)
    para_style(doc, "Compact", 8.5, align=WD_ALIGN_PARAGRAPH.LEFT, after=0, line=1.15, indent_first=0)
    para_style(doc, "Title", 16, bold=True, align=C, before=0, after=6, line=1.3)
    para_style(doc, "Subtitle", 12, bold=True, align=C, after=10, line=1.2)
    para_style(doc, "Author", 10, align=C, after=14)
    para_style(doc, "AbstractBody", 9, align=J, after=6, line=1.35, left=8, right=8)
    para_style(doc, "Heading 1", 12, bold=True, before=14, after=6, line=1.3)
    para_style(doc, "Heading 2", 10.5, bold=True, before=8, after=4, line=1.3)
    para_style(doc, "Heading 3", 10, bold=True, before=6, after=3, line=1.3)
    para_style(doc, "Captioned Figure", 10, align=C, after=2)
    para_style(doc, "Bibliography", 9, align=J, after=3, line=1.3)
    for name in ("Heading 1", "Heading 2", "Heading 3", "Title", "Subtitle"):
        doc.styles[name].font.italic = False
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(25)
    sec.top_margin, sec.bottom_margin = Mm(25), Mm(22)
    sec.header_distance, sec.footer_distance, sec.gutter = Mm(12), Mm(12), Mm(0)
    # 바닥글 쪽 번호
    p = sec.footer.paragraphs[0]
    p.alignment = C
    run = p.add_run()
    for tag, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)
    doc.save(path)


def add_table_borders(docx_path):
    doc = Document(docx_path)
    for tbl in doc.tables:
        tblPr = tbl._tbl.tblPr
        borders = OxmlElement("w:tblBorders")
        for edge, sz in (("top", 8), ("bottom", 8), ("insideH", 2), ("insideV", 2),
                         ("left", 0), ("right", 0)):
            el = OxmlElement(f"w:{edge}")
            el.set(qn("w:val"), "single" if sz else "nil")
            el.set(qn("w:sz"), str(sz))
            el.set(qn("w:color"), "000000")
            borders.append(el)
        old = tblPr.find(qn("w:tblBorders"))
        if old is not None:
            tblPr.remove(old)
        tblPr.append(borders)
    # 표·그림 제목은 가운데, 표 주(註)는 작은 글씨
    for p in doc.paragraphs:
        txt = p.text
        if re.match(r"^(Table|Fig\.) \d+\.", txt):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if txt.startswith("Table") else WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Pt(0)
            p.paragraph_format.keep_with_next = txt.startswith("Table")
            for r in p.runs:
                r.font.size = Pt(9)
        elif txt.startswith("주:") or txt.startswith("Note."):
            p.paragraph_format.first_line_indent = Pt(0)
            for r in p.runs:
                r.font.size = Pt(8.5)
        elif re.match(r"^\[\d+\] ", txt):
            # 참고문헌: 번호 뒤 내어쓰기(본문과 같은 10pt)
            p.paragraph_format.left_indent = Pt(24)
            p.paragraph_format.first_line_indent = Pt(-24)
            p.paragraph_format.space_after = Pt(4)
    doc.save(docx_path)


def main():
    ver, date = sys.argv[1], sys.argv[2]
    ref = ROOT / "build" / "reference.docx"
    make_reference(ref)
    out = ROOT / f"DTTM_한국산학기술학회_투고원고_{ver}_{date}.docx"
    subprocess.run(["pandoc", str(ROOT / "src" / "manuscript.md"),
                    "-f", "markdown", "-o", str(out),
                    "--reference-doc", str(ref), "--resource-path", str(ROOT)],
                   check=True)
    add_table_borders(out)
    print(out)


if __name__ == "__main__":
    main()
