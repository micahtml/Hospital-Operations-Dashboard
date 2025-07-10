
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Connect to DB
conn = sqlite3.connect("hospital_operations.db")

# Load base data
df_patients = pd.read_sql("SELECT * FROM patients", conn, parse_dates=["admit_date", "discharge_date"])
df_admissions = pd.read_sql("SELECT * FROM admissions", conn)
df_kpis = pd.read_sql("SELECT * FROM kpis", conn)
df_costs = pd.read_sql("SELECT * FROM costs", conn)
df_staffing = pd.read_sql("SELECT * FROM staffing", conn)

# Merge patients and admissions for metrics
df = df_patients.merge(df_admissions, on="patient_id")

# Sidebar Filters
st.sidebar.title("🏥 Filters")
selected_department = st.sidebar.selectbox("Select Department", ["All"] + sorted(df["department"].unique().tolist()))
selected_month = st.sidebar.selectbox("Select Month", ["All"] + sorted(df_kpis["month"].unique()))

# Apply filters
if selected_department != "All":
    df = df[df["department"] == selected_department]
    df_kpis = df_kpis[df_kpis["department"] == selected_department]
    df_costs = df_costs[df_costs["department"] == selected_department]
    df_staffing = df_staffing[df_staffing["department"] == selected_department]

if selected_month != "All":
    df_kpis = df_kpis[df_kpis["month"] == selected_month]
    df_staffing = df_staffing[df_staffing["month"] == selected_month]

# KPIs
st.title("🏥 Hospital Operations Dashboard")
st.markdown("### Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Avg Length of Stay", f"{df['length_of_stay'].mean():.2f} days")
col2.metric("Readmission Rate", f"{(df['readmitted'].sum() / len(df)) * 100:.1f}%")
if not df_kpis.empty:
    col3.metric("Infection Rate", f"{df_kpis['infection_rate_percent'].iloc[0]:.2f}%")

col4, col5, col6 = st.columns(3)
if not df_costs.empty:
    col4.metric("Avg Billing", f"${df_costs['billing_amount'].mean():,.0f}")
if not df_staffing.empty and not df.empty:
    ratio = df_staffing['staff_count'].sum() / len(df) if len(df) > 0 else 0
    col5.metric("Staff-to-Patient Ratio", f"{ratio:.2f}")
col6.metric("Avg Wait Time", f"{df_kpis['avg_wait_time_minutes'].iloc[0]:.1f} min" if not df_kpis.empty else "N/A")

# === Visual Insights Section ===
st.markdown("### 📈 Visual Insights")

df["admit_date"] = pd.to_datetime(df["admit_date"])

# Readmission Rate by Month
readmit_df = df.copy()
readmit_df["month"] = readmit_df["admit_date"].dt.to_period("M").astype(str)
readmit_summary = readmit_df.groupby("month").agg(
    total_admissions=("readmitted", "count"),
    readmissions=("readmitted", "sum")
).reset_index()
readmit_summary["readmission_rate"] = (readmit_summary["readmissions"] / readmit_summary["total_admissions"]) * 100

fig1 = px.line(readmit_summary, x="month", y="readmission_rate",
               title="Monthly Readmission Rate",
               markers=True, labels={"readmission_rate": "Readmission Rate (%)"})
st.plotly_chart(fig1)

# Avg Length of Stay by Department
stay_summary = df.groupby("department").agg(
    avg_stay=("length_of_stay", "mean")
).reset_index()

fig2 = px.bar(stay_summary, x="department", y="avg_stay",
              title="Average Length of Stay by Department",
              labels={"avg_stay": "Avg Length of Stay (Days)"},
              color="department")
st.plotly_chart(fig2)

# Infection Rate & Wait Time by Department
if not df_kpis.empty:
    kpi_bar = df_kpis.groupby("department").agg({
        "infection_rate_percent": "mean",
        "avg_wait_time_minutes": "mean"
    }).reset_index()

    fig3 = px.bar(kpi_bar, x="department", y="infection_rate_percent",
                  title="Avg Infection Rate by Department",
                  labels={"infection_rate_percent": "Infection Rate (%)"},
                  color="department")
    st.plotly_chart(fig3)

    fig4 = px.bar(kpi_bar, x="department", y="avg_wait_time_minutes",
                  title="Avg Wait Time by Department",
                  labels={"avg_wait_time_minutes": "Wait Time (min)"},
                  color="department")
    st.plotly_chart(fig4)

# Data Tables
st.markdown("### Patient Admissions Sample")
st.dataframe(df[["patient_id", "department", "admit_date", "length_of_stay", "readmitted"]].head(10))

st.markdown("### Department KPI Snapshot")
st.dataframe(df_kpis if not df_kpis.empty else pd.DataFrame({"message": ["No KPI data for selection."]}))
