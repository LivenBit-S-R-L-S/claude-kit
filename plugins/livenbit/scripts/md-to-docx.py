#!/usr/bin/env python3
"""Converte un contratto in Markdown in un .docx impaginato.

Usa solo la libreria standard: un .docx e' uno zip di XML, non serve
nessuna dipendenza esterna. Sottoinsieme di Markdown supportato, scelto
su cio' che serve a un contratto:

  # ## ###     titoli
  **grassetto**
  - elenco
  1. elenco numerato
  ---          interruzione di pagina
  |a|b|        tabella
  testo        paragrafo

Uso: md-to-docx.py <input.md> <output.docx>
"""
import re
import sys
import zipfile
from datetime import datetime, timezone
from xml.sax.saxutils import escape

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>"""


def _style(sid, name, size, bold, before, after, outline=None):
    ol = f'<w:outlineLvl w:val="{outline}"/>' if outline is not None else ""
    b = '<w:b/>' if bold else ""
    return (
        f'<w:style w:type="paragraph" w:styleId="{sid}">'
        f'<w:name w:val="{name}"/><w:basedOn w:val="Normal"/>'
        f'<w:pPr><w:keepNext/><w:spacing w:before="{before}" w:after="{after}"/>{ol}</w:pPr>'
        f'<w:rPr>{b}<w:sz w:val="{size}"/></w:rPr></w:style>'
    )


STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {W}>
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/>
</w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal">
<w:name w:val="Normal"/><w:pPr><w:spacing w:after="140" w:line="276" w:lineRule="auto"/>
<w:jc w:val="both"/></w:pPr></w:style>
{_style("Title", "Title", 40, True, 0, 320)}
{_style("Heading1", "heading 1", 30, True, 360, 160, 0)}
{_style("Heading2", "heading 2", 26, True, 280, 140, 1)}
{_style("Heading3", "heading 3", 23, True, 240, 120, 2)}
</w:styles>"""


SETTINGS = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings {W}><w:defaultTabStop w:val="708"/><w:compat/></w:settings>"""


def core_props(title):
    """Metadati mostrati da Word nelle proprieta' del documento."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<cp:coreProperties '
        'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f"<dc:title>{escape(title)}</dc:title>"
        "<dc:creator>LivenBit SRLS</dc:creator>"
        "<cp:lastModifiedBy>LivenBit SRLS</cp:lastModifiedBy>"
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
        "</cp:coreProperties>"
    )


def runs(text):
    """Converte **grassetto** in run Word, lasciando il resto come testo."""
    out = []
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if not part:
            continue
        bold = "<w:b/>" if i % 2 else ""
        out.append(
            f'<w:r><w:rPr>{bold}</w:rPr>'
            f'<w:t xml:space="preserve">{escape(part)}</w:t></w:r>'
        )
    return "".join(out)


def para(text, style=None, numbered=False, bullet=False):
    pr = []
    if style:
        pr.append(f'<w:pStyle w:val="{style}"/>')
    if bullet or numbered:
        pr.append('<w:ind w:left="360" w:hanging="360"/>')
    ppr = f"<w:pPr>{''.join(pr)}</w:pPr>" if pr else ""
    return f"<w:p>{ppr}{runs(text)}</w:p>"


def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def table(rows):
    grid = "".join('<w:gridCol w:w="4500"/>' for _ in rows[0])
    body = ""
    for r, cells in enumerate(rows):
        tcs = ""
        for cell in cells:
            txt = f"**{cell}**" if r == 0 else cell
            tcs += (
                '<w:tc><w:tcPr><w:tcW w:w="4500" w:type="dxa"/></w:tcPr>'
                f'{para(txt)}</w:tc>'
            )
        body += f"<w:tr>{tcs}</w:tr>"
    borders = "".join(
        f'<w:{e} w:val="single" w:sz="4" w:color="999999"/>'
        for e in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    return (
        f'<w:tbl><w:tblPr><w:tblBorders>{borders}</w:tblBorders></w:tblPr>'
        f'<w:tblGrid>{grid}</w:tblGrid>{body}</w:tbl><w:p/>'
    )


def convert(md):
    body, pending, first_h1 = [], [], True
    lines = md.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if re.match(r"^\|.*\|$", line):
            pending = []
            while i < len(lines) and re.match(r"^\|.*\|$", lines[i].rstrip()):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    pending.append(cells)
                i += 1
            if pending:
                body.append(table(pending))
            continue

        if line.strip() in ("---", "***", "___"):
            body.append(page_break())
        elif line.startswith("### "):
            body.append(para(line[4:], "Heading3"))
        elif line.startswith("## "):
            body.append(para(line[3:], "Heading2"))
        elif line.startswith("# "):
            body.append(para(line[2:], "Title" if first_h1 else "Heading1"))
            first_h1 = False
        elif re.match(r"^\s*[-*]\s+", line):
            body.append(para("• " + re.sub(r"^\s*[-*]\s+", "", line), bullet=True))
        elif re.match(r"^\s*\d+[.)]\s+", line):
            body.append(para(line.strip(), numbered=True))
        elif line.strip():
            body.append(para(line.strip()))
        i += 1

    sect = (
        '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1418" w:right="1276" w:bottom="1418" w:left="1276"/></w:sectPr>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f'<w:document {W}><w:body>{"".join(body)}{sect}</w:body></w:document>'
    )


def main():
    if len(sys.argv) != 3:
        sys.exit("Uso: md-to-docx.py <input.md> <output.docx>")
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as fh:
        md = fh.read()
    document = convert(md)
    m = re.search(r"^#\s+(.+)$", md, re.M)
    title = m.group(1).strip() if m else "Documento"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("docProps/core.xml", core_props(title))
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/settings.xml", SETTINGS)
        z.writestr("word/document.xml", document)
    print(f"Scritto {dst}")


if __name__ == "__main__":
    main()
