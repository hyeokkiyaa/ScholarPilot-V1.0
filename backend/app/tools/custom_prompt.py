from app.tools.base import BaseTool

class CustomPromptTool(BaseTool):
    name = "custom_prompt"
    description = "Executes user-defined custom prompt"
    
    async def run(self, paper_content: str, custom_prompt: str = "", **kwargs) -> str:
        if not custom_prompt:
            return "Error: No custom prompt provided"
        
        prompt = """
{custom_prompt}

Paper content:
{content}

Result:
""".format(custom_prompt=custom_prompt, content=paper_content[:12000])
        
        return await self.model.complete(prompt, self.get_system_prompt())
