import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.endpoints import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Autonomous AI Data Analyst - Enterprise Decision Intelligence & Agentic BI Platform"
)

# Enable CORS for local dev and production frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API endpoints
app.include_router(api_router, prefix="/api")

# Determine frontend directory path
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
index_file = os.path.join(frontend_dir, "index.html")

if os.path.exists(index_file):
    @app.get("/", summary="Serve InsightAgent Web Dashboard")
    async def serve_index():
        return FileResponse(index_file)

    @app.get("/dashboard", summary="Serve InsightAgent Web Dashboard")
    async def serve_dashboard():
        return FileResponse(index_file)
else:
    @app.get("/")
    def root():
        return {
            "system": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "docs_url": "/docs",
            "api_prefix": "/api"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
