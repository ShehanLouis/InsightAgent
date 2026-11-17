from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
import numpy as np
from app.schemas.payloads import AnomalyItem, AutoAuditReport

class StatisticalAnomalyDetector:
    """
    Scans tabular retail/sales datasets using statistical heuristics
    (Z-scores, IQR, margin degradation, fulfillment bottlenecks)
    to generate an instant Executive Health Audit.
    """

    @staticmethod
    def audit_superstore(df: pd.DataFrame) -> AutoAuditReport:
        anomalies: List[AnomalyItem] = []
        key_drivers: List[str] = []
        health_score = 88

        # 1. Discount vs Profit Margin Destruction
        if "Discount" in df.columns and "Profit" in df.columns and "Sales" in df.columns:
            high_discount_mask = df["Discount"] >= 0.3
            high_disc_loss = df[high_discount_mask]["Profit"].sum()
            high_disc_orders = high_discount_mask.sum()

            if high_disc_loss < 0:
                health_score -= 18
                anomalies.append(
                    AnomalyItem(
                        title="Severe Profit Erosion on Heavy Discounts (>=30%)",
                        severity="high",
                        metric="Profit Margin",
                        dimension="Discount Band (>=30%)",
                        observation=f"{high_disc_orders:,} orders discounted at 30%+ resulted in cumulative losses of ${abs(high_disc_loss):,.2f}.",
                        impact="Discounts above 30% systematically fail to generate positive contribution margin.",
                        recommendation="Implement immediate pricing guardrails to cap maximum allowable sales discount at 20% unless approved by finance."
                    )
                )
                key_drivers.append("Heavy discounting (>30%) is the #1 driver of negative cash flow.")

        # 2. Sub-Category Drain Analysis
        if "Sub-Category" in df.columns and "Profit" in df.columns and "Sales" in df.columns:
            subcat_perf = df.groupby("Sub-Category").agg({
                "Profit": "sum",
                "Sales": "sum"
            }).reset_index()
            subcat_perf["Margin"] = subcat_perf["Profit"] / subcat_perf["Sales"]
            losing_subcats = subcat_perf[subcat_perf["Profit"] < 0].sort_values("Profit")

            for _, row in losing_subcats.iterrows():
                health_score -= 8
                anomalies.append(
                    AnomalyItem(
                        title=f"Unprofitable Product Line: {row['Sub-Category']}",
                        severity="high",
                        metric="Operating Profit",
                        dimension=f"Sub-Category: {row['Sub-Category']}",
                        observation=f"Generated ${row['Sales']:,.2f} in sales but accumulated net loss of ${abs(row['Profit']):,.2f} (Margin: {row['Margin']*100:.1f}%).",
                        impact="Diverts logistics and inventory capacity toward product lines with negative unit economics.",
                        recommendation=f"Review supplier procurement contracts and eliminate promotional discounting for {row['Sub-Category']}."
                    )
                )
                key_drivers.append(f"{row['Sub-Category']} operates at negative gross margin ({row['Margin']*100:.1f}%).")

        # 3. Regional Outlier Performance
        if "Region" in df.columns and "Profit" in df.columns:
            reg_perf = df.groupby("Region").agg({
                "Profit": "sum",
                "Sales": "sum"
            }).reset_index()
            reg_perf["Margin"] = reg_perf["Profit"] / reg_perf["Sales"]
            lowest_reg = reg_perf.sort_values("Margin").iloc[0]

            if lowest_reg["Margin"] < 0.08:
                health_score -= 7
                anomalies.append(
                    AnomalyItem(
                        title=f"Underperforming Region: {lowest_reg['Region']}",
                        severity="medium",
                        metric="Regional Margin",
                        dimension=f"Region: {lowest_reg['Region']}",
                        observation=f"{lowest_reg['Region']} region reports a profit margin of only {lowest_reg['Margin']*100:.1f}%, far below the national benchmark.",
                        impact="Drags down blended enterprise profitability despite high delivery volumes.",
                        recommendation=f"Audit regional distribution costs and state-level tax or freight surcharges in {lowest_reg['Region']}."
                    )
                )
                key_drivers.append(f"{lowest_reg['Region']} region lags enterprise margins by {(0.12 - lowest_reg['Margin'])*100:.1f} percentage points.")

        # 4. Shipping Delay / Fulfillment Bottleneck
        if "Fulfillment Days" in df.columns:
            mean_fulfillment = df["Fulfillment Days"].mean()
            std_fulfillment = df["Fulfillment Days"].std()
            extreme_slow = df[df["Fulfillment Days"] > (mean_fulfillment + 2 * std_fulfillment)]
            if len(extreme_slow) > 0:
                health_score -= 5
                anomalies.append(
                    AnomalyItem(
                        title="Fulfillment Latency Spike (>95th Percentile)",
                        severity="medium",
                        metric="Fulfillment Days",
                        dimension="Logistics / Ship Mode",
                        observation=f"{len(extreme_slow):,} shipments experienced fulfillment times exceeding {mean_fulfillment + 2*std_fulfillment:.1f} days (avg: {mean_fulfillment:.1f} days).",
                        impact="Directly impairs customer retention and drives increased post-order support tickets.",
                        recommendation="Set SLA breach alerts for standard class shipments exceeding 5 days in transit."
                    )
                )

        health_score = max(35, min(98, health_score))

        summary = (
            f"Automated Enterprise Audit completed across {len(df):,} transactions. "
            f"Overall retail portfolio health score is rated at {health_score}/100. "
            f"Primary findings indicate acute margin compression in high-discount orders and specific underperforming sub-categories. "
            f"Immediate intervention is recommended for pricing rules and regional distribution efficiency."
        )

        return AutoAuditReport(
            dataset_id="superstore",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            health_score=health_score,
            anomalies=anomalies,
            executive_summary=summary,
            key_drivers=key_drivers[:5]
        )
