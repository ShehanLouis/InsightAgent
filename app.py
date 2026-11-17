import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("superstore_clean.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Order Month"] = pd.to_datetime(df["Order Month"])
    return df

df = load_data()

st.title("Superstore Sales & Profitability Dashboard")

# --- Sidebar filters ---
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", options=df["Region"].unique(), default=list(df["Region"].unique()))
categories = st.sidebar.multiselect("Category", options=df["Category"].unique(), default=list(df["Category"].unique()))
date_range = st.sidebar.date_input(
    "Order Date range",
    [df["Order Date"].min(), df["Order Date"].max()]
)

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered = df[
        (df["Region"].isin(regions)) &
        (df["Category"].isin(categories)) &
        (df["Order Date"] >= pd.to_datetime(start_date)) &
        (df["Order Date"] <= pd.to_datetime(end_date))
    ]
else:
    st.warning("Please select both a start and end date in the date filter.")
    st.stop()

if filtered.empty:
    st.info("No data found for the selected filters. Please adjust your selection.")
    st.stop()


# --- KPIs ---
col1, col2, col3, col4, col5 = st.columns(5)
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
margin = total_profit / total_sales if total_sales else 0
avg_order = filtered.groupby("Order ID")["Sales"].sum().mean()

col1.metric("Total Sales", f"${total_sales/1e6:.2f}M")
col2.metric("Total Profit", f"${total_profit/1e3:.0f}K")
col3.metric("Profit Margin", f"{margin*100:.1f}%")
col4.metric("Avg Order Value", f"${avg_order:,.0f}" if not np.isnan(avg_order) else "—")
col5.metric("Orders", f"{filtered['Order ID'].nunique():,}")

# --- Monthly trend ---
st.subheader("Monthly Sales Trend")
monthly = filtered.groupby("Order Month")["Sales"].sum().reset_index()
st.line_chart(monthly.set_index("Order Month"))

# --- Category & Region ---
c1, c2 = st.columns(2)
with c1:
    st.subheader("Sales vs Profit by Category")
    by_category = filtered.groupby("Category")[["Sales", "Profit"]].sum()
    st.bar_chart(by_category)
with c2:
    st.subheader("Sales by Region")
    by_region = filtered.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    st.bar_chart(by_region)

# --- Discount vs margin ---
st.subheader("Avg Profit Margin by Discount Band")
filtered = filtered.copy()
filtered["Profit Margin"] = filtered["Profit"] / filtered["Sales"]
bins = pd.cut(filtered["Discount"], bins=[-0.01, 0, 0.1, 0.2, 0.3, 1],
              labels=["0%", "0-10%", "10-20%", "20-30%", "30%+"])
discount_profit = filtered.groupby(bins, observed=True)["Profit Margin"].mean()
st.bar_chart(discount_profit)

# --- Raw data ---
with st.expander("View raw data"):
    st.dataframe(filtered)