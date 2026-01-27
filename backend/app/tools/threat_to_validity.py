import json
from app.tools.base import BaseTool

class ThreatToValidity(BaseTool):
    name = "threat_to_validity"
    description = "Extracts threats to validity (for SE papers)"
    
    async def run(self, paper_content: str, **kwargs) -> dict:
        prompt = """
Extract threats to validity discussed in this paper.
Categorize into: internal_validity, external_validity, construct_validity, conclusion_validity
Return as JSON with these four keys, each containing a list of threats.

If a category is not discussed, return empty list for that category.

Paper content:
{content}

Return JSON only:
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
            return {
                "internal_validity": [],
                "external_validity": [],
                "construct_validity": [],
                "conclusion_validity": []
            }
