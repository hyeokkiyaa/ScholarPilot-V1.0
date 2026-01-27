import json
from app.tools.base import BaseTool

class DatasetExtractor(BaseTool):
    name = "dataset_extractor"
    description = "Extracts dataset information"
    
    async def run(self, paper_content: str, **kwargs) -> list:
        prompt = """
Extract all datasets used in this paper.
For each dataset, provide: name, size (if mentioned), source/url (if mentioned), description
Return as JSON array of objects.

Paper content:
{content}

Datasets (JSON array):
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
