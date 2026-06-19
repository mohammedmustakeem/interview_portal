import fitz  # PyMuPDF
from practice.Tech.engines.resume_engine import ResumeParser

class PDFTextExtractor:

    @staticmethod
    def extract_text(file_path: str) -> str:
        text = ""

        doc = fitz.open(file_path)

        for page in doc:
            text += page.get_text("text")

        doc.close()

        return text
    
    
# data = ResumeParser()

# text = PDFTextExtractor.extract_text("practice\Tech\engines\Thasin_Resume.pdf")
# print(text)

# print(data.parse(text))
