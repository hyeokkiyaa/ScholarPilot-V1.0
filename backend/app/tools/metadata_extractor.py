import json
from app.tools.base import BaseTool

class MetadataExtractor(BaseTool):
    name = "metadata_extractor"
    description = "Extracts title, authors, year, affiliation, and links from paper"
    
    async def run(self, paper_content: str, **kwargs) -> dict:
        prompt = """
Extract the following metadata from this research paper. Return as JSON only, no explanation.

Required fields:
- title: Paper title
- authors: List of author names
- year: Publication year (integer)
- affiliation: Primary institution/organization
- venue: Conference/journal name if mentioned
- github_url: GitHub repository URL if mentioned (null if not found)
- doi: DOI if mentioned (null if not found)

Paper content:
{content}

Return JSON only:
""".format(content=paper_content[:8000])
        
        response = await self.model.complete(prompt, self.get_system_prompt())
        
        try:
            # Clean response and parse JSON
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            return json.loads(cleaned)
        except:
            return {"title": None, "authors": [], "year": None, "affiliation": None}
