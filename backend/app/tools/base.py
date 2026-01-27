from abc import ABC, abstractmethod
from typing import Any, Optional
from app.adapters.model_adapter import BaseModelAdapter

class BaseTool(ABC):
    name: str
    description: str
    
    def __init__(self, model: BaseModelAdapter):
        self.model = model
    
    @abstractmethod
    async def run(self, paper_content: str, **kwargs) -> Any:
        pass
    
    def get_system_prompt(self) -> str:
        return "You are a research paper analyzer. Provide accurate, concise analysis based on the paper content."
