import fitz  # PyMuPDF


def read_pdf(file_path: str) -> str:
    """
    Read a PDF file and return its raw extracted text.
    Does not chunk, clean, or embed — just reads.
    """
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text