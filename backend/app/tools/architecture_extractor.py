from app.tools.base import BaseTool

class ArchitectureExtractor(BaseTool):
    name = "architecture_extractor"
    description = "Extracts system/model architecture details"
    
    async def run(self, paper_content: str, **kwargs) -> str:
        prompt = """
Describe the system or model architecture presented in this paper.
Include:
1. Main components
2. How components interact
3. Data flow
4. Key design decisions

If no clear architecture is presented, state that.

Paper content:
{content}

Architecture description:
""".format(content=paper_content[:12000])
        
        return await self.model.complete(prompt, self.get_system_prompt())
