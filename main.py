import pandas as pd

# Read Dataset
df = pd.read_csv("data/online_retail.csv") # We use pandas because it provides powerful data manipulation tools

print("="*50)
print("SHOPPER SPECTRUM DATASET")
print("="*50)

# Shape of Dataset
print("\n1. Dataset Shape")# Helps understand size of data before processing
print(df.shape)

# Column Names
print("\n2. Column Names")# Useful to understand available features in dataset
print(df.columns)

# Data Types
print("\n3. Data Types")# Helps identify numeric, categorical, and datetime fields
print(df.dtypes)

# Dataset Information
print("\n4. Dataset Information")# Summary of dataset (non-null counts, memory usage, etc.)
print(df.info())#used for quick overview of dataset structure

print("=" * 50)
print("Missing Values")
print("=" * 50)
print(df.isnull().sum())# Check missing values in each column

print("=" * 50)
print("Duplicate Rows")
print("=" * 50)
print(df.duplicated().sum())# Count duplicate rows in dataset

print("=" * 50)
print("Summary Statistics")
print("=" * 50)
print(df.describe()) # Show mean, min, max, quartiles for numeric columns

# ---------------- DATA CLEANING ---------------- #
# Display dataset shape before cleaning
print("Dataset Shape Before Cleaning:")
print(df.shape)

# Count missing Customer IDs
missing_customer = df["CustomerID"].isnull().sum()
print("\nMissing Customer IDs:", missing_customer)

# Remove rows with missing Customer IDs
df = df.dropna(subset=["CustomerID"])

# Verify cleaning
print("\nDataset Shape After Cleaning:")
print(df.shape)

print("\nMissing Customer IDs After Cleaning:")
print(df["CustomerID"].isnull().sum())

duplicate_count = df.duplicated().sum()# Check and remove duplicate records
print("Duplicate Records:", duplicate_count)

df = df.drop_duplicates()

print("Duplicate Records After Cleaning:")
print(df.duplicated().sum())

print("Dataset Shape After Removing Duplicates:")
print(df.shape)

# ---------------- CANCELLED ORDERS ---------------- #
# Display cancelled orders
cancelled_orders = df[df["InvoiceNo"].astype(str).str.startswith("C")]# Identify cancelled orders (InvoiceNo starting with 'C')
                                                                      # These represent returned/cancelled transactions
print("Number of Cancelled Orders:")
print(cancelled_orders.shape)

print("\nFirst 10 Cancelled Orders:")
print(cancelled_orders.head(10))

# Remove cancelled invoices
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

cancelled_after = df["InvoiceNo"].astype(str).str.startswith("C").sum()

print("Cancelled Orders After Cleaning:", cancelled_after)

print("Dataset Shape:", df.shape)

# ---------------- INVALID DATA CHECK ---------------- #
negative_quantity = (df["Quantity"] <= 0).sum()# Check invalid quantity values (<= 0)
print("Transactions with Quantity <= 0 :", negative_quantity)# These are not valid purchases

invalid_price = (df["UnitPrice"] <= 0).sum()# Check invalid unit price values (<= 0)
print("Transactions with UnitPrice <= 0 :", invalid_price)

# Check Quantity
print((df["Quantity"] <= 0).sum())

# Check Unit Price
print((df["UnitPrice"] <= 0).sum())

# Display invalid prices
print(df[df["UnitPrice"] <= 0].head())

# ---------------- FEATURE ENGINEERING ---------------- #
# Create TotalPrice column
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]# Represents revenue per transaction

print("TotalPrice column created successfully!")

# Display first 5 rows
print(df[["Quantity", "UnitPrice", "TotalPrice"]].head())

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    format="mixed",
    dayfirst=True
)
print(df["InvoiceDate"].dtype)
print(df["InvoiceDate"].head(10))

# ---------------- TIME FEATURES ---------------- #
df["Year"] = df["InvoiceDate"].dt.year # Extract time-based features for analysis
df["Month"] = df["InvoiceDate"].dt.month
df["Day"] = df["InvoiceDate"].dt.day
df["Hour"] = df["InvoiceDate"].dt.hour
df["DayName"] = df["InvoiceDate"].dt.day_name()

print(df[["InvoiceDate","Year","Month","Day","Hour","DayName"]].head())

# ---------------- SAVE CLEANED DATA ---------------- #
# Save cleaned dataset
df.to_csv("data/cleaned_online_retail.csv", index=False)
print("✅ Cleaned dataset saved successfully!")
index=False



