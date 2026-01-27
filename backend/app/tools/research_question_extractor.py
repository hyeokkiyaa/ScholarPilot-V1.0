import json
from app.tools.base import BaseTool

class ResearchQuestionExtractor(BaseTool):
    name = "research_question_extractor"
    description = "Extracts research questions"
    
    async def run(self, paper_content: str, **kwargs) -> list:
        prompt = """
Extract the research questions (RQs) from this paper.
Return as JSON array of strings in format "RQ1: ..."

If no explicit RQs are stated, infer the main research questions addressed.

Paper content:
{content}

Research questions (JSON array):
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
