import streamlit as st
import pandas as pd
import plotly.express as px

def show():

    # Load cleaned dataset
    df = pd.read_csv("data/cleaned_online_retail.csv")

    st.title("🌍 Country Analysis")
    # Calculate Revenue by Country
    country_revenue = (
        df.groupby("Country")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    # Create Revenue Chart
    fig_revenue = px.bar(
        country_revenue,
        x="Country",
        y="TotalPrice",
        title="Top 10 Countries by Revenue",
        color="TotalPrice",
        color_continuous_scale="Viridis"
    )

    fig_revenue.update_layout(
        title_x=0.5,
        xaxis_title="Country",
        yaxis_title="Revenue"
    )


    # Calculate Orders by Country
    country_orders = (
        df.groupby("Country")["InvoiceNo"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    country_orders.columns = ["Country", "Orders"]
    # Create Orders Chart
    fig_orders = px.bar(
        country_orders,
        x="Country",
        y="Orders",
        title="Top 10 Countries by Orders",
        color="Orders",
        color_continuous_scale="Plasma"
    )

    fig_orders.update_layout(
        title_x=0.5,
        xaxis_title="Country",
        yaxis_title="Number of Orders"
    )

    # Layout: Side by Side Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌍 Revenue by Country")
        st.plotly_chart(fig_revenue, use_container_width=True)

    with col2:
        st.subheader("📦 Orders by Country")
        st.plotly_chart(fig_orders, use_container_width=True)


