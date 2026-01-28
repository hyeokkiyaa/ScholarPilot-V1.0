from fastapi import APIRouter
from app.api import projects, papers, columns, analysis, export, settings, results

api_router = APIRouter()

api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(columns.router, tags=["columns"]) # Path prefix handled inside router for some
api_router.include_router(papers.router, tags=["papers"])
api_router.include_router(results.router, tags=["results"])
api_router.include_router(analysis.router, tags=["analysis"])
api_router.include_router(export.router, tags=["export"])
