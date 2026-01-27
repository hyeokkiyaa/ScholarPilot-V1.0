import re
from pathlib import Path
from typing import Tuple, Optional, Any
from app.parsers.pdf_parser import PDFParser
# from app.crawlers.arxiv_crawler import ArxivCrawler # Phase 2 extension
# from app.crawlers.semantic_scholar import SemanticScholarCrawler
# from app.crawlers.link_crawler import LinkCrawler

class InputRouterAgent:
    def __init__(self):
        self.pdf_parser = PDFParser()
        # self.arxiv_crawler = ArxivCrawler()
        # self.semantic_scholar = SemanticScholarCrawler()
        # self.link_crawler = LinkCrawler()
    
    def detect_input_type(self, input_value: str) -> str:
        """Detect the type of input: pdf, arxiv, doi, url, or title"""
        
        # Check if it's a file path (PDF)
        if input_value.endswith('.pdf') or Path(input_value).suffix == '.pdf':
            return "pdf"
        
        # Check if it's an arXiv link
        arxiv_patterns = [
            r'arxiv\.org/abs/(\d+\.\d+)',
            r'arxiv\.org/pdf/(\d+\.\d+)',
            r'arxiv:(\d+\.\d+)'
        ]
        for pattern in arxiv_patterns:
            if re.search(pattern, input_value):
                return "arxiv"
        
        # Check if it's a DOI
        if re.search(r'10\.\d{4,}/[^\s]+', input_value) or 'doi.org' in input_value:
            return "doi"
        
        # Check if it's a URL
        if input_value.startswith('http://') or input_value.startswith('https://'):
            return "url"
        
        # Otherwise, treat as title
        return "title"
    
    async def process(self, input_value: str, pdf_file: Optional[bytes] = None) -> Tuple[Any, str, Optional[str]]:
        """
        Process input and return (content, source_type, error_message)
        """
        
        # If PDF file is directly uploaded
        if pdf_file:
            try:
                content = await self.pdf_parser.parse(pdf_file)
                return content, "pdf", None
            except Exception as e:
                return "", "pdf", f"Failed to parse PDF: {str(e)}"
        
        input_type = self.detect_input_type(input_value)
        
        if input_type == "pdf":
            try:
                with open(input_value, 'rb') as f:
                    content = await self.pdf_parser.parse(f.read())
                return content, "pdf", None
            except Exception as e:
                return "", "pdf", f"Failed to read PDF file: {str(e)}"
        
        # For other types, we need the crawlers which will be implemented in extended tools or later in Phase 2
        # For now, return error or mock
        
        return "", input_type, f"Crawling for {input_type} not implemented yet. Please upload PDF directly."
