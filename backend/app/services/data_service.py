import os
import uuid
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from app.core.config import settings
from app.schemas.payloads import DatasetSummary

class DataService:
    _instance = None
    _datasets: Dict[str, pd.DataFrame] = {}

    def __init__(self):
        self.load_default_dataset()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_default_dataset(self) -> str:
        candidates = [
            settings.DEFAULT_DATASET_PATH,
            os.path.join(os.getcwd(), "superstore_clean.csv"),
            os.path.join(os.getcwd(), "..", "superstore_clean.csv"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "superstore_clean.csv"),
            "superstore_clean.csv"
        ]
        path = None
        for cand in candidates:
            if cand and os.path.exists(cand):
                path = cand
                break
        
        if not path:
            raise FileNotFoundError(f"Could not locate superstore_clean.csv in candidate locations: {candidates}")

        df = pd.read_csv(path)
        for col in ["Order Date", "Ship Date", "Order Month"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        self._datasets["default"] = df
        return "default"

    def get_dataset(self, dataset_id: str = "default") -> pd.DataFrame:
        if dataset_id not in self._datasets:
            return self._datasets["default"]
        return self._datasets[dataset_id]

    def add_custom_dataset(self, df: pd.DataFrame, filename: str) -> str:
        new_id = str(uuid.uuid4())[:8]
        # Clean datetime columns if present
        for col in df.columns:
            if "date" in col.lower() or "time" in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col], errors="ignore")
                except Exception:
                    pass
        self._datasets[new_id] = df
        return new_id

    def get_summary(self, dataset_id: str = "default") -> DatasetSummary:
        df = self.get_dataset(dataset_id)
        
        # Calculate Quick KPIs if columns exist
        quick_kpis = {}
        if "Sales" in df.columns:
            quick_kpis["total_sales"] = round(float(df["Sales"].sum()), 2)
            quick_kpis["avg_order_value"] = round(float(df.groupby("Order ID")["Sales"].sum().mean()), 2) if "Order ID" in df.columns else round(float(df["Sales"].mean()), 2)
        if "Profit" in df.columns:
            quick_kpis["total_profit"] = round(float(df["Profit"].sum()), 2)
            if "Sales" in df.columns and quick_kpis.get("total_sales", 0) > 0:
                quick_kpis["profit_margin"] = round(float((quick_kpis["total_profit"] / quick_kpis["total_sales"]) * 100), 2)
        if "Order ID" in df.columns:
            quick_kpis["total_orders"] = int(df["Order ID"].nunique())
        if "Customer ID" in df.columns:
            quick_kpis["unique_customers"] = int(df["Customer ID"].nunique())
        
        # Convert dtypes to string
        dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
        missing = {col: int(count) for col, count in df.isnull().sum().items()}
        
        # Sample 10 records, formatted nicely for JSON
        sample_df = df.head(10).copy()
        for col in sample_df.select_dtypes(include=["datetime64[ns]", "datetime64"]).columns:
            sample_df[col] = sample_df[col].dt.strftime("%Y-%m-%d")
        
        # Replace NaN with None
        sample_records = sample_df.replace({np.nan: None}).to_dict(orient="records")

        return DatasetSummary(
            dataset_id=dataset_id,
            filename="superstore_clean.csv" if dataset_id == "default" else f"custom_{dataset_id}.csv",
            row_count=len(df),
            column_count=len(df.columns),
            columns=list(df.columns),
            dtypes=dtypes,
            missing_values=missing,
            sample_data=sample_records,
            quick_kpis=quick_kpis
        )
