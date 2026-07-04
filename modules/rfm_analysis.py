import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    df = pd.read_csv("data/cleaned_online_retail.csv")

    st.title("👥 RFM Analysis")

    # Convert InvoiceDate to datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Create snapshot date (for Recency calculation)
    snapshot_date = df["InvoiceDate"].max()

    # Create RFM table
    rfm = df.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
        "InvoiceNo": "nunique",
        "TotalPrice": "sum"
    })

    # Rename columns
    rfm.columns = ["Recency", "Frequency", "Monetary"]

    # Reset index
    rfm = rfm.reset_index()

    st.write("RFM Table")
    st.dataframe(rfm.head())

    st.subheader("📉 Recency Distribution")

    fig_r = px.histogram(
        rfm,
        x="Recency",
        nbins=30,
        title="Recency Distribution"
    )

    st.plotly_chart(fig_r, use_container_width=True)

    st.subheader("📊 Frequency Distribution")

    fig_f = px.histogram(
        rfm,
        x="Frequency",
        nbins=30,
        title="Frequency Distribution"
    )

    st.plotly_chart(fig_f, use_container_width=True)

    st.subheader("💰 Monetary Distribution")

    fig_m = px.histogram(
        rfm,
        x="Monetary",
        nbins=30,
        title="Monetary Distribution"
    )

    st.plotly_chart(fig_m, use_container_width=True)


    ## Correlation Heatmap
    corr = rfm[["Recency", "Frequency", "Monetary"]].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Correlation Heatmap of RFM Features"
    )

    st.plotly_chart(fig, use_container_width=True)