#=============================================================================================
# EDA AND VISUALIZATION
#=============================================================================================
import pandas as pd
import matplotlib.pyplot as plt
#load cleaned dataset
df = pd.read_csv("data/cleaned_online_retail.csv")

print("=" * 50)
print("EXECUTIVE KPI")
print("=" * 50)

# ---------------- KPI CALCULATION ---------------- #
# Calculate total revenue
total_revenue = df["TotalPrice"].sum()
print("Total Revenue :", round(total_revenue, 2))

# Calculate total orders
total_orders = df["InvoiceNo"].nunique()# Helps understand order volume
print("Total Orders :", total_orders)

# Calculate total customers
total_customers = df["CustomerID"].nunique()# Indicates customer base size
print("Total Customers :", total_customers)

# Calculate total products
total_products = df["StockCode"].nunique()# Helps understand product diversity
print("Total Products :", total_products)

# Calculate average order value
average_order_value = total_revenue / total_orders # Key business metric to understand spending per order
print("Average Order Value :", round(average_order_value, 2))

#=============================================================================================
# Monthly Revenue Visualization 
#=============================================================================================
# Group data by month to analyze seasonal sales trends
monthly_sales = (
    df.groupby("Month")["TotalPrice"]
      .sum()
      .reset_index()
)
print(monthly_sales)

# Find the month with the highest revenue
best_month = monthly_sales.loc[
    monthly_sales["TotalPrice"].idxmax()
]
print("\nBest Sales Month:")
print(best_month)

# Plotting
plt.figure(figsize=(10,5))
plt.plot(
    monthly_sales["Month"],
    monthly_sales["TotalPrice"],
    marker="o"
)
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.grid(True)
plt.show()

#=============================================================================================
#Countries by Revenue Visualization
#=============================================================================================
# Identify top 10 countries contributing to revenue
country_sales = (
    df.groupby("Country")["TotalPrice"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)
print(country_sales)

# Plotting
plt.figure(figsize=(12,6))
country_sales.plot(kind="bar")
plt.title("Top 10 Countries by Revenue")
plt.xlabel("Country")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.show()

#=============================================================================================
#Top Selling Products Visualization
#=============================================================================================
# Identify most sold products based on quantity
Top_products = (
    df.groupby("Description")["Quantity"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)
print(Top_products)

# Plotting
plt.figure(figsize=(12,6))
Top_products.sort_values().plot(kind="barh")
plt.title("Top 10 Selling Products")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")
plt.show()

#=============================================================================================
#Top Customers Visualization
#=============================================================================================
# Identify top 10 customers based on spending
Top_customers = (
    df.groupby("CustomerID")["TotalPrice"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)
print(Top_customers)

# Plotting
plt.figure(figsize=(12,6))
Top_customers.sort_values().plot(kind="barh")
plt.title("Top 10 Customers by Spending")
plt.xlabel("Revenue")
plt.ylabel("Customer ID")
plt.show()

#=============================================================================================
# Hourly Sales Visualization
#=============================================================================================  
# Analyze sales trends by hour of the day to identify peak shopping times
hourly_sales = (
    df.groupby("Hour")["TotalPrice"]
      .sum()
      .reset_index()
)
print(hourly_sales)

# Find the hour with the highest revenue
best_hour = hourly_sales.loc[
    hourly_sales["TotalPrice"].idxmax()
]
print("\nBest Sales Hour:")
print(best_hour)

# Plotting
plt.figure(figsize=(10,5))
plt.plot(
    hourly_sales["Hour"],
    hourly_sales["TotalPrice"],
    marker="o"
)
plt.title("Hourly Sales Trend")
plt.xlabel("Hour")
plt.ylabel("Revenue")
plt.grid(True)
plt.show()

#=============================================================================================
# Day of the week sales visualization
#=============================================================================================  
# Analyze revenue by day of week
day_sales = (
    df.groupby("DayName")["TotalPrice"]
      .sum()
)
# Maintain correct weekday order for proper visualization
day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]
day_sales = day_sales.reindex(day_order)

# Plotting
plt.figure(figsize=(10,5))

day_sales.plot(kind="bar")
plt.title("Revenue by Day")
plt.xlabel("Day")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.show()

