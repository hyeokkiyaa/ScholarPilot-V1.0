from app.tools.base import BaseTool

class RelatedWorkSummarizer(BaseTool):
    name = "related_work_summarizer"
    description = "Summarizes related work section"
    
    async def run(self, paper_content: str, **kwargs) -> str:
        prompt = """
Summarize the related work discussed in this paper.
Format the output in Markdown using bold headers and bullet points.
Structure the summary exactly as follows:

### **Key Themes**
*   **[Theme/Category Name]**: [Brief summary of work in this area]
*   **[Theme/Category Name]**: [Brief summary of work in this area]

### **Differentiation**
[Explanation of how this paper differs from or builds upon the related work]

Paper content:
{content}
""".format(content=paper_content[:12000])
        
        return await self.model.complete(prompt, self.get_system_prompt())
