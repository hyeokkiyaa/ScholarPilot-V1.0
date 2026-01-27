import json
from app.tools.base import BaseTool

class BaselineExtractor(BaseTool):
    name = "baseline_extractor"
    description = "Extracts baseline methods/systems for comparison"
    
    async def run(self, paper_content: str, **kwargs) -> list:
        prompt = """
Extract all baseline methods, models, or systems that this paper compares against.
Return as JSON array of strings (baseline names).

Paper content:
{content}

Baselines (JSON array):
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
