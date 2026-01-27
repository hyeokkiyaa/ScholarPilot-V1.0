from app.tools.base import BaseTool

class OneSentenceSummary(BaseTool):
    name = "one_sentence_summary"
    description = "Generates a single sentence summary"
    
    async def run(self, paper_content: str, **kwargs) -> str:
        prompt = """
Summarize this research paper in exactly ONE sentence (max 30 words).
Capture the core contribution or finding.

Paper content:
{content}

One sentence summary:
""".format(content=paper_content[:8000])
        
        return await self.model.complete(prompt, self.get_system_prompt())
