import json
from app.tools.base import BaseTool

class MetricExtractor(BaseTool):
    name = "metric_extractor"
    description = "Extracts evaluation metrics and results"
    
    async def run(self, paper_content: str, **kwargs) -> dict:
        prompt = """
Extract evaluation metrics and key results from this paper.
Return as JSON with:
- metrics: list of metric names used
- results: key results as object (metric: value or description)

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
            return {"metrics": [], "results": {}}
