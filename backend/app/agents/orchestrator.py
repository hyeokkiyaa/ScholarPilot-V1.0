from typing import List, Dict, Any
from app.tools.registry import TOOL_REGISTRY
from app.adapters.model_adapter import BaseModelAdapter
from app.models.column import ColumnDef
# from app.models.result import Result

class OrchestratorAgent:
    def __init__(self, model: BaseModelAdapter):
        self.model = model
    
    async def analyze_paper(self, paper_content: str, columns: List[ColumnDef]) -> Dict[str, Any]:
        """
        Analyze paper content using the specified columns/tools.
        Returns dict mapping column_id to result.
        """
        results = {}
        
        for column in columns:
            try:
                tool_class = TOOL_REGISTRY.get(column.tool_name)
                
                if not tool_class:
                    results[column.id] = {
                        "status": "error",
                        "value": None,
                        "error_message": f"Unknown tool: {column.tool_name}"
                    }
                    continue
                
                tool = tool_class(self.model)
                
                # Handle custom prompt tool
                if column.tool_name == "custom_prompt":
                    value = await tool.run(paper_content, custom_prompt=column.custom_prompt)
                else:
                    value = await tool.run(paper_content)
                
                results[column.id] = {
                    "status": "done",
                    "value": value,
                    "error_message": None
                }
                
            except Exception as e:
                results[column.id] = {
                    "status": "error",
                    "value": None,
                    "error_message": str(e)
                }
        
        return results
    
    async def analyze_single_column(self, paper_content: str, column: ColumnDef) -> Dict[str, Any]:
        """Analyze a single column (for retry functionality)"""
        try:
            tool_class = TOOL_REGISTRY.get(column.tool_name)
            
            if not tool_class:
                return {
                    "status": "error",
                    "value": None,
                    "error_message": f"Unknown tool: {column.tool_name}"
                }
            
            tool = tool_class(self.model)
            
            if column.tool_name == "custom_prompt":
                value = await tool.run(paper_content, custom_prompt=column.custom_prompt)
            else:
                value = await tool.run(paper_content)
            
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
