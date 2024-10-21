#Extract PDF
import logging
import fitz


def extract_text_from_pdf(pdf_content: bytes) -> str:
    text = ""
    try:
        with fitz.open(stream=pdf_content, filetype="pdf") as pdf_doc:
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc.load_page(page_num)
                text += page.get_text()
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
    return text