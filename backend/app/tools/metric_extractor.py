import json
from app.tools.base import BaseTool

class MetricExtractor(BaseTool):
    name = "metric_extractor"
    description = "Extracts evaluation metrics and results"
    
    async def run(self, paper_content: str, **kwargs) -> dict:
        prompt = """
Analyze the paper to extract quantitative evaluation metrics and results.
Focus on tables and the "Experiments" or "Results" sections.

Return a JSON object with strictly two keys:
1. "metrics": A list of strings, naming the metrics used (e.g. "Accuracy", "F1 Score", "BLEU").
2. "results": An object where keys are the metric names and values are the specific scores/values reported in the paper. 
   - Ensure you extract the VALUES (numbers, percentages), not just the names.
   - If multiple models are compared, provide the best result or the main proposed method's result.
   - Example format: {{ "Accuracy": "94.5%", "Inference Time": "12ms" }}

Paper content:
{content}

Return ONLY valid JSON:
""".format(content=paper_content[:15000])
        
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
