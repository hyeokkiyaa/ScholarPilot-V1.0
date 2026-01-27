from typing import List, Dict, Any
from app.tools.registry import TOOL_REGISTRY
from app.adapters.model_adapter import BaseModelAdapter
from app.models.column import ColumnDef
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
# from app.models.result import Result

class OrchestratorAgent:
    def __init__(self, model: BaseModelAdapter):
        self.model = model
    
    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    async def _run_tool_with_retry(self, tool_name: str, paper_content: str, custom_prompt: str = None):
        """Execute a tool with retry logic"""
        tool_class = TOOL_REGISTRY.get(tool_name)
        
        if not tool_class:
            raise ValueError(f"Unknown tool: {tool_name}")
            
        tool = tool_class(self.model)
        
        if tool_name == "custom_prompt":
            return await tool.run(paper_content, custom_prompt=custom_prompt)
        else:
            return await tool.run(paper_content)

    async def analyze_paper(self, paper_content: str, columns: List[ColumnDef]) -> Dict[str, Any]:
        """
        Analyze paper content using the specified columns/tools.
        Returns dict mapping column_id to result.
        """
        results = {}
        
        for column in columns:
            try:
                # Use the retry logic wrapper
                value = await self._run_tool_with_retry(
                    column.tool_name, 
                    paper_content, 
                    custom_prompt=column.custom_prompt
                )
                
                results[column.id] = {
                    "status": "done",
                    "value": value,
                    "error_message": None
                }
                
            except Exception as e:
                # If retries fail, capture the error
                print(f"Failed to analyze col {column.id} after retries: {e}")
                results[column.id] = {
                    "status": "error",
                    "value": None,
                    "error_message": str(e)
                }
        
        return results
    
    async def analyze_single_column(self, paper_content: str, column: ColumnDef) -> Dict[str, Any]:
        """Analyze a single column (for retry functionality)"""
        try:
            value = await self._run_tool_with_retry(
                column.tool_name, 
                paper_content, 
                custom_prompt=column.custom_prompt
            )
            
            return {
                "status": "done",
                "value": value,
                "error_message": None
            }
            
        except Exception as e:
            return {
                "status": "error",
                "value": None,
                "error_message": str(e)
            }

