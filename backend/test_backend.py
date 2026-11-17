import fastapi
import google.genai
import plotly
import pandas as pd
import numpy as np
import scipy
from app.services.data_service import DataService
from app.services.anomaly_detector import StatisticalAnomalyDetector
from app.agent.analyst import InsightAgent

ds = DataService.get_instance()
df = ds.get_dataset()
print(f"DataService loaded dataset with {len(df)} rows.")

summary = ds.get_summary()
print("Quick KPIs:", summary.quick_kpis)

audit = StatisticalAnomalyDetector.audit_superstore(df)
print(f"Audit score: {audit.health_score}/100, Anomalies found: {len(audit.anomalies)}")

agent = InsightAgent()
resp = agent._run_analytical_fallback("Show monthly sales and profit trend", df)
print("Fallback Analyst Answer:", resp.answer[:120], "...")
print("Chart generated:", resp.chart.chart_type if resp.chart else None)
print("ALL BACKEND MODULES OPERATIONAL!")
