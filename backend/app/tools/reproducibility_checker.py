import json
from app.tools.base import BaseTool

class ReproducibilityChecker(BaseTool):
    name = "reproducibility_checker"
    description = "Checks code/data availability and reproducibility info"
    
    async def run(self, paper_content: str, **kwargs) -> dict:
        prompt = """
Check reproducibility information in this paper.
Return JSON with:
- code_available: boolean
- code_url: URL if available
- data_available: boolean
- data_url: URL if available
- environment_info: any mentioned environment/setup requirements
- reproducibility_notes: any other relevant info

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
                "code_available": False,
                "code_url": None,
                "data_available": False,
                "data_url": None,
                "environment_info": None,
                "reproducibility_notes": None
            }
