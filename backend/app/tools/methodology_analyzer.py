from app.tools.base import BaseTool

class MethodologyAnalyzer(BaseTool):
    name = "methodology_analyzer"
    description = "Analyzes the methodology and approach"
    
    async def run(self, paper_content: str, **kwargs) -> str:
        prompt = """
Analyze the methodology of this research paper.
Include:
1. Overall approach/framework
2. Key techniques or algorithms used
3. System architecture (if applicable)
4. Evaluation methodology

Keep the analysis concise but comprehensive.

Paper content:
{content}

Methodology analysis:
""".format(content=paper_content[:12000])
        
        return await self.model.complete(prompt, self.get_system_prompt())
