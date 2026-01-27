import json
from app.tools.base import BaseTool

class LimitationFinder(BaseTool):
    name = "limitation_finder"
    description = "Finds limitations and future work"
    
    async def run(self, paper_content: str, **kwargs) -> dict:
        prompt = """
Extract the limitations and future work mentioned in this paper.
Return as JSON with two arrays: "limitations" and "future_work"

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
            return {"limitations": [], "future_work": []}
