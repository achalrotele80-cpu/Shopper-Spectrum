import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px

def show():

    st.title("🛍️ Product Recommendation System")
    st.markdown("Recommend similar products using Item-Based Collaborative Filtering")

    # Load data
    df = pd.read_csv("data/cleaned_online_retail.csv")
    df["CustomerID"] = df["CustomerID"].astype(int)

    # Remove Missing Product Names
    df = df.dropna(subset=["Description"])

    # Product-Customer Matrix
    product_customer = df.pivot_table(
         index="Description",
         columns="CustomerID",
         values="Quantity",
         aggfunc="sum",
         fill_value=0
    )

    # Cosine Similarity
    similarity = cosine_similarity(product_customer)

    similarity_df = pd.DataFrame(
         similarity,
         index=product_customer.index,
         columns=product_customer.index
    )

    # Product Selection
    product_name = st.selectbox(
         "Select Product",
         sorted(product_customer.index.tolist())
    )

    top_n = st.slider(
         "Number of Recommendations",
         min_value=1,
         max_value=10,
         value=5
    )

    if st.button("Get Recommendations"):

     # Get Similar Products
     similar_products = similarity_df[product_name].sort_values(
        ascending=False
     )[1:top_n+1]

     recommendations = pd.DataFrame({
        "Recommended Product": similar_products.index,
        "Similarity Score": similar_products.values.round(3)
     })

     st.success(f"Top {top_n} Products Similar to '{product_name}'")

     st.dataframe(
         recommendations,
         use_container_width=True
     )

     # Bar Chart
     st.subheader("📊 Similarity Scores")

     chart = recommendations.sort_values(
            "Similarity Score",
            ascending=True
        )

     st.bar_chart(
            chart.set_index("Recommended Product")
        )
     
     st.subheader("🔥 Product Similarity Heatmap")

     heatmap_df = pd.DataFrame(
       similarity_df.loc[
          [product_name] + recommendations["Recommended Product"].tolist(),
          [product_name] + recommendations["Recommended Product"].tolist()
        ]
     )

     fig = px.imshow(
         heatmap_df,
         text_auto=".2f",
         color_continuous_scale="Blues",
         title="Product Similarity Matrix"
     )

     st.plotly_chart(
         fig,
         use_container_width=True
     )

