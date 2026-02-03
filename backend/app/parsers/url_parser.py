import httpx
from bs4 import BeautifulSoup
from app.parsers.pdf_parser import PDFParser
import logging

logger = logging.getLogger(__name__)

class URLParser:
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def parse(self, url: str) -> str:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                
                content_type = response.headers.get("content-type", "").lower()
                
                # 1. Direct PDF Link
                if "application/pdf" in content_type or url.endswith(".pdf"):
                    return await self.pdf_parser.parse(response.content)
                
                # 2. HTML Page - Try to find PDF link (Agentic search)
                if "text/html" in content_type:
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    # Heuristic 1: Meta tags (e.g. Google Scholar / Highwire Press tags)
                    pdf_meta = soup.find("meta", {"name": "citation_pdf_url"})
                    if pdf_meta and pdf_meta.get("content"):
                        pdf_url = pdf_meta["content"]
                        logger.info(f"Found PDF via meta tag: {pdf_url}")
                        return await self.parse(pdf_url) # Recursive call
                        
                    # Heuristic 2: arXiv specific
                    if "arxiv.org/abs/" in url:
                        pdf_url = url.replace("/abs/", "/pdf/")
                        logger.info(f"inferred arXiv PDF: {pdf_url}")
                        return await self.parse(pdf_url)

                    # Fallback: Extract text from HTML
                    # Remove scripts and styles
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    text = soup.get_text(separator="\n")
                    # Clean up whitespace
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = '\n'.join(chunk for chunk in chunks if chunk)
                    return text
                    
                raise ValueError(f"Unsupported content type: {content_type}")
                
            except Exception as e:
                logger.error(f"Failed to parse URL {url}: {e}")
                raise e
