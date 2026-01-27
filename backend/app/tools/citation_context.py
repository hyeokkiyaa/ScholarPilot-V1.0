import json
from app.tools.base import BaseTool

class CitationContext(BaseTool):
    name = "citation_context"
    description = "Extracts key citations and their context"
    
    async def run(self, paper_content: str, **kwargs) -> list:
        prompt = """
Identify the most important citations in this paper (5-10 key references).
For each, provide: citation (author/title), why it's cited, relationship to this work.
Return as JSON array of objects with fields: citation, reason, relationship

Paper content:
{content}

Key citations (JSON array):
""".format(content=paper_content[:12000])
        
        response = await self.model.complete(prompt, self.get_system_prompt())
        
        try:
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            return json.loads(cleaned)
        except:
            return []
