from app.tools.base import BaseTool

class Summarizer(BaseTool):
    name = "summarizer"
    description = "Generates 3-5 sentence summary of the paper"
    
    async def run(self, paper_content: str, **kwargs) -> str:
        prompt = """
Provide a concise summary of this research paper in 3-5 sentences.
Focus on: (1) the problem addressed, (2) the proposed approach, (3) key results/contributions.

Paper content:
{content}

Summary:
""".format(content=paper_content[:12000])
        
        return await self.model.complete(prompt, self.get_system_prompt())
