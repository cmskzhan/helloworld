from fpdf import FPDF
from io import BytesIO
from docx import Document
import re

class CV_PDF(FPDF):
    def header(self):
        pass

    def _sanitize(self, text):
        replacements = {
            '\u2022': '-', '\u2019': "'", '\u2018': "'", '\u201c': '"', '\u201d': '"',
            '\u2013': '-', '\u2014': '--', '\u2026': '...', '\u00a0': ' ',
        }
        for char, repl in replacements.items():
            text = text.replace(char, repl)
        return text.encode('latin-1', errors='replace').decode('latin-1')

    def _break_long_words(self, text, max_chars=80):
        words = text.split(' ')
        result = []
        for word in words:
            while len(word) > max_chars:
                result.append(word[:max_chars])
                word = word[max_chars:]
            result.append(word)
        return ' '.join(result)

    def safe_write(self, w, h, txt):
        txt = self._sanitize(txt)
        txt = self._break_long_words(txt)
        try:
            self.multi_cell(w=w, h=h, text=txt, new_x="LMARGIN", new_y="NEXT")
        except Exception:
            for chunk in txt.split('\n'):
                self.cell(w=0, h=h, text=chunk[:100], new_x="LMARGIN", new_y="NEXT")

    def print_markdown(self, md_text):
        self.set_font("Helvetica", size=11)
        lines = md_text.split('\n')
        for line in lines:
            if line.startswith('# '):
                self.set_font("Helvetica", 'B', 16)
                self.cell(w=0, h=10, text=self._sanitize(line[2:]), new_x="LMARGIN", new_y="NEXT")
                self.ln(2)
            elif line.startswith('## '):
                self.set_font("Helvetica", 'B', 14)
                self.cell(w=0, h=10, text=self._sanitize(line[3:]), new_x="LMARGIN", new_y="NEXT")
                self.ln(1)
            elif line.startswith('### '):
                self.set_font("Helvetica", 'B', 12)
                self.cell(w=0, h=8, text=self._sanitize(line[4:]), new_x="LMARGIN", new_y="NEXT")
            elif line.startswith('- ') or line.startswith('* '):
                self.set_font("Helvetica", size=11)
                clean_line = line.replace('**', '').replace('__', '')
                self.safe_write(0, 6, f"  - {clean_line[2:]}")
            else:
                self.set_font("Helvetica", size=11)
                clean_line = line.replace('**', '').replace('__', '')
                self.safe_write(0, 6, clean_line)
                if line.strip() == "": self.ln(2)

def create_pdf_bytes(text: str) -> bytes:
    pdf = CV_PDF()
    pdf.set_margin(15)
    pdf.add_page()
    pdf.print_markdown(text)
    return bytes(pdf.output())

def create_docx_bytes(text: str) -> bytes:
    doc = Document()
    for line in text.split('\n'):
        if line.startswith('# '):
            doc.add_heading(line[2:], 0)
        elif line.startswith('## '):
            doc.add_heading(line[3:], 1)
        elif line.startswith('### '):
            doc.add_heading(line[4:], 2)
        else:
            p = doc.add_paragraph()
            parts = re.split(r'(\*\*.*?\*\*)', line)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    p.add_run(part[2:-2]).bold = True
                else:
                    p.add_run(part)
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()
