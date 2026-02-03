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
            # Convert results list to dict for easier lookup
            results_map = {r.column_id: r for r in paper.results}
            
            for col_id, col_name in column_map.items():
                result = results_map.get(col_id)
                if result and result.value:
                    content_str = self._format_value(result.value)
                     
                    # Notion limit for text content is 2000 chars
                    if len(content_str) > 2000:
                         content_str = content_str[:1997] + "..."
                         
                    properties[col_name] = {
                        "rich_text": [{"text": {"content": content_str}}]
                    }
    
    def _format_value(self, value) -> str:
        """Format complex objects into human-readable strings for Notion"""
        if value is None:
            return ""
            
        if isinstance(value, list):
            # Empty list
            if not value: return "-"
            
            # List of strings
            if all(isinstance(x, str) for x in value):
                return ", ".join(value)
                
            # List of objects
            if all(isinstance(x, dict) for x in value):
                items = []
                for item in value:
                    name = item.get('name') or item.get('title') or item.get('Title')
                    if name:
                        details = []
                        if item.get('size'): details.append(str(item.get('size')))
                        if item.get('url'): details.append(item.get('url'))
                        item_str = name + (f" ({', '.join(details)})" if details else "")
                        items.append(item_str)
                    else:
                         # Fallback
                        vals = [str(v) for k,v in item.items() if v]
                        items.append(", ".join(vals))
                return "\n".join(items)
                
            return str(value)
    
        if isinstance(value, dict):
            # Flatten dictionary
            lines = []
            for k, v in value.items():
                if v is None or v == "": continue
                str_v = str(v)
                if isinstance(v, list):
                    str_v = ", ".join([str(i) for i in v])
                elif isinstance(v, dict):
                    str_v = ", ".join([f"{sk}: {sv}" for sk, sv in v.items()])
                lines.append(f"{k}: {str_v}")
            return "\n".join(lines)
    
        return str(value)
        
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
