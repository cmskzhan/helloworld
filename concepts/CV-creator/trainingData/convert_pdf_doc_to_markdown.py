#!/usr/bin/env python3
"""Convert CV PDF/DOC/DOCX files to Markdown.

Usage: run the script with `--source` (glob or dir) and `--outdir`.
It prefers system tools: `pdftotext`, `pandoc`, `soffice` (libreoffice), `antiword`.
If not available, falls back to Python libraries (`PyPDF2`, `python-docx`) when installed.
"""

from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path


def is_tool(name: str) -> bool:
	return shutil.which(name) is not None


def run_cmd(args, capture=False, check=False):
	try:
		if capture:
			return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check, text=True)
		else:
			return subprocess.run(args, check=check)
	except Exception as e:
		return None


def convert_pdf_to_md(src: Path, dst: Path) -> bool:
	if is_tool("pdftotext"):
		res = run_cmd(["pdftotext", str(src), "-"], capture=True)
		if res and res.stdout:
			dst.write_text(res.stdout)
			return True
	try:
		from PyPDF2 import PdfReader

		reader = PdfReader(str(src))
		texts = []
		for p in reader.pages:
			try:
				texts.append(p.extract_text() or "")
			except Exception:
				pass
		dst.write_text("\n\n".join(texts))
		return True
	except Exception:
		return False


def convert_docx_to_md(src: Path, dst: Path) -> bool:
	if is_tool("pandoc"):
		res = run_cmd(["pandoc", str(src), "-o", str(dst)])
		return res is not None and res.returncode == 0
	try:
		from docx import Document

		doc = Document(str(src))
		parts = []
		for p in doc.paragraphs:
			text = p.text.strip()
			if not text:
				parts.append("")
			else:
				parts.append(text)
		dst.write_text("\n\n".join(parts))
		return True
	except Exception:
		return False


def convert_doc_to_md(src: Path, dst: Path, tmpdir: Path) -> bool:
	if is_tool("soffice"):
		# convert to docx with libreoffice
		res = run_cmd(["soffice", "--headless", "--convert-to", "docx", "--outdir", str(tmpdir), str(src)])
		if res is not None:
			converted = tmpdir / (src.stem + ".docx")
			if converted.exists():
				return convert_docx_to_md(converted, dst)
	if is_tool("antiword"):
		res = run_cmd(["antiword", str(src)], capture=True)
		if res and res.stdout:
			dst.write_text(res.stdout)
			return True
	return False


def ensure_outdir(path: Path):
	path.mkdir(parents=True, exist_ok=True)


def find_files(sources) -> list[Path]:
	out = []
	for s in sources:
		expanded = sorted(glob.glob(s))
		for p in expanded:
			pth = Path(p)
			if pth.is_dir():
				for ext in ("*.pdf", "*.doc", "*.docx"):
					out += list(pth.rglob(ext))
			else:
				if pth.suffix.lower() in (".pdf", ".doc", ".docx"):
					out.append(pth)
	return [Path(x) for x in sorted(set(out))]


def main(argv=None):
	p = argparse.ArgumentParser(description="Convert CV PDF/DOC/DOCX to Markdown")
	p.add_argument("--source", "-s", nargs="+", default=["/Users/kai/Library/CloudStorage/OneDrive-Personal/Documents/CV*"], help="Source file(s)/globs or directories")
	p.add_argument("--outdir", "-o", default="converted_CVs", help="Output directory")
	p.add_argument("--dry-run", action="store_true")
	args = p.parse_args(argv)

	outdir = Path(args.outdir)
	ensure_outdir(outdir)

	files = find_files(args.source)
	if not files:
		print("No matching files found for:", args.source)
		return 1

	tmpdir = outdir / ".tmp"
	ensure_outdir(tmpdir)

	summary = {"converted": [], "failed": []}
	for f in files:
		rel = f.name
		dest = outdir / (f.stem + ".md")
		print(f"Processing: {f} -> {dest}")
		if args.dry_run:
			continue
		ok = False
		if f.suffix.lower() == ".pdf":
			ok = convert_pdf_to_md(f, dest)
		elif f.suffix.lower() == ".docx":
			ok = convert_docx_to_md(f, dest)
		elif f.suffix.lower() == ".doc":
			ok = convert_doc_to_md(f, dest, tmpdir)
		if ok:
			summary["converted"].append(str(dest))
		else:
			summary["failed"].append(str(f))

	if tmpdir.exists():
		try:
			shutil.rmtree(tmpdir)
		except Exception:
			pass

	print("\nSummary:")
	print("Converted:")
	for c in summary["converted"]:
		print(" -", c)
	if summary["failed"]:
		print("Failed to convert:")
		for f in summary["failed"]:
			print(" -", f)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

