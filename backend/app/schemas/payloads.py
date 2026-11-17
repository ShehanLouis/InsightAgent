from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's natural language question or request")
    dataset_id: Optional[str] = Field("default", description="ID of the dataset to analyze")
    api_key: Optional[str] = Field(None, description="Optional runtime Gemini API key")

class CodeExecutionStep(BaseModel):
    step_number: int
    thought: str
    code: str
    output: str
    error: Optional[str] = None
    success: bool

class ChartSpecification(BaseModel):
    chart_type: str = Field(..., description="plotly chart type: bar, line, scatter, pie, heatmap, histogram")
    data: List[Dict[str, Any]]
    layout: Dict[str, Any]

class ChatResponse(BaseModel):
    answer: str
    execution_steps: List[CodeExecutionStep] = []
    chart: Optional[ChartSpecification] = None
    metrics: Dict[str, Any] = {}
    suggested_followups: List[str] = []

class DatasetSummary(BaseModel):
    dataset_id: str
    filename: str
    row_count: int
    column_count: int
    columns: List[str]
    dtypes: Dict[str, str]
    missing_values: Dict[str, int]
    sample_data: List[Dict[str, Any]]
    quick_kpis: Dict[str, Any]

class AnomalyItem(BaseModel):
    title: str
    severity: str  # "high", "medium", "low", "info"
    metric: str
    dimension: str
    observation: str
    impact: str
    recommendation: str

class AutoAuditReport(BaseModel):
    dataset_id: str
    generated_at: str
    health_score: int
    anomalies: List[AnomalyItem]
    executive_summary: str
    key_drivers: List[str]
