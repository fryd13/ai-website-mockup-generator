from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import logging
from pathlib import Path
from config import settings
from routes.mockup import router as mockup_router
import json

# Logging configuration

LOG_FILE=f"{settings.LOG_DIR}/main.log"

logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Inicialize Fast API APP
app = FastAPI(
    title="Website Mockup Generator API",
    description="API do generowania mockupów stron internetowych za pomocą AI",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

#Middleware for restricting IPs to allowed connections (in my case, only the frontend server)
@app.middleware("http")
async def ip_allow(req: Request, call_next):
    if req.client.host not in settings.ALLOWED_IPS:
        return JSONResponse(status_code=403, content={"detail": "Access denied"})
    return await call_next(req)

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


# Mount dir for mockups 
# The directory is automatically created if it doesn't exist
mockups_path = Path(settings.IMAGE_STORAGE_PATH)
mockups_path.mkdir(parents=True, exist_ok=True)
app.mount("/mockups", StaticFiles(directory=str(mockups_path)), name="mockups")

#router with endpoints - routes/mockup.py
app.include_router(mockup_router)


@app.get("/")
async def root():
    return {
        "message": "Website Mockup Generator API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )