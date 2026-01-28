from app.tools.base import BaseTool

class Summarizer(BaseTool):
    name = "summarizer"
    description = "Generates 3-5 sentence summary of the paper"
    
    async def run(self, paper_content: str, **kwargs) -> str:
        prompt = """
Provide a structured summary of this research paper.
Format the output in Markdown using bold headers and bullet points.
Structure the summary exactly as follows:

### **Problem Statement**
[Brief description of the problem being addressed]

### **Proposed Approach**
[Brief description of the solution or methodology]

### **Key Contributions**
*   [Contribution 1]
*   [Contribution 2]
*   [Contribution 3]

Paper content:
{content}
""".format(content=paper_content[:12000])
        
        return await self.model.complete(prompt, self.get_system_prompt())
