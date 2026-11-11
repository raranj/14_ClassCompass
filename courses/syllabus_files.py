from pathlib import Path

from bs4 import BeautifulSoup
from docx import Document
from pypdf import PdfReader


MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_TEXT_LENGTH = 20000
MAX_PDF_PAGES = 60

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".html",
    ".htm",
}


def extract_syllabus_file(uploaded_file):
    """
    Extract plain text from an uploaded PDF,
    DOCX, or HTML syllabus.
    """

    extension = Path(uploaded_file.name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. Upload PDF, DOCX, or HTML."
        )

    if uploaded_file.size > MAX_FILE_SIZE:
        raise ValueError(
            "File is too large. Maximum size is 5 MB."
        )

    try:
        uploaded_file.seek(0)

        if extension == ".pdf":
            # Read text from PDF pages.
            reader = PdfReader(uploaded_file)

            if reader.is_encrypted:
                raise ValueError(
                    "Password-protected PDFs are not supported."
                )

            if len(reader.pages) > MAX_PDF_PAGES:
                raise ValueError(
                    "PDF exceeds the 60-page limit."
                )

            parts = [
                page.extract_text() or ""
                for page in reader.pages
            ]

            text = "\n".join(parts)

        elif extension == ".docx":
            # Read paragraphs and tables from Word files.
            document = Document(uploaded_file)

            parts = [
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            for table in document.tables:
                for row in table.rows:
                    parts.append(
                        " | ".join(
                            cell.text for cell in row.cells
                        )
                    )

            text = "\n".join(parts)

        else:
            # Read visible content from HTML files.
            html = uploaded_file.read().decode(
                "utf-8-sig",
                errors="replace"
            )

            soup = BeautifulSoup(html, "html.parser")

            for tag in soup([
                "script", "style", "noscript",
                "head", "svg", "iframe"
            ]):
                tag.decompose()

            text = soup.get_text(separator="\n")

    except ValueError:
        raise

    except Exception as exc:
        raise ValueError(
            "Could not read this file. "
            "Check that it is a valid, unprotected document."
        ) from exc

    # Remove empty lines and excess whitespace.
    cleaned_lines = [
        " ".join(line.split())
        for line in text.splitlines()
        if line.strip()
    ]

    text = "\n".join(cleaned_lines)

    if not text:
        raise ValueError(
            "No readable text found. "
            "Scanned PDFs may require OCR."
        )

    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(
            "The extracted text exceeds 20,000 characters. "
            "Upload a shorter syllabus or paste a relevant section."
        )

    return text
