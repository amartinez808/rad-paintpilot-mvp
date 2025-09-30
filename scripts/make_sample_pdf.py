from pathlib import Path

# Tiny placeholder PDF so the CLI has an input file path for the demo
pdf_bytes = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<<>>\n%%EOF\n"

out = Path("data/sample_plans/office_2ndfloor.pdf")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(pdf_bytes)
print(f"Created placeholder PDF at: {out.resolve()}")
