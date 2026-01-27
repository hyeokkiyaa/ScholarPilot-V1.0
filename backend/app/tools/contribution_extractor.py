import json
from app.tools.base import BaseTool

class ContributionExtractor(BaseTool):
    name = "contribution_extractor"
    description = "Extracts key contributions as a list"
    
    async def run(self, paper_content: str, **kwargs) -> list:
        prompt = """
Extract the main contributions of this paper as a bullet-point list.
Return as JSON array of strings. Typically 3-5 contributions.

Paper content:
{content}

Contributions (JSON array):
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
            return [response]
