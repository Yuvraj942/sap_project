import pandas as pd
import streamlit as st

st.set_page_config(page_title="SAP P2P Analytics", page_icon="📊", layout="wide")

st.title("SAP P2P Analytics Dashboard")
st.caption("Working prototype built on capstone sample data")

DATA_PATH = "data/p2p_sample_transactions.csv"

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    date_cols = ["pr_date", "po_date", "gr_date", "invoice_date", "payment_date"]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"Data file not found: {DATA_PATH}")
    st.stop()

# KPI calculations
cycle_df = df.copy()
cycle_df["pr_to_po_days"] = (cycle_df["po_date"] - cycle_df["pr_date"]).dt.days
cycle_df["po_to_gr_days"] = (cycle_df["gr_date"] - cycle_df["po_date"]).dt.days
cycle_df["gr_to_invoice_days"] = (cycle_df["invoice_date"] - cycle_df["gr_date"]).dt.days
cycle_df["invoice_to_payment_days"] = (cycle_df["payment_date"] - cycle_df["invoice_date"]).dt.days

total_po_value = float(cycle_df["po_value"].sum())
avg_pr_to_po = float(cycle_df["pr_to_po_days"].mean())
avg_po_to_gr = float(cycle_df["po_to_gr_days"].mean())
avg_invoice_to_payment = float(cycle_df["invoice_to_payment_days"].mean())
on_time_rate = float(cycle_df["on_time_flag"].mean() * 100)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total PO Value", f"INR {total_po_value:,.0f}")
col2.metric("Avg PR->PO Days", f"{avg_pr_to_po:.2f}")
col3.metric("Avg PO->GR Days", f"{avg_po_to_gr:.2f}")
col4.metric("Avg Inv->Pay Days", f"{avg_invoice_to_payment:.2f}")
col5.metric("Vendor On-Time Rate", f"{on_time_rate:.1f}%")

st.subheader("Vendor Performance")
vendor_summary = (
    cycle_df.groupby("vendor_id", as_index=False)
    .agg(
        total_transactions=("transaction_id", "count"),
        total_po_value=("po_value", "sum"),
        avg_pr_to_po_days=("pr_to_po_days", "mean"),
        avg_po_to_gr_days=("po_to_gr_days", "mean"),
        on_time_rate_pct=("on_time_flag", lambda s: s.mean() * 100),
    )
    .sort_values(by="total_po_value", ascending=False)
)
st.dataframe(vendor_summary, use_container_width=True)

st.subheader("Monthly Spend Trend")
monthly = cycle_df.copy()
monthly["month"] = monthly["po_date"].dt.to_period("M").astype(str)
monthly_spend = monthly.groupby("month", as_index=False)["po_value"].sum()
monthly_spend = monthly_spend.sort_values("month")

# Line charts look blank when only one month exists; use bar chart in that case.
if len(monthly_spend) <= 1:
    st.bar_chart(monthly_spend.set_index("month"))
    st.caption("Only one month is present in sample data, so bar view is shown for clarity.")
else:
    st.line_chart(monthly_spend.set_index("month"))

st.subheader("Raw Transaction Data")
st.dataframe(cycle_df, use_container_width=True)
