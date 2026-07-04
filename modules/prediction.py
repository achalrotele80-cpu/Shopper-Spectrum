import streamlit as st
import pandas as pd
import numpy as np
import joblib


def show():

    st.title("🤖 Customer Prediction")
    st.markdown("Predict the customer segment using RFM values.")

    # Load trained model and scaler
    kmeans = joblib.load("models/kmeans_model.pkl")
    scaler = joblib.load("models/scaler.pkl")

    # User Input
    recency = st.number_input(
        "Recency (Days)",
        min_value=0,
        value=20
    )

    frequency = st.number_input(
        "Frequency",
        min_value=1,
        value=15
    )

    monetary = st.number_input(
        "Monetary Value",
        min_value=0.0,
        value=8000.0
    )
    # Predict Customer Segment
    if st.button("Predict Customer Segment"):

        new_customer = pd.DataFrame(
             [[recency, frequency, monetary]],
             columns=["Recency", "Frequency", "Monetary"]
       )
        
        # Apply the same transformation used during training
        new_customer = np.log1p(new_customer)

        # Scale the new customer data
        scaled_customer = scaler.transform(new_customer)

        # Predict the cluster for the new customer
        cluster = kmeans.predict(scaled_customer)[0]

        segment_names = {
            0: "High-Value",
            1: "Regular",
            2: "Occasional",
            3: "At-Risk"
        }

        st.success(
            f"Predicted Segment: **{segment_names.get(cluster, 'Unknown')}**"
        )

        # Business Recommendation
        recommendations = {
            0: "Reward loyalty with exclusive discounts and VIP offers.",
            1: "Encourage repeat purchases through personalized product recommendations, reward points, and special discounts.",
            2: "Increase engagement with seasonal offers, bundle deals, and promotional campaigns.",
            3: "Launch win-back campaigns with personalized discounts, reminder emails, and special offers to re-engage the customer"
        }

        st.info(
            recommendations.get(cluster, "")
        )