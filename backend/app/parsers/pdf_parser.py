import fitz  # PyMuPDF
from typing import Optional
import io

class PDFParser:
    def __init__(self, max_pages: int = 50):
        self.max_pages = max_pages
    
    async def parse(self, pdf_data: bytes) -> str:
        """Parse PDF and extract text content"""
        try:
            # fitz.open expects bytes or filename. For bytes, use stream.
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            
            text_parts = []
            pages_to_process = min(len(doc), self.max_pages)
            
            for page_num in range(pages_to_process):
                page = doc[page_num]
                text = page.get_text()
                text_parts.append(text)
            
            doc.close()
            
            full_text = "\n\n".join(text_parts)
            
            # Basic cleaning
            full_text = self._clean_text(full_text)
            
            return full_text
            
        except Exception as e:
            raise Exception(f"PDF parsing failed: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        import re
        
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        
        # Remove page numbers (common patterns)
        text = re.sub(r'\n\d+\n', '\n', text)
        
        return text.strip()
    
    async def get_page_count(self, pdf_data: bytes) -> int:
        """Get total page count of PDF"""
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        count = len(doc)
        doc.close()
        return count
