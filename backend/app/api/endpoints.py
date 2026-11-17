from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
import pandas as pd
import io

from app.schemas.payloads import (
    ChatRequest,
    ChatResponse,
    DatasetSummary,
    AutoAuditReport
)
from app.services.data_service import DataService
from app.services.anomaly_detector import StatisticalAnomalyDetector
from app.agent.analyst import InsightAgent

router = APIRouter()
agent = InsightAgent()

def get_data_service() -> DataService:
    return DataService.get_instance()

@router.get("/health", summary="Service Health Check")
async def health_check():
    return {
        "status": "healthy",
        "service": "InsightAgent API",
        "version": "1.0.0"
    }

@router.get("/dataset/summary", response_model=DatasetSummary, summary="Retrieve Dataset Metadata & KPIs")
async def get_dataset_summary(
    dataset_id: str = "default",
    service: DataService = Depends(get_data_service)
):
    try:
        return service.get_summary(dataset_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate summary: {str(e)}")

@router.post("/dataset/upload", summary="Upload Custom CSV Dataset")
async def upload_dataset(
    file: UploadFile = File(...),
    service: DataService = Depends(get_data_service)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        dataset_id = service.add_custom_dataset(df, file.filename)
        summary = service.get_summary(dataset_id)
        return {
            "message": "Dataset uploaded successfully",
            "dataset_id": dataset_id,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse CSV: {str(e)}")

@router.get("/insights/auto-audit", response_model=AutoAuditReport, summary="Run Instant Statistical Auto-Audit")
async def run_auto_audit(
    dataset_id: str = "default",
    service: DataService = Depends(get_data_service)
):
    df = service.get_dataset(dataset_id)
    report = StatisticalAnomalyDetector.audit_superstore(df)
    return report

@router.post("/chat", response_model=ChatResponse, summary="Submit Question to Autonomous AI Data Analyst")
async def chat_with_data(
    payload: ChatRequest,
    service: DataService = Depends(get_data_service)
):
    df = service.get_dataset(payload.dataset_id or "default")
    response = await agent.analyze(
        question=payload.message,
        df=df,
        api_key=payload.api_key
    )
    return response
