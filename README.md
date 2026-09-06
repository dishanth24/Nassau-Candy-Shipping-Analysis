# 🍬 Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

## 📊 Project Overview

This project presents an interactive data analytics dashboard designed to analyze shipping and distribution performance for Nassau Candy Distributor.

The system transforms raw order and shipment records into meaningful logistics insights using data preprocessing, exploratory data analysis, interactive visualization, geographic analysis, shipping risk classification, bottleneck detection, and business recommendations.

The final application is developed using Python and Streamlit and provides an interactive environment for exploring shipping performance across customers, products, regions, states, shipping modes, and time periods.

---

## 🎯 Project Objectives

The main objectives of this project are to:

- Analyze shipping performance.
- Calculate and examine Shipping Lead Time.
- Compare different shipping modes.
- Analyze route-level performance.
- Study customer distribution and customer value.
- Evaluate product-level performance.
- Compare regional and state-level performance.
- Analyze sales and profitability.
- Identify shipping delays and operational risk.
- Perform geographic distribution analysis.
- Detect potential logistics bottlenecks.
- Analyze shipping trends over time.
- Provide actionable logistics recommendations.
- Develop an interactive Streamlit dashboard.

---

## 🗂️ Dataset

The project uses the Nassau Candy Distributor shipping dataset.

### Dataset Size

- Records: 10,194
- Original fields: 18

### Main Dataset Categories

The dataset contains information related to:

- Orders
- Customers
- Products
- Shipping modes
- Order dates
- Shipment dates
- Cities
- States/Provinces
- Regions
- Sales
- Units
- Gross Profit
- Cost

A derived `Shipping Lead Time` field is used for shipping-performance analysis.

---

## ⚠️ Data Quality Note

The source shipment-date information contains unusually large date differences.

As a result, the calculated Shipping Lead Time can contain very large values.

These values should be treated as a data-quality observation and validated against original operational records before being interpreted as actual delivery durations.

The current dashboard preserves the project's existing calculation and does not claim that these large values represent normal real-world delivery times.

---

## 📈 Dashboard Features

The dashboard contains the following analytical modules:

### 1. KPI Summary

Provides an overview of:

- Total Orders
- Total Sales
- Total Profit
- Average Shipping Lead Time

### 2. Shipping Insights

Analyzes shipping performance across different shipping modes.

### 3. Route-Level Analysis

Provides interactive analysis of shipping performance across regions and destinations.

### 4. Customer Analysis

Examines customer distribution and customer-level performance.

### 5. Customer Value Matrix

Compares customers using:

- Orders
- Sales
- Profit
- Average Shipping Lead Time

### 6. Product Analysis

Analyzes product distribution and performance.

### 7. Product Performance

Uses an interactive treemap to visualize product contribution.

### 8. Regional Analysis

Compares regional performance using operational and financial indicators.

### 9. State / Province Analysis

Provides detailed geographical performance analysis.

### 10. Ship Mode Analysis

Compares shipping modes using multiple performance metrics.

### 11. Profitability Analysis

Analyzes:

- Sales
- Profit
- Profit Margin
- Product profitability

### 12. Customer–Product Analysis

Allows users to explore customer distribution for selected products.

### 13. Time-Based Analysis

Analyzes monthly:

- Orders
- Sales
- Profit
- Average Shipping Lead Time

### 14. Order Distribution

Provides order-level analysis using statistical visualizations.

### 15. Shipping Delay & Risk Analysis

Classifies shipping records into:

- Fast
- Normal
- Delayed
- Critical

### 16. Geographic Analysis

Provides an interactive state-level geographic visualization.

### 17. Bottleneck Detection

Identifies potentially high-risk areas using operational indicators.

### 18. Route Efficiency Trend

Provides monthly route-performance trend analysis.

### 19. Executive Summary

Provides a consolidated business interpretation of the analysis.

---

## 🎛️ Interactive Controls

The dashboard provides interactive controls for:

- Region
- Ship Mode
- Order Date

The selected filters dynamically update the dashboard.

---

## 📥 Dashboard Actions

The application provides:

- Reset Filters
- Download Filtered Data
- Quick Navigation
- Back to Top

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data processing and analysis |
| Matplotlib | Visualization |
| Plotly | Interactive visualization |
| Streamlit | Dashboard development |
| HTML/CSS | Dashboard styling and navigation |
| CSV | Dataset format |

---

## 📁 Project Structure

```text
Nassau-Candy-Shipping-Analysis/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── Nassau Candy Distributor.csv
│
└── .streamlit/
    └── config.toml