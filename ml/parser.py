import fitz  # PyMuPDF


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF resume using PyMuPDF."""
    try:
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"[parser] Error reading {file_path}: {e}")
        return ""


def extract_text_from_file(file_path: str) -> str:
    """Handle both PDF and TXT files."""
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    raise ValueError(f"Unsupported file type: {file_path}")
