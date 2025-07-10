
from fastapi import FastAPI, BackgroundTasks, Request, HTTPException
from fastapi.responses import FileResponse
from app.scraper.engine import run_scraper
from app.models import ScrapeTask, ScrapeResult
from app.database import SessionLocal, engine, Base
from app.schemas import ScrapeRequest, ScrapeResponse, ScrapeResultSchema
from pathlib import Path
from app.logging_config import setup_logging
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import os

setup_logging()
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scrape", response_model=ScrapeResponse)
async def scrape(request: ScrapeRequest, background_tasks: BackgroundTasks):
    db = SessionLocal()
    try:
        task = ScrapeTask(url=request.url, status="queued")
        db.add(task)
        db.commit()
        db.refresh(task)
        background_tasks.add_task(run_scraper, task.id, request.dict())
        return ScrapeResponse(task_id=task.id, status=task.status)
    finally:
        db.close()

@app.get("/result/{task_id}", response_model=ScrapeResultSchema)
async def get_result(task_id: int):
    db = SessionLocal()
    try:
        result = db.query(ScrapeResult).filter(ScrapeResult.task_id == task_id).first()
        if result is None:
            raise HTTPException(status_code=404, detail="Result not found")
        return result
    finally:
        db.close()

@app.get("/tasks")
async def list_tasks():
    db = SessionLocal()
    try:
        return db.query(ScrapeTask).all()
    finally:
        db.close()

@app.get("/download-pdf/{task_id}")
async def download_pdf(task_id: int):
    db = SessionLocal()
    try:
        task = db.query(ScrapeTask).filter(ScrapeTask.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if task.status != "completed":
            raise HTTPException(status_code=400, detail="Task not completed yet")
        reports_dir = Path("reports").resolve()
        
        pdf_files = list(reports_dir.glob(f"scraping_report_{task_id}_*.pdf"))
        
        if not pdf_files:
            raise HTTPException(status_code=404, detail="PDF report not found")
        
        pdf_path = pdf_files[0] 
        
        if not pdf_path.exists():
            raise HTTPException(status_code=404, detail="PDF file not found on disk")
        
        if not pdf_path.is_file():
            raise HTTPException(status_code=400, detail="Path is not a file")
        
        download_filename = f"scraping_report_task_{task_id}.pdf"
        
        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=download_filename,
            headers={
                "Content-Disposition": f"attachment; filename={download_filename}",
                "Cache-Control": "no-cache"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading PDF for task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during PDF download")
    finally:
        db.close()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Web scraping service is running"}
