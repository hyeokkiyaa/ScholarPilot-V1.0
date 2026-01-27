from typing import Dict, Any, List
import httpx
from app.models.paper import Paper
from app.models.project import Project

class NotionExporter:
    def __init__(self, api_key: str, database_id: str):
        self.api_key = api_key
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    async def test_connection(self) -> bool:
        """Verify we can access the database"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/databases/{self.database_id}",
                    headers=self.headers
                )
                return response.status_code == 200
        except Exception as e:
            print(f"Notion connection error: {e}")
            return False

    async def export_paper(self, paper: Paper, project: Project) -> bool:
        """Create a page in the notion database for the paper"""
        properties = {
            "Name": {"title": [{"text": {"content": paper.title or "Untitled"}}]},
            "Status": {"select": {"name": paper.status}},
        }
        
        # Add source URL if present
        if paper.source_url:
            properties["URL"] = {"url": paper.source_url}
            
        # Add dynamic column values
        column_map = {col.id: col.name for col in project.columns}
        
        if paper.results:
            for col_id, col_name in column_map.items():
                result = paper.results.get(col_id)
                if result and result.value:
                    # Notion has strict property type rules. 
                    # For simplicity, we'll try to map everything to Rich Text first.
                    # A robust implementation would check the column type/tool and map to specific Notion types (Select, Number, etc.)
                    
                    content_str = str(result.value)
                    if len(content_str) > 2000:
                         content_str = content_str[:1997] + "..."
                         
                    properties[col_name] = {
                        "rich_text": [{"text": {"content": content_str}}]
                    }
        
        # Payload
        data = {
            "parent": {"database_id": self.database_id},
            "properties": properties
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/pages",
                    headers=self.headers,
                    json=data
                )
                if response.status_code != 200:
                    print(f"Failed to create Notion page: {response.text}")
                    return False
                return True
        except Exception as e:
            print(f"Notion export error: {e}")
            return False
