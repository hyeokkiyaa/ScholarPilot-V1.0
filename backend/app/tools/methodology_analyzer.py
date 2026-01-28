from app.tools.base import BaseTool

class MethodologyAnalyzer(BaseTool):
    name = "methodology_analyzer"
    description = "Analyzes the methodology and approach"
    
    async def run(self, paper_content: str, **kwargs) -> str:
        prompt = """
Analyze the methodology of this research paper.
Format the output in Markdown using bold headers and bullet points.
Structure the analysis exactly as follows:

### **Framework Overview**
[Concise description of the overall approach]

### **Key Techniques**
*   **[Technique Name]**: [Brief description]
*   **[Technique Name]**: [Brief description]

### **Evaluation Setup**
[Description of datasets, metrics, or experimental setup]

Paper content:
{content}
""".format(content=paper_content[:12000])
        
        return await self.model.complete(prompt, self.get_system_prompt())
