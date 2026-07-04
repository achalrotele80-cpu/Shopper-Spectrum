import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    
    # Load Dataset
    df = pd.read_csv("data/cleaned_online_retail.csv")
    
    # ==========================
    # Executive Dashboard
    # ==========================

    st.title("📊 Executive Dashboard")
    st.markdown("### Customer Analytics & Recommendation System")

    # Convert InvoiceDate to datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    #calculate total revenue
    total_revenue = df["TotalPrice"].sum()

    # Calculate total orders
    total_orders = df["InvoiceNo"].nunique()

    # Calculate total customers
    total_customers = df["CustomerID"].nunique()

    # Calculate total products
    total_products = df["StockCode"].nunique()

    # Calculate total countries
    total_countries = df["Country"].nunique()

    # Calculate average order value
    average_order_value = total_revenue / total_orders

    # Display KPIs in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")

    with col2:
        st.metric("🧾 Total Orders", total_orders)

    with col3:
        st.metric("👥 Customers", total_customers)

    # Display additional KPIs in columns
    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("📦 Products", total_products)

    with col5:
        st.metric("🌍 Countries", total_countries)

    with col6:
        st.metric("💵 Avg Order Value", f"${average_order_value:,.2f}")

    # Monthly Sales Trend
    monthly_sales = (
        df.groupby("Month")["TotalPrice"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly_sales,
        x="Month",
        y="TotalPrice",
        title="Monthly Sales Trend",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    #==========================
    st.subheader("🏆 Top 10 Products")
    top_products = (
        df.groupby("Description")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_products = px.bar(
        top_products,
        x="TotalPrice",
        y="Description",
        orientation="h",
        title="Top 10 Products by Revenue"
    )

    st.plotly_chart(fig_products, use_container_width=True)

    st.subheader("🌍 Sales by Country")
    country_sales = (
        df.groupby("Country")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    # Create Country Sales Chart
    fig_country = px.bar(
            country_sales,
            x="Country",
            y="TotalPrice",
            title="Top 10 Countries by Revenue",
            color="TotalPrice",
            color_continuous_scale="Blues"
        )

    fig_country.update_layout(
            xaxis_title="Country",
            yaxis_title="Revenue",
            title_x=0.5
        )

    st.plotly_chart(fig_country, use_container_width=True)

