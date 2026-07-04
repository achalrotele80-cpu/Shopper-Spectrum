import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.metrics import silhouette_score

def show():
    df = pd.read_csv("data/customer_segments.csv")

    # Calculate Silhouette Score
    score = silhouette_score(
        df[["Recency", "Frequency", "Monetary"]],
        df["Cluster"]
    )

    # Display the customer segments distribution
    st.title("🎯 Customer Segmentation (K-Means)")

    # Display the Silhouette Score
    st.metric("Silhouette Score", f"{score:.3f}")

    # Display the first few rows of the DataFrame
    st.subheader("👥 Customer Segments Distribution")

    # Count the number of customers in each cluster
    cluster_counts = df["Cluster"].value_counts().reset_index()
    cluster_counts.columns = ["Cluster", "Count"]

    # Create a bar chart
    fig = px.bar(
        cluster_counts,
        x="Cluster",
        y="Count",
        title="Number of Customers per Cluster",
        color="Cluster"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🌐 3D Customer Segmentation")

    fig3d = px.scatter_3d(
        df,
        x="Recency",
        y="Frequency",
        z="Monetary",
        color="Segment",
        hover_data=["CustomerID", "RFM_Score"],
        title="3D Visualization of Customer Segments"
    )

    # Update layout for better visualization
    fig3d.update_layout(
        title_x=0.5,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.plotly_chart(fig3d, use_container_width=True)

    st.subheader("📋 Cluster Summary")

    cluster_summary = (
        df.groupby("Segment")[["Recency", "Frequency", "Monetary"]]
        .mean()
        .round(2)
    )

    st.dataframe(cluster_summary, use_container_width=True)

