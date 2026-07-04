import streamlit as st
import pandas as pd
import plotly.express as px

def show():

    # Load cleaned data
    df = pd.read_csv("data/cleaned_online_retail.csv")

    # Convert InvoiceDate to datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Create Month column
    df["Month"] = df["InvoiceDate"].dt.to_period("M")

    # Sales Overview
    st.title("📊 Sales Analytics")

    monthly_sales = (
        df.groupby("Month")["TotalPrice"]
        .sum()
        .reset_index()
    )

    monthly_sales["Month"] = monthly_sales["Month"].astype(str)

    fig = px.line(
        monthly_sales,
        x="Month",
        y="TotalPrice",
        title="Monthly Revenue Trend",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
