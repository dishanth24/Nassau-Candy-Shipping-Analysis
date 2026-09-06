import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/Nassau Candy Distributor.csv")

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors="coerce")

# Calculate shipping lead time
df["Shipping Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

# Average shipping lead time by Ship Mode
ship_mode = df.groupby("Ship Mode")["Shipping Lead Time"].mean().sort_values()

# Create chart
plt.figure(figsize=(9, 5))
ship_mode.plot(kind="bar")

plt.title("Average Shipping Lead Time by Ship Mode")
plt.xlabel("Ship Mode")
plt.ylabel("Average Lead Time (Days)")
plt.xticks(rotation=0)
plt.tight_layout()

# Save chart
plt.savefig("analysis/ship_mode_lead_time.png", dpi=300)

plt.show()

# Top 10 slowest routes
route_analysis = (
    df.groupby(["State/Province", "Region"])
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .sort_values("Avg_Lead_Time", ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
route_analysis["Avg_Lead_Time"].sort_values().plot(kind="barh")

plt.title("Top 10 Slowest Shipping Routes")
plt.xlabel("Average Shipping Lead Time (Days)")
plt.ylabel("State / Province")
plt.tight_layout()

plt.savefig("analysis/top_10_slowest_routes.png", dpi=300)

plt.show()