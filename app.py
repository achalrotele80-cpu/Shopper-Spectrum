import streamlit as st
import pandas as pd
import plotly.express as px

from modules import dashboard
from modules import sales
from modules import country
from modules import rfm_analysis
from modules import clustering_analysis
from modules import recommendation
from modules import prediction
from modules import business_insights

@st.cache_data
def load_cleaned_data():
    df = pd.read_csv("data/cleaned_online_retail.csv")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df


@st.cache_data
def load_rfm_data():
    return pd.read_csv("data/rfm_data.csv")


@st.cache_data
def load_customer_segments():
    return pd.read_csv("data/customer_segments.csv")

st.set_page_config(
    page_title="Shopper Spectrum",
    page_icon="🛒",
    layout="wide"
)

# Sidebar
st.sidebar.title("🛒 Shopper Spectrum")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Sales Analytics",
        "Country Analysis",
        "RFM Analysis",
        "Customer Segmentation",
        "Product Recommendation",
        "Customer Prediction",
        "Business Insights"
    ]
)

# Display the selected page
if page == "Executive Dashboard":
    dashboard.show()
    st.stop()

elif page == "Sales Analytics":
    sales.show()
    st.stop()

elif page == "Country Analysis":
    country.show()
    st.stop()   

elif page == "RFM Analysis":
    rfm_analysis.show()
    st.stop()

elif page == "Customer Segmentation":
    clustering_analysis.show()
    st.stop()

elif page == "Product Recommendation":
    recommendation.show()
    st.stop()

elif page == "Customer Prediction":
    prediction.show()
    st.stop()

elif page == "Business Insights":
    business_insights.show(load_cleaned_data(), load_customer_segments())
    st.stop()
