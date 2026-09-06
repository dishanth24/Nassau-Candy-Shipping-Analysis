import pandas as pd

# Load dataset
df = pd.read_csv("data/Nassau Candy Distributor.csv")

# Convert date columns
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors="coerce")

# Calculate shipping lead time
df["Shipping Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

print("=" * 60)
print("NASSAU CANDY DISTRIBUTOR - EDA")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

print("\nShipping Lead Time Statistics:")
print(df["Shipping Lead Time"].describe())

print("\nShip Mode:")
print(df["Ship Mode"].value_counts())

print("\nRegion:")
print(df["Region"].value_counts())

print("\nFirst 5 Records:")
print(df.head())

print("\nRoute-Level Analysis:")

route_analysis = (
    df.groupby(["State/Province", "Region"])
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .sort_values("Avg_Lead_Time", ascending=False)
)

print(route_analysis.head(10))

print("\nTOP 10 SLOWEST ROUTES:")
print(route_analysis.head(10))

print("\nTOP 10 FASTEST ROUTES:")
print(route_analysis.sort_values("Avg_Lead_Time").head(10))

print("\nSHIP MODE PERFORMANCE:")

ship_mode_analysis = (
    df.groupby("Ship Mode")
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .sort_values("Avg_Lead_Time")
)

print(ship_mode_analysis)

print("\nFACTORY / CUSTOMER COLUMNS CHECK:")

for column in df.columns:
    if any(word in column.lower() for word in ["factory", "customer", "product"]):
        print(column)