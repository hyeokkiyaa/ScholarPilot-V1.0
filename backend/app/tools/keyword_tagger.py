import json
from app.tools.base import BaseTool

class KeywordTagger(BaseTool):
    name = "keyword_tagger"
    description = "Extracts research field, technologies, and keywords"
    
    async def run(self, paper_content: str, **kwargs) -> dict:
        prompt = """
Extract the following from this research paper. Return as JSON only.

- field: List of research fields (e.g., "Machine Learning", "Software Engineering")
- technologies: List of specific technologies/frameworks used
- keywords: List of important keywords/terms

Paper content:
{content}

Return JSON only:
""".format(content=paper_content[:8000])
        
        response = await self.model.complete(prompt, self.get_system_prompt())
        
        try:
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            return json.loads(cleaned)
        except:
            return {"field": [], "technologies": [], "keywords": []}
