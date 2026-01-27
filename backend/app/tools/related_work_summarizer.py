from app.tools.base import BaseTool

class RelatedWorkSummarizer(BaseTool):
    name = "related_work_summarizer"
    description = "Summarizes related work section"
    
    async def run(self, paper_content: str, **kwargs) -> str:
        prompt = """
Summarize the related work discussed in this paper.
Group by category/theme if possible.
Highlight how this paper differs from or builds upon related work.

Paper content:
{content}

Related work summary:
""".format(content=paper_content[:12000])
        
        return await self.model.complete(prompt, self.get_system_prompt())
