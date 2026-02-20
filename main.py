from pypdf import PdfWriter

merger = PdfWriter()

pdfs = ["front page synopsis.pdf", "Project Synopsis - REAL-TIME CHAT APP (1).pdf"]
for pdf in pdfs:
    merger.append(pdf)

merger.write("merged.pdf")