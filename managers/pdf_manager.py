import os

from pypdf import PdfReader


class PDFManager:

    def extract_text(self, pdf_path):

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(pdf_path)

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text