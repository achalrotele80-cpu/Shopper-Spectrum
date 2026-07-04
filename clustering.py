import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load the RFM dataset
rfm = pd.read_csv("data/rfm_data.csv")
print(rfm.head())

# ---------------- DATA TRANSFORMATION ---------------- #
# Apply Log Transformation is appropriate for RFM values to reduce skewness and handle outliers
# Helps normalize extreme values in customer spending and frequency
rfm["Recency"] = np.log1p(rfm["Recency"])
rfm["Frequency"] = np.log1p(rfm["Frequency"])
rfm["Monetary"] = np.log1p(rfm["Monetary"])

print("✅ Log Transformation Applied")
print(rfm[["Recency","Frequency","Monetary"]].head())

# ---------------- FEATURE SCALING ---------------- #
# Select RFM features
rfm_features = rfm[["Recency", "Frequency", "Monetary"]]

# Scale the RFM features
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_features)
print(rfm_scaled[:5])

# ---------------- FIND OPTIMAL CLUSTERS ---------------- #
# Store WCSS and Silhouette Scores
wcss = [] # WCSS: measures compactness of clusters (used in Elbow method)
silhouette_scores = []# Silhouette Score: measures quality of clustering (higher = better separation)


# Try different number of clusters (2 to 10)
for i in range(2, 11):
    # Initialize KMeans with i clusters
    kmeans = KMeans(
        n_clusters=i,
        random_state=42,
        n_init=20
    )

    labels = kmeans.fit_predict(rfm_scaled) # Fit model and assign cluster labels

    wcss.append(kmeans.inertia_) # Store WCSS (inertia)

    score = silhouette_score(rfm_scaled, labels)   # Evaluate clustering performance
    silhouette_scores.append(score)

    print(f"K = {i}  |  Silhouette Score = {score:.4f}")

print(wcss)
print(silhouette_scores)

# ---------------- ELBOW METHOD PLOT ---------------- #
# Helps identify optimal number of clusters visually
# Plotting the Elbow Method graph
plt.figure(figsize=(8,5))
plt.plot(range(2,11), wcss, marker="o")
plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.grid(True)
plt.show()

# ---------------- SILHOUETTE SCORE PLOT ---------------- #
# Shows how well clusters are separated
plt.figure(figsize=(8,5))
plt.plot(
    range(2,11),
    silhouette_scores,
    marker="o"
)

plt.title("Silhouette Score vs Number of Clusters")
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Score")
plt.grid(True)

plt.show()

# ---------------- FINAL KMEANS MODEL ---------------- #
# Create KMeans model
kmeans = KMeans(
    n_clusters=4,
    random_state=42
)

# Train final model
# Fit the model to the scaled RFM data
kmeans.fit(rfm_scaled)

# Save the trained model and scaler
joblib.dump(kmeans, "models/kmeans_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

# ---------------- MODEL EVALUATION ---------------- #
# Calculate Silhouette Score
score = silhouette_score(rfm_scaled, kmeans.labels_)
print(f"Silhouette Score: {score:.3f}")

# Save the Silhouette Score
with open("data/silhouette_score.txt", "w") as f:
    f.write(str(score))

# ---------------- CUSTOMER SEGMENT ASSIGNMENT ---------------- #
# Assign cluster labels to the original RFM dataframe
rfm["Cluster"] = kmeans.labels_
print(rfm.head())

# Display the number of customers in each cluster
print(rfm["Cluster"].value_counts())

# ---------------- CLUSTER ANALYSIS ---------------- #
# Compute average RFM values per cluster
# Helps understand behavior of each segment
# Display the average RFM values for each cluster
cluster_summary = (
    rfm.groupby("Cluster")[["Recency", "Frequency", "Monetary"]]
       .mean()
)
print(cluster_summary)

# Save cluster summary for dashboard/report
cluster_summary.to_csv("data/cluster_summary.csv")

# ---------------- BUSINESS SEGMENTS ---------------- #
# Map cluster labels to segment names
segment_names = {
0:"High-Value",
1:"Regular",
2:"Occasional",
3:"At-Risk"
}

rfm["Segment"] = rfm["Cluster"].map(segment_names)
print(rfm[["CustomerID", "Cluster", "Segment"]].head(10))
print(rfm["Segment"].value_counts())

# Save the customer segments to a CSV file
rfm.to_csv("data/customer_segments.csv", index=False)
print("✅ Customer Segments saved successfully!")

