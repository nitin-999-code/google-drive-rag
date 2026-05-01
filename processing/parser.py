from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {e}")
            return ""

    if file_path.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error extracting text from TXT {file_path}: {e}")
            return ""

    return ""
