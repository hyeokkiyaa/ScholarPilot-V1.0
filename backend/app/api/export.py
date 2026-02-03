from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
import pandas as pd
import io
import zipfile
import json

router = APIRouter()

@router.get("/projects/{id}/export/excel")
def export_excel(id: str, db: Session = Depends(get_db)):
    try:
        project, df = _get_project_dataframe(id, db)
        
        # Apply Excel formatting
        df_formatted = df.map(_format_for_excel)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_formatted.to_excel(writer, index=False, sheet_name='Analysis Results')
        output.seek(0)
        
        headers = {
            'Content-Disposition': f'attachment; filename="{project.name}_analysis.xlsx"'
        }
        return StreamingResponse(output, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@router.get("/projects/{id}/export/csv")
def export_csv(id: str, db: Session = Depends(get_db)):
    project, df = _get_project_dataframe(id, db)
    
    # Apply Excel/CSV formatting
    df_formatted = df.map(_format_for_excel)
    
    output = io.StringIO()
    df_formatted.to_csv(output, index=False)
    output.seek(0)
    
    headers = {
        'Content-Disposition': f'attachment; filename="{project.name}_analysis.csv"'
    }
    return StreamingResponse(
        iter([output.getvalue()]), 
        headers=headers, 
        media_type='text/csv'
    )

@router.get("/projects/{id}/export/markdown")
def export_markdown(id: str, db: Session = Depends(get_db)):
    # Export as a zip of markdown files
    project, df = _get_project_dataframe(id, db)
    
    zip_output = io.BytesIO()
    with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 1. Summary Table
        # Format specifically for Markdown Table (using <br> for breaks)
        df_table = df.map(_format_for_markdown_table)
        
        summary_md = f"# {project.name} - Analysis Summary\n\n"
        # Table
        summary_md += df_table.to_markdown(index=False)
        zip_file.writestr("summary.md", summary_md)
        
        # 2. Individual Files
        # For individual files, we can use the raw data to generate rich blocks
        for index, row in df.iterrows():
            paper_title = row.get('Paper', f"paper_{index}")
            filename = f"{_sanitize_filename(str(paper_title))}.md"
            
            content = f"# {paper_title}\n\n"
            for col in df.columns:
                if col == 'Paper': continue
                
                val = row[col]
                formatted_val = _format_for_markdown_block(val)
                content += f"## {col}\n{formatted_val}\n\n"
            
            zip_file.writestr(f"papers/{filename}", content)
            
    zip_output.seek(0)
    headers = {
        'Content-Disposition': f'attachment; filename="{project.name}_markdown.zip"'
    }
    return StreamingResponse(
        zip_output, 
        headers=headers, 
        media_type='application/zip'
    )

def _get_project_dataframe(project_id: str, db: Session):
    from app.models.project import Project
    from app.models.paper import Paper
    from app.models.result import Result
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # Prepare data rows
    data = []
    
    # Get all column names first to ensure order
    # Default columns
    column_names = {col.id: col.name for col in project.columns}
    
    for paper in project.papers:
        row = {'Paper': paper.title or "Untitled"}
        
        # Add metadata if available (basic stuff)
        # row['Status'] = paper.status
        
        # Add dynamic results
        if paper.results:
            # Convert results list to dict for easier lookup
            results_map = {r.column_id: r for r in paper.results}
            
            for col_id, col_name in column_names.items():
                result = results_map.get(col_id)
                value = None # Use None as default value, not empty string, to preserve type
                if result:
                    value = result.value
                row[col_name] = value
        
        data.append(row)
    
    df = pd.DataFrame(data)
    # Ensure all columns exist even if empty
    for col_name in column_names.values():
        if col_name not in df.columns:
            df[col_name] = None 
            
    # Reorder columns: Paper + configured columns
    cols_order = ['Paper'] + [col.name for col in project.columns]
    # Filter only those that exist in df to be safe
    cols_order = [c for c in cols_order if c in df.columns]
    df = df[cols_order]
    
    return project, df

def _format_for_excel(value) -> str:
    """Format complex objects into human-readable strings for Excel (newlines)"""
    if value is None or value == "":
        return ""
        
    if isinstance(value, list):
        if not value: return "-"
        if all(isinstance(x, str) for x in value):
            return ", ".join(value)
        if all(isinstance(x, dict) for x in value):
            items = []
            for item in value:
                name = _extract_name(item)
                if name:
                    details = _extract_details(item)
                    item_str = name + (f" ({', '.join(details)})" if details else "")
                    items.append(item_str)
                else:
                    vals = [str(v) for k,v in item.items() if v]
                    items.append(", ".join(vals))
            return "\n".join(items)
        return str(value)

    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            if v is None or v == "": continue
            str_v = _flatten_value(v)
            lines.append(f"{k}: {str_v}")
        return "\n".join(lines)

    return str(value)

def _format_for_markdown_table(value) -> str:
    """Format for Markdown Tables (uses <br> for breaks, no block elements)"""
    val = _format_for_excel(value) # Reuse logic but replace newlines
    return val.replace("\n", "<br>")

def _format_for_markdown_block(value) -> str:
    """Format for Individual Markdown Files (uses lists, bolding)"""
    if value is None or value == "":
        return "_No data_"
        
    if isinstance(value, list):
        if not value: return "-"
        if all(isinstance(x, str) for x in value):
            return "\n".join([f"- {x}" for x in value])
            
        if all(isinstance(x, dict) for x in value):
            items = []
            for item in value:
                name = _extract_name(item)
                if name:
                    details = _extract_details(item)
                    item_str = f"- **{name}**"
                    if details:
                        item_str += f"\n  - " + "\n  - ".join(details)
                    items.append(item_str)
                else:
                    # Fallback
                    items.append(f"- {str(item)}")
            return "\n".join(items)
    
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            if v is None or v == "": continue
            str_v = _flatten_value(v)
            lines.append(f"- **{k}**: {str_v}")
        return "\n".join(lines)
        
    return str(value)

def _extract_name(item: dict):
    return item.get('name') or item.get('title') or item.get('Title')

def _extract_details(item: dict):
    details = []
    if item.get('size'): details.append(f"Size: {item.get('size')}")
    if item.get('url'): details.append(f"URL: {item.get('url')}")
    return details

def _flatten_value(v):
    if isinstance(v, list): return ", ".join([str(i) for i in v])
    if isinstance(v, dict): return ", ".join([f"{sk}: {sv}" for sk, sv in v.items()])
    return str(v)

def _sanitize_filename(name: str) -> str:
    import re
    return re.sub(r'[\\/*?:"<>|]', "", name)[:50]



@router.post("/projects/{id}/export/notion")
async def export_notion(id: str, db: Session = Depends(get_db)):
    from app.models.project import Project
    from app.models.settings import Settings
    from app.adapters.notion_exporter import NotionExporter
    
    # Get settings
    notion_key_setting = db.query(Settings).filter(Settings.key == "notion_api_key").first()
    notion_db_id_setting = db.query(Settings).filter(Settings.key == "notion_database_id").first()
    
    notion_key = notion_key_setting.value if notion_key_setting else None
    notion_db_id = notion_db_id_setting.value if notion_db_id_setting else None
    
    if not notion_key or not notion_db_id:
         raise HTTPException(status_code=400, detail="Notion credentials not configured in settings")
         
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    exporter = NotionExporter(notion_key, notion_db_id)
    
    # verify connection first
    if not await exporter.test_connection():
        raise HTTPException(status_code=400, detail="Failed to connect to Notion. Check your credentials.")
    
    # Export papers
    success_count = 0
    exported_titles = []
    
    for paper in project.papers:
        try:
            success = await exporter.export_paper(paper, project)
            if success:
                success_count += 1
                exported_titles.append(paper.title)
        except Exception as e:
            print(f"Failed to export paper {paper.id}: {e}")
            
    return {"status": "success", "exported": success_count, "total": len(project.papers), "papers": exported_titles}

@router.post("/test-connection/notion")
async def test_notion_connection(request: dict):
    from app.adapters.notion_exporter import NotionExporter
    api_key = request.get("api_key")
    db_id = request.get("database_id")
    
    if not api_key or not db_id:
        raise HTTPException(status_code=400, detail="Missing api_key or database_id")
        
    exporter = NotionExporter(api_key, db_id)
    if await exporter.test_connection():
        return {"status": "success", "message": "Connection successful"}
    else:
        raise HTTPException(status_code=400, detail="Connection failed")
