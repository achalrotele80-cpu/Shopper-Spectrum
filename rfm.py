import pandas as pd
# Load cleaned dataset from preprocessing stage
# This dataset is already cleaned (no missing, duplicates, cancelled orders)
df = pd.read_csv("data/cleaned_online_retail.csv")
print(df.head())

# ---------------- CONVERT DATE COLUMN ---------------- #
# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])# Required for time-based customer behavior analysis

# Calculate the reference date for recency calculation
reference_date = df["InvoiceDate"].max()
print(reference_date)

# ---------------- RFM CALCULATION ---------------- #
# RFM stands for:
# Recency -> How recently customer purchased
# Frequency -> How often customer purchased
# Monetary -> How much customer spent

# Calculate RFM metrics
rfm = df.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (reference_date - x.max()).days,
    "InvoiceNo": "nunique",
    "TotalPrice": "sum"
})

# Rename columns
rfm.columns = ["Recency", "Frequency", "Monetary"]

# Reset index to make CustomerID a column
rfm = rfm.reset_index()

print(rfm.head())
print(rfm.describe())# Summary statistics of RFM values and distribution insights

# ---------------- RFM SCORING ---------------- #
# RFM scoring converts raw values into ranks (1 to 5)
# Create RFM scores
import numpy as np

# Recency score: lower recency = better (recent customers are valuable)
rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    5,
    labels=[5,4,3,2,1]
)

# Frequency score: higher frequency = better (active customers are valuable)
# rank() avoids duplicate bin issues
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1,2,3,4,5]
)
# Monetary score: higher spending = better customer
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    5,
    labels=[1,2,3,4,5]
)
# Combine all scores into a single RFM segment code
rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)
# Display final RFM table
print(
    rfm[
        [
            "CustomerID",
            "Recency",
            "Frequency",
            "Monetary",
            "R_Score",
            "F_Score",
            "M_Score",
            "RFM_Score"
        ]
    ].head()
)

# ---------------- SAVE RFM DATA ---------------- #
# Save the RFM dataset to a CSV file
rfm.to_csv("data/rfm_data.csv", index=False)
print("✅ RFM dataset saved successfully!")

# ---------------- FEATURE SCALING ---------------- #
# Scale the RFM features
from sklearn.preprocessing import StandardScaler
rfm_features = rfm[["Recency", "Frequency", "Monetary"]]
scaler = StandardScaler() # Scaling RFM values is important for clustering algorithms (like KMeans)

# Standardize features to mean=0, std=1
rfm_scaled = scaler.fit_transform(rfm_features)
print(rfm_scaled[:5])

