import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Nassau Candy Distributor",
    page_icon="🍬",
    layout="wide"
)
# ============================================================
# CUSTOM DASHBOARD STYLING
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
}

h1 {
    font-size: 42px !important;
    font-weight: 800 !important;
    margin-bottom: 5px !important;
}

h2 {
    background: linear-gradient(
        90deg,
        rgba(70, 90, 140, 0.30),
        rgba(70, 90, 140, 0.05)
    );
    padding: 12px 18px;
    border-radius: 10px;
    border-left: 5px solid #6ea8fe;
    margin-top: 25px;
    margin-bottom: 18px;
}

h3 {
    background: rgba(70, 90, 140, 0.16);
    padding: 9px 14px;
    border-radius: 8px;
    border-left: 4px solid #8ab4f8;
}
[data-testid="stMetric"] {
    background-color: #161a23;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #292e3a;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
}

section[data-testid="stSidebar"] {
    background-color: #151821;
    border-right: 1px solid #292e3a;
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div id="top"></div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        background: linear-gradient(
            90deg,
            rgba(180, 30, 90, 0.30),
            rgba(120, 40, 100, 0.08)
        );
        padding: 14px 20px;
        border-radius: 10px;
        border-left: 5px solid #ff5c9a;
        margin-bottom: 15px;
    ">
        <h1 style="
            margin: 0;
            font-size: 42px;
            font-weight: 800;
        ">
            🍬 Nassau Candy Distributor
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "### 🚚 Shipping Route Efficiency Dashboard"
)

st.caption(
    "Data-driven insights for improving delivery performance, "
    "route efficiency, and distribution operations."
)

# =========================================================
# LOAD DATASET
# =========================================================

df = pd.read_csv("data/Nassau Candy Distributor.csv")

# =========================================================
# DATE CONVERSION
# =========================================================

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True,
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    dayfirst=True,
    errors="coerce"
)

# =========================================================
# SHIPPING LEAD TIME
# =========================================================

df["Shipping Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("## 🎛️ Dashboard Controls")
st.sidebar.caption("Use the controls below to explore shipping performance.")

# ---------------- REGION FILTER ----------------

st.sidebar.markdown("🌎 **Select Region**")

regions = sorted(df["Region"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions,
    label_visibility="collapsed"
)

# ---------------- SHIP MODE FILTER ----------------

st.sidebar.markdown("🚚 **Select Ship Mode**")

ship_modes = sorted(df["Ship Mode"].dropna().unique())

selected_ship_modes = st.sidebar.multiselect(
    "Ship Mode",
    options=ship_modes,
    default=ship_modes,
    label_visibility="collapsed"
)

# ------------------------------------------------------------
# Safe Order Date Filter
# ------------------------------------------------------------

valid_dates = df["Order Date"].dropna()

if len(valid_dates) > 0:

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    selected_dates = st.sidebar.date_input(
        "Order Date",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )

else:

    st.sidebar.error("No valid order dates available.")

    selected_dates = None
# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["Region"].isin(selected_regions)) &
    (df["Ship Mode"].isin(selected_ship_modes))
].copy()

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date) &
        (filtered_df["Order Date"].dt.date <= end_date)
    ].copy()

# Use filtered data for the complete dashboard
df = filtered_df

# ------------------------------------------------------------
# DASHBOARD ACTIONS
# ------------------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Dashboard Actions")

if st.sidebar.button(
    "🔄 Reset Filters",
    use_container_width=True
):
    st.rerun()

st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_nassau_shipping_data.csv",
    mime="text/csv",
    use_container_width=True
)

# =========================================================
# CHECK FILTER RESULT
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No data available for the selected filters. "
        "Please select at least one Region and Ship Mode."
    )

    st.stop()

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_orders = len(filtered_df)

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Gross Profit"].sum()

avg_lead_time = filtered_df["Shipping Lead Time"].mean()

# =========================================================
# KPI DASHBOARD
# =========================================================
st.caption(
    "📊 Current performance overview based on the selected filters"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📦 Total Orders",
    f"{total_orders:,}"
)

col2.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)

col3.metric(
    "📈 Total Profit",
    f"${total_profit:,.2f}"
)

col4.metric(
    "🚚 Avg Shipping Lead Time",
    f"{avg_lead_time:,.0f} days"
)
st.caption(
    f"📌 Showing {len(filtered_df):,} records from the selected filters"
)

st.divider()

# ============================================================
# QUICK ANALYSIS NAVIGATION
# ============================================================

st.markdown("### 🔎 Quick Navigation")

st.caption(
    "Click an analysis section to jump directly to it."
)

st.markdown(
    """
    <div style="
        display:flex;
        flex-wrap:wrap;
        gap:8px;
        margin-top:10px;
        margin-bottom:15px;
    ">

    <a href="#shipping-insights"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       📦 Shipping Insights
    </a>

    <a href="#route-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       🛣️ Route Analysis
    </a>

    <a href="#customer-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       👥 Customer Analysis
    </a>

    <a href="#product-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       🍫 Product Analysis
    </a>

    <a href="#regional-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       🌎 Regional Analysis
    </a>

    <a href="#state-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       📍 State Analysis
    </a>

    <a href="#ship-mode-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       🚚 Ship Mode
    </a>

    <a href="#profitability-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       💰 Profitability
    </a>

    <a href="#customer-product-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       🔗 Customer–Product
    </a>

    <a href="#time-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       📅 Time Analysis
    </a>

    <a href="#order-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       📦 Order Distribution
    </a>

    <a href="#geographic-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       🗺️ Geographic Analysis
    </a>

    <a href="#bottleneck-analysis"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       🚦 Bottlenecks
    </a>

    <a href="#route-trend"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       📈 Route Trend
    </a>

    <a href="#executive-summary"
       style="color:white; text-decoration:none;
       background:#1e1e1e; padding:8px 12px;
       border-radius:8px; border:1px solid #444;">
       💡 Executive Summary
    </a>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================================
# FLOATING BACK TO TOP
# ============================================================

st.markdown(
    """
    <a href="#top"
       style="
           position:fixed;
           bottom:25px;
           right:30px;
           z-index:9999;
           background:#1e1e1e;
           color:white;
           text-decoration:none;
           padding:10px 16px;
           border-radius:10px;
           border:1px solid #555;
           font-size:13px;
           font-weight:600;
           box-shadow:0 4px 12px rgba(0,0,0,0.4);
       ">
       🔝 Back to Top
    </a>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SHIPPING PERFORMANCE BY SHIP MODE
# ============================================================

st.markdown(
    '<div id="ship-mode-analysis"></div>',
    unsafe_allow_html=True
)

st.header("🚚 Shipping Performance by Ship Mode")

ship_mode = (
    df.groupby("Ship Mode")
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
    .sort_values("Avg_Lead_Time")
)

fig_ship = px.bar(
    ship_mode,
    x="Ship Mode",
    y="Avg_Lead_Time",
    text="Avg_Lead_Time",
    hover_data={
        "Ship Mode": True,
        "Orders": True,
        "Avg_Lead_Time": ":.1f",
        "Total_Sales": ":,.2f",
        "Total_Profit": ":,.2f"
    },
    title="Average Shipping Lead Time by Ship Mode"
)

fig_ship.update_traces(
    texttemplate="%{text:.1f} days",
    textposition="outside",
    textfont=dict(
        color="white",
        size=14
    ),
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Orders: %{customdata[0]:,}<br>"
        "Avg Lead Time: %{y:.1f} days<br>"
        "Total Sales: $%{customdata[1]:,.2f}<br>"
        "Total Profit: $%{customdata[2]:,.2f}"
        "<extra></extra>"
    )
)

fig_ship.update_layout(
    title=dict(
        text="Average Shipping Lead Time by Ship Mode",
        font=dict(size=20, color="white")
    ),

    xaxis=dict(
        title=dict(
            text="Ship Mode",
            font=dict(size=14, color="white")
        ),
        tickfont=dict(size=13, color="white")
    ),

    yaxis=dict(
        title=dict(
            text="Average Lead Time (Days)",
            font=dict(size=14, color="white")
        ),
        tickfont=dict(size=13, color="white"),
        gridcolor="rgba(255,255,255,0.15)"
    ),

    height=520,

    margin=dict(
        l=70,
        r=30,
        t=80,
        b=70
    ),

    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",

    font=dict(
        family="Arial",
        size=14,
        color="white"
    ),

    hoverlabel=dict(
        bgcolor="#1f2937",
        bordercolor="#ffffff",
        font=dict(
            color="white",
            size=13
        )
    )
)

st.plotly_chart(
    fig_ship,
    use_container_width=True
)


# ============================================================
# ROUTE-LEVEL ANALYSIS
# ============================================================

st.markdown(
    '<div id="route-analysis"></div>',
    unsafe_allow_html=True
)

st.header("📍 Route-Level Analysis")
st.markdown(
    "Explore shipping performance across regions and states/provinces."
)

# ============================================================
# INTERACTIVE ROUTE EXPLORER
# ============================================================

st.subheader("🔎 Interactive Route Explorer")

route_regions = sorted(
    filtered_df["Region"].dropna().unique()
)

selected_route_region = st.selectbox(
    "🌎 Select a Region",
    options=route_regions,
    key="route_region_selector"
)

region_data = filtered_df[
    filtered_df["Region"] == selected_route_region
]

# ============================================================
# ROUTE SUMMARY
# ============================================================

route_summary = (
    region_data
    .groupby("State/Province")
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

# ============================================================
# ROUTE KPIs
# ============================================================

route_col1, route_col2, route_col3, route_col4 = st.columns(4)

route_col1.metric(
    "📦 Orders",
    f"{route_summary['Orders'].sum():,}"
)

route_col2.metric(
    "📍 States / Provinces",
    f"{route_summary['State/Province'].nunique():,}"
)

route_col3.metric(
    "💰 Sales",
    f"${route_summary['Total_Sales'].sum():,.2f}"
)

route_col4.metric(
    "⏱️ Avg Lead Time",
    f"{region_data['Shipping Lead Time'].mean():,.0f} days"
)

st.divider()

# ============================================================
# ROUTE PERFORMANCE VISUALIZATION
# ============================================================

st.subheader("📈 Route Performance Overview")

st.caption(
    "Bubble size represents sales volume. Hover over a point for detailed route information."
)

route_chart = route_summary.copy()

route_chart["Avg_Lead_Time"] = route_chart["Avg_Lead_Time"].round(1)
route_chart["Total_Sales"] = route_chart["Total_Sales"].round(2)
route_chart["Total_Profit"] = route_chart["Total_Profit"].round(2)

fig_route = px.scatter(
    route_chart,
    x="Orders",
    y="Avg_Lead_Time",
    size="Total_Sales",
    color="Total_Profit",
    hover_name="State/Province",
    hover_data={
        "Orders": True,
        "Avg_Lead_Time": ":.1f",
        "Total_Sales": ":,.2f",
        "Total_Profit": ":,.2f"
    },
    labels={
        "Orders": "Number of Orders",
        "Avg_Lead_Time": "Average Lead Time (Days)",
        "Total_Sales": "Sales",
        "Total_Profit": "Profit"
    },
    title=f"Route Efficiency — {selected_route_region}",
    template="plotly_dark",
    height=550
)

fig_route.update_layout(
    title_font_size=22,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
    legend_title="Profit",
    margin=dict(l=30, r=30, t=70, b=30)
)

fig_route.update_traces(
    marker=dict(
        opacity=0.85,
        line=dict(width=1)
    )
)

st.plotly_chart(
    fig_route,
    use_container_width=True
)

# ============================================================
# ROUTE DETAILS TABLE
# ============================================================

st.subheader("📋 Route Details")

display_routes = (
    route_summary
    .sort_values("Avg_Lead_Time", ascending=False)
    .copy()
)

display_routes["Avg_Lead_Time"] = (
    display_routes["Avg_Lead_Time"].round(1)
)

display_routes["Total_Sales"] = (
    display_routes["Total_Sales"].round(2)
)

display_routes["Total_Profit"] = (
    display_routes["Total_Profit"].round(2)
)

st.dataframe(
    display_routes,
    use_container_width=True,
    hide_index=True,
    column_config={
        "State/Province": st.column_config.TextColumn(
            "State / Province"
        ),
        "Orders": st.column_config.NumberColumn(
            "Orders",
            format="%d"
        ),
        "Avg_Lead_Time": st.column_config.NumberColumn(
            "Avg Lead Time",
            format="%.1f days"
        ),
        "Total_Sales": st.column_config.NumberColumn(
            "Total Sales",
            format="$%.2f"
        ),
        "Total_Profit": st.column_config.NumberColumn(
            "Total Profit",
            format="$%.2f"
        )
    }
)

st.divider()

# ============================================================
# OVERALL ROUTE ANALYSIS
# ============================================================

route_analysis = (
    filtered_df
    .groupby(["State/Province", "Region"])
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

# ============================================================
# TOP 10 SLOWEST ROUTES
# ============================================================

slowest_routes = (
    route_analysis
    .sort_values(
        "Avg_Lead_Time",
        ascending=False
    )
    .head(10)
    .copy()
)

slowest_routes["Avg_Lead_Time"] = (
    slowest_routes["Avg_Lead_Time"].round(1)
)

slowest_routes["Total_Sales"] = (
    slowest_routes["Total_Sales"].round(2)
)

slowest_routes["Total_Profit"] = (
    slowest_routes["Total_Profit"].round(2)
)

st.subheader("🐌 Slowest Shipping Routes")

st.caption(
    "Routes with the highest average shipping lead time."
)

st.dataframe(
    slowest_routes,
    use_container_width=True,
    hide_index=True,
    column_config={
        "State/Province": "State / Province",
        "Region": "Region",
        "Orders": st.column_config.NumberColumn(
            "Orders",
            format="%d"
        ),
        "Avg_Lead_Time": st.column_config.NumberColumn(
            "Avg Lead Time",
            format="%.1f days"
        ),
        "Total_Sales": st.column_config.NumberColumn(
            "Total Sales",
            format="$%.2f"
        ),
        "Total_Profit": st.column_config.NumberColumn(
            "Total Profit",
            format="$%.2f"
        )
    }
)

# ============================================================
# TOP 10 FASTEST ROUTES
# ============================================================

fastest_routes = (
    route_analysis
    .sort_values(
        "Avg_Lead_Time",
        ascending=True
    )
    .head(10)
    .copy()
)

fastest_routes["Avg_Lead_Time"] = (
    fastest_routes["Avg_Lead_Time"].round(1)
)

fastest_routes["Total_Sales"] = (
    fastest_routes["Total_Sales"].round(2)
)

fastest_routes["Total_Profit"] = (
    fastest_routes["Total_Profit"].round(2)
)

st.subheader("⚡ Fastest Shipping Routes")

st.caption(
    "Routes with the lowest average shipping lead time."
)

st.dataframe(
    fastest_routes,
    use_container_width=True,
    hide_index=True,
    column_config={
        "State/Province": "State / Province",
        "Region": "Region",
        "Orders": st.column_config.NumberColumn(
            "Orders",
            format="%d"
        ),
        "Avg_Lead_Time": st.column_config.NumberColumn(
            "Avg Lead Time",
            format="%.1f days"
        ),
        "Total_Sales": st.column_config.NumberColumn(
            "Total Sales",
            format="$%.2f"
        ),
        "Total_Profit": st.column_config.NumberColumn(
            "Total Profit",
            format="$%.2f"
        )
    }
)

# =========================================================
# CUSTOMER DISTRIBUTION ANALYSIS
# =========================================================
st.markdown(
    '<div id="customer-analysis"></div>',
    unsafe_allow_html=True
)


st.header("👥 Customer Distribution Analysis")

customer_analysis = (
    filtered_df
    .groupby("Customer ID")
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

# ---------------------------------------------------------
# CUSTOMER METRICS
# ---------------------------------------------------------

customer_col1, customer_col2, customer_col3 = st.columns(3)

customer_col1.metric(
    "👥 Unique Customers",
    f"{filtered_df['Customer ID'].nunique():,}"
)

customer_col2.metric(
    "📦 Orders",
    f"{len(filtered_df):,}"
)

customer_col3.metric(
    "💰 Customer Sales",
    f"${filtered_df['Sales'].sum():,.2f}"
)

# ---------------------------------------------------------
# TOP CUSTOMER SELECTOR
# ---------------------------------------------------------

customer_view = st.selectbox(
    "📊 Rank Customers By",
    options=[
        "Orders",
        "Total_Sales",
        "Total_Profit"
    ]
)

top_customers = (
    customer_analysis
    .sort_values(
        customer_view,
        ascending=False
    )
    .head(10)
)

# ---------------------------------------------------------
# CUSTOMER TABLE
# ---------------------------------------------------------

st.subheader("🏆 Top 10 Customers")

st.dataframe(
    top_customers,
    use_container_width=True
)

# ---------------------------------------------------------
# CUSTOMER CHART
# ---------------------------------------------------------

st.subheader("📈 Customer Performance")

chart_customers = (
    top_customers
    .sort_values(customer_view, ascending=True)
)

fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(
    chart_customers["Customer ID"].astype(str),
    chart_customers[customer_view]
)

ax.set_title(
    f"Top 10 Customers by {customer_view}",
    fontsize=16
)

ax.set_xlabel(customer_view)
ax.set_ylabel("Customer ID")

plt.tight_layout()

st.pyplot(fig)

# ============================================================
# CUSTOMER VALUE MATRIX
# ============================================================

st.subheader("🎯 Customer Value Matrix")

st.caption(
    "Identify high-value customers by comparing order volume, sales, "
    "profitability, and shipping performance."
)

customer_matrix = (
    filtered_df
    .groupby("Customer ID")
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

customer_matrix["Avg_Lead_Time"] = (
    customer_matrix["Avg_Lead_Time"].round(1)
)

customer_matrix["Total_Sales"] = (
    customer_matrix["Total_Sales"].round(2)
)

customer_matrix["Total_Profit"] = (
    customer_matrix["Total_Profit"].round(2)
)

fig_customer_matrix = px.scatter(
    customer_matrix,
    x="Orders",
    y="Total_Sales",
    size="Total_Profit",
    color="Avg_Lead_Time",
    hover_name="Customer ID",
    hover_data={
        "Orders": True,
        "Total_Sales": ":,.2f",
        "Total_Profit": ":,.2f",
        "Avg_Lead_Time": ":.1f"
    },
    labels={
        "Orders": "Number of Orders",
        "Total_Sales": "Total Sales",
        "Total_Profit": "Total Profit",
        "Avg_Lead_Time": "Avg Lead Time"
    },
    title="Customer Value Matrix",
    template="plotly_dark",
    height=600
)

fig_customer_matrix.update_layout(
    title=dict(
        text="Customer Value Matrix",
        font=dict(
            size=22,
            color="white"
        )
    ),
    xaxis=dict(
        title=dict(
            text="Number of Orders",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    yaxis=dict(
        title=dict(
            text="Total Sales ($)",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    margin=dict(
        l=70,
        r=40,
        t=80,
        b=60
    )
)

fig_customer_matrix.update_traces(
    marker=dict(
        opacity=0.8,
        line=dict(width=1)
    ),
    hovertemplate=(
        "<b>Customer ID: %{hovertext}</b><br>"
        "Orders: %{x:,}<br>"
        "Total Sales: $%{y:,.2f}<br>"
        "Total Profit: $%{marker.size:,.2f}<br>"
        "Avg Lead Time: %{marker.color:.1f} days"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig_customer_matrix,
    use_container_width=True
)


# ============================================================
# PRODUCT DISTRIBUTION ANALYSIS
# ============================================================

st.divider()

st.markdown(
    '<div id="product-analysis"></div>',
    unsafe_allow_html=True
)


st.header("📦 Product Distribution Analysis")

# Product-level analysis
product_analysis = (
    filtered_df.groupby(["Product ID", "Product Name"])
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

# Product KPIs
total_products = product_analysis["Product ID"].nunique()
product_orders = product_analysis["Orders"].sum()
product_sales = product_analysis["Total_Sales"].sum()

pcol1, pcol2, pcol3 = st.columns(3)

pcol1.metric(
    "📦 Total Products",
    f"{total_products:,}"
)

pcol2.metric(
    "🛒 Product Orders",
    f"{product_orders:,}"
)

pcol3.metric(
    "💰 Product Sales",
    f"${product_sales:,.2f}"
)

st.write("")

# Product ranking selector
product_rank_view = st.selectbox(
    "📊 Rank Products By",
    ["Orders", "Total Sales", "Total Profit"],
    key="product_rank"
)

# Map selector to dataframe column
product_column_map = {
    "Orders": "Orders",
    "Total Sales": "Total_Sales",
    "Total Profit": "Total_Profit"
}

product_sort_column = product_column_map[product_rank_view]

# Top 10 products
top_products = (
    product_analysis
    .sort_values(product_sort_column, ascending=False)
    .head(10)
)

st.subheader("🏆 Top 10 Products")

st.dataframe(
    top_products,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# INTERACTIVE PRODUCT PERFORMANCE
# ============================================================

st.subheader("📊 Product Performance")

st.caption(
    "Explore product contribution by orders, sales, profit, and shipping performance."
)

product_chart_data = product_analysis.copy()

# Interactive Treemap
fig_product = px.treemap(
    product_chart_data,
    path=["Product Name"],
    values=product_sort_column,
    color="Total_Profit",
    color_continuous_scale="Plasma",
    hover_data={
        "Product ID": True,
        "Orders": ":,.0f",
        "Total_Sales": ":,.2f",
        "Total_Profit": ":,.2f",
        "Avg_Lead_Time": ":,.1f"
    },
    labels={
        "Orders": "Orders",
        "Total_Sales": "Total Sales ($)",
        "Total_Profit": "Total Profit ($)",
        "Avg_Lead_Time": "Avg Lead Time (Days)"
    }
)

fig_product.update_layout(
    title=dict(
        text=f"Product Performance by {product_rank_view}",
        font=dict(
            size=22,
            color="white"
        )
    ),
    height=650,
    margin=dict(
        l=20,
        r=20,
        t=80,
        b=20
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

fig_product.update_traces(
    textinfo="label+value",
    textfont=dict(
        size=14
    ),
    hovertemplate=(
        "<b>%{label}</b><br>"
        "Orders: %{customdata[1]:,.0f}<br>"
        "Total Sales: $%{customdata[2]:,.2f}<br>"
        "Total Profit: $%{customdata[3]:,.2f}<br>"
        "Avg Lead Time: %{customdata[4]:,.1f} days"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig_product,
    use_container_width=True
)

# ============================================================
# REGIONAL PERFORMANCE ANALYSIS
# ============================================================

st.divider()
st.markdown(
    '<div id="regional-analysis"></div>',
    unsafe_allow_html=True
)


st.header("🌎 Regional Performance Analysis")

# Regional analysis
region_analysis = (
    filtered_df.groupby("Region")
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

# Regional KPIs
best_sales_region = region_analysis.loc[
    region_analysis["Total_Sales"].idxmax(), "Region"
]

best_profit_region = region_analysis.loc[
    region_analysis["Total_Profit"].idxmax(), "Region"
]

rcol1, rcol2, rcol3 = st.columns(3)

rcol1.metric(
    "🌎 Regions",
    f"{region_analysis['Region'].nunique()}"
)

rcol2.metric(
    "🏆 Top Sales Region",
    best_sales_region
)

rcol3.metric(
    "💰 Top Profit Region",
    best_profit_region
)

st.write("")

# Regional ranking selector
region_rank_view = st.selectbox(
    "📊 Rank Regions By",
    ["Orders", "Total Sales", "Total Profit", "Avg Lead Time"],
    key="region_rank"
)

region_column_map = {
    "Orders": "Orders",
    "Total Sales": "Total_Sales",
    "Total Profit": "Total_Profit",
    "Avg Lead Time": "Avg_Lead_Time"
}

region_sort_column = region_column_map[region_rank_view]

# Regional table
ranked_regions = (
    region_analysis
    .sort_values(region_sort_column, ascending=False)
)

st.subheader("🏅 Regional Performance")

st.dataframe(
    ranked_regions,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# INTERACTIVE REGIONAL COMPARISON
# ============================================================

st.subheader("📊 Regional Performance Comparison")

st.caption(
    "Compare regions across orders, sales, profit, and shipping efficiency."
)

# Prepare regional comparison data
regional_radar = ranked_regions[
    ["Region", "Orders", "Total_Sales", "Total_Profit", "Avg_Lead_Time"]
].copy()

# Normalize metrics to a 0–100 performance scale
# Higher orders, sales and profit = better
# Lower lead time = better
metrics = [
    "Orders",
    "Total_Sales",
    "Total_Profit",
    "Avg_Lead_Time"
]

for column in metrics:
    min_value = regional_radar[column].min()
    max_value = regional_radar[column].max()

    if max_value == min_value:
        regional_radar[f"{column}_Score"] = 100
    else:
        regional_radar[f"{column}_Score"] = (
            (regional_radar[column] - min_value)
            / (max_value - min_value)
        ) * 100

# Invert lead-time score because lower shipping time is better
regional_radar["Avg_Lead_Time_Score"] = (
    100 - regional_radar["Avg_Lead_Time_Score"]
)

# Create radar chart
fig_region_radar = go.Figure()

categories = [
    "Orders",
    "Sales",
    "Profit",
    "Shipping Efficiency"
]

score_columns = [
    "Orders_Score",
    "Total_Sales_Score",
    "Total_Profit_Score",
    "Avg_Lead_Time_Score"
]

for _, row in regional_radar.iterrows():

    values = [
        row[column]
        for column in score_columns
    ]

    values.append(values[0])

    fig_region_radar.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill="toself",
            name=str(row["Region"]),
            opacity=0.65,
            hovertemplate=(
                f"<b>{row['Region']}</b><br>"
                f"Orders: {row['Orders']:,.0f}<br>"
                f"Sales: ${row['Total_Sales']:,.2f}<br>"
                f"Profit: ${row['Total_Profit']:,.2f}<br>"
                f"Avg Lead Time: {row['Avg_Lead_Time']:,.1f} days"
                "<extra></extra>"
            )
        )
    )

fig_region_radar.update_layout(
    title=dict(
        text="Regional Performance Radar",
        font=dict(
            size=22,
            color="white"
        )
    ),
    height=650,
    polar=dict(
        bgcolor="rgba(0,0,0,0)",
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickfont=dict(
                size=11,
                color="white"
            ),
            gridcolor="rgba(255,255,255,0.15)"
        ),
        angularaxis=dict(
            tickfont=dict(
                size=13,
                color="white"
            ),
            gridcolor="rgba(255,255,255,0.15)"
        )
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(
        l=60,
        r=60,
        t=90,
        b=50
    ),
    legend=dict(
        title="Region",
        font=dict(
            color="white"
        )
    )
)

st.plotly_chart(
    fig_region_radar,
    use_container_width=True
)



# ============================================================
# SHIP MODE PERFORMANCE ANALYSIS
# ============================================================

st.divider()
st.markdown(
    '<div id="ship-mode-analysis"></div>',
    unsafe_allow_html=True
)

st.header("🚚 Ship Mode Performance Analysis")

# Ship mode analysis
ship_mode_analysis = (
    filtered_df.groupby("Ship Mode")
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

# Ship mode KPIs
best_ship_mode_sales = ship_mode_analysis.loc[
    ship_mode_analysis["Total_Sales"].idxmax(), "Ship Mode"
]

best_ship_mode_profit = ship_mode_analysis.loc[
    ship_mode_analysis["Total_Profit"].idxmax(), "Ship Mode"
]

fastest_ship_mode = ship_mode_analysis.loc[
    ship_mode_analysis["Avg_Lead_Time"].idxmin(), "Ship Mode"
]

scol1, scol2, scol3 = st.columns(3)

scol1.metric(
    "🏆 Top Sales Ship Mode",
    best_ship_mode_sales
)

scol2.metric(
    "💰 Top Profit Ship Mode",
    best_ship_mode_profit
)

scol3.metric(
    "⚡ Fastest Ship Mode",
    fastest_ship_mode
)

st.write("")

# Ranking selector
ship_mode_rank_view = st.selectbox(
    "📊 Rank Ship Modes By",
    [
        "Orders",
        "Total Sales",
        "Total Profit",
        "Avg Lead Time"
    ],
    key="ship_mode_rank"
)

ship_mode_column_map = {
    "Orders": "Orders",
    "Total Sales": "Total_Sales",
    "Total Profit": "Total_Profit",
    "Avg Lead Time": "Avg_Lead_Time"
}

ship_mode_sort_column = ship_mode_column_map[
    ship_mode_rank_view
]

# Ranked ship modes
ranked_ship_modes = (
    ship_mode_analysis
    .sort_values(
        ship_mode_sort_column,
        ascending=False
    )
)

st.subheader("🏅 Ship Mode Performance")

st.dataframe(
    ranked_ship_modes,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# INTERACTIVE SHIP MODE COMPARISON
# ============================================================

st.subheader("📊 Ship Mode Performance Comparison")

st.caption(
    "Compare shipping modes across orders, sales, profit, and average lead time."
)

# Prepare ship mode data
ship_mode_matrix = ranked_ship_modes[
    [
        "Ship Mode",
        "Orders",
        "Avg_Lead_Time",
        "Total_Sales",
        "Total_Profit"
    ]
].copy()

# ------------------------------------------------------------
# Normalize values to a 0–100 comparison scale
# ------------------------------------------------------------

ship_mode_scores = ship_mode_matrix.copy()

# Higher is better for these metrics
positive_metrics = [
    "Orders",
    "Total_Sales",
    "Total_Profit"
]

for column in positive_metrics:

    min_value = ship_mode_scores[column].min()
    max_value = ship_mode_scores[column].max()

    if max_value == min_value:
        ship_mode_scores[column] = 100
    else:
        ship_mode_scores[column] = (
            (ship_mode_scores[column] - min_value)
            / (max_value - min_value)
        ) * 100

# Lower shipping lead time is better
min_lead = ship_mode_matrix["Avg_Lead_Time"].min()
max_lead = ship_mode_matrix["Avg_Lead_Time"].max()

if max_lead == min_lead:

    ship_mode_scores["Avg_Lead_Time"] = 100

else:

    ship_mode_scores["Avg_Lead_Time"] = (
        100
        - (
            (ship_mode_matrix["Avg_Lead_Time"] - min_lead)
            / (max_lead - min_lead)
        ) * 100
    )

# ------------------------------------------------------------
# Create heatmap
# ------------------------------------------------------------

heatmap_data = ship_mode_scores.set_index("Ship Mode")[
    [
        "Orders",
        "Total_Sales",
        "Total_Profit",
        "Avg_Lead_Time"
    ]
]

heatmap_data.columns = [
    "Orders",
    "Sales",
    "Profit",
    "Shipping Efficiency"
]

fig_ship_heatmap = px.imshow(
    heatmap_data,
    text_auto=".1f",
    aspect="auto",
    color_continuous_scale="Plasma",
    labels={
        "x": "Performance Metric",
        "y": "Ship Mode",
        "color": "Performance Score"
    }
)

fig_ship_heatmap.update_layout(
    title=dict(
        text="Ship Mode Performance Heatmap",
        font=dict(
            size=22,
            color="white"
        )
    ),
    height=500,
    margin=dict(
        l=80,
        r=40,
        t=90,
        b=60
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        title="Performance Metric",
        tickfont=dict(
            size=13,
            color="white"
        )
    ),
    yaxis=dict(
        title="Ship Mode",
        tickfont=dict(
            size=13,
            color="white"
        )
    ),
    coloraxis_colorbar=dict(
        title="Score",
        tickfont=dict(
            color="white"
        ),
        title_font=dict(
            color="white"
        )
    )
)

# ------------------------------------------------------------
# Custom hover information
# ------------------------------------------------------------

fig_ship_heatmap.update_traces(
    customdata=[
        [
            [
                ship_mode_matrix.iloc[row]["Orders"],
                ship_mode_matrix.iloc[row]["Total_Sales"],
                ship_mode_matrix.iloc[row]["Total_Profit"],
                ship_mode_matrix.iloc[row]["Avg_Lead_Time"]
            ]
            for column in range(4)
        ]
        for row in range(len(ship_mode_matrix))
    ],
    hovertemplate=(
        "<b>Ship Mode: %{y}</b><br>"
        "Metric: %{x}<br>"
        "Performance Score: %{z:.1f}<br>"
        "<br>"
        "Orders: %{customdata[0]:,.0f}<br>"
        "Total Sales: $%{customdata[1]:,.2f}<br>"
        "Total Profit: $%{customdata[2]:,.2f}<br>"
        "Avg Lead Time: %{customdata[3]:,.1f} days"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig_ship_heatmap,
    use_container_width=True
)


# ============================================================
# PROFITABILITY ANALYSIS
# ============================================================

st.divider()
st.markdown(
    '<div id="profitability-analysis"></div>',
    unsafe_allow_html=True
)

st.header("💰 Profitability Analysis")

# Profitability calculations
profit_analysis = (
    filtered_df.groupby("Product Name")
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

# Calculate profit margin
profit_analysis["Profit_Margin"] = (
    profit_analysis["Total_Profit"]
    / profit_analysis["Total_Sales"]
    * 100
)

# Overall profitability
overall_sales = filtered_df["Sales"].sum()
overall_profit = filtered_df["Gross Profit"].sum()

overall_margin = (
    overall_profit / overall_sales * 100
    if overall_sales != 0
    else 0
)

# Highest profit product
best_profit_product = profit_analysis.loc[
    profit_analysis["Total_Profit"].idxmax(),
    "Product Name"
]

# Highest margin product
best_margin_product = profit_analysis.loc[
    profit_analysis["Profit_Margin"].idxmax(),
    "Product Name"
]

# KPI cards
pcol1, pcol2, pcol3 = st.columns(3)

pcol1.metric(
    "💵 Total Profit",
    f"${overall_profit:,.2f}"
)

pcol2.metric(
    "📈 Overall Profit Margin",
    f"{overall_margin:.2f}%"
)

pcol3.metric(
    "🏆 Most Profitable Product",
    best_profit_product
)

st.write("")

# Profitability ranking
profit_rank_view = st.selectbox(
    "📊 Rank Products By",
    [
        "Total Profit",
        "Profit Margin",
        "Total Sales"
    ],
    key="profit_rank"
)

profit_column_map = {
    "Total Profit": "Total_Profit",
    "Profit Margin": "Profit_Margin",
    "Total Sales": "Total_Sales"
}

profit_sort_column = profit_column_map[profit_rank_view]

ranked_profit = (
    profit_analysis
    .sort_values(
        profit_sort_column,
        ascending=False
    )
    .head(10)
)

# Profitability table
st.subheader("🏆 Top 10 Profitable Products")

st.dataframe(
    ranked_profit,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# INTERACTIVE PROFITABILITY ANALYSIS
# ============================================================

st.subheader("💰 Profitability Performance")

st.caption(
    "Explore the relationship between product sales, profit, order volume, "
    "and profit margin."
)

profit_chart_data = profit_analysis.copy()

# Round values for cleaner hover information
profit_chart_data["Total_Sales"] = (
    profit_chart_data["Total_Sales"].round(2)
)

profit_chart_data["Total_Profit"] = (
    profit_chart_data["Total_Profit"].round(2)
)

profit_chart_data["Profit_Margin"] = (
    profit_chart_data["Profit_Margin"].round(2)
)

# ============================================================
# INTERACTIVE PROFITABILITY BUBBLE CHART
# ============================================================

fig_profit = px.scatter(
    profit_chart_data,
    x="Total_Sales",
    y="Total_Profit",
    size="Orders",
    color="Profit_Margin",
    hover_name="Product Name",
    color_continuous_scale="Plasma",
    size_max=45,
    labels={
        "Total_Sales": "Total Sales ($)",
        "Total_Profit": "Total Profit ($)",
        "Orders": "Orders",
        "Profit_Margin": "Profit Margin (%)"
    },
    title="Sales vs Profit by Product",
    template="plotly_dark",
    height=650
)

fig_profit.update_layout(
    title=dict(
        text="Sales vs Profit by Product",
        font=dict(
            size=22,
            color="white"
        )
    ),
    xaxis=dict(
        title=dict(
            text="Total Sales ($)",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    yaxis=dict(
        title=dict(
            text="Total Profit ($)",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    margin=dict(
        l=70,
        r=70,
        t=90,
        b=60
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

fig_profit.update_traces(
    marker=dict(
        opacity=0.85,
        line=dict(
            width=1
        )
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "Total Sales: $%{x:,.2f}<br>"
        "Total Profit: $%{y:,.2f}<br>"
        "Orders: %{marker.size:,.0f}<br>"
        "Profit Margin: %{marker.color:.2f}%"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig_profit,
    use_container_width=True
)

# ============================================================
# STATE / PROVINCE PERFORMANCE ANALYSIS
# ============================================================

st.divider()
st.markdown(
    '<div id="state-analysis"></div>',
    unsafe_allow_html=True
)

st.header("🗺️ State / Province Performance")

# State-level analysis
state_analysis = (
    filtered_df.groupby(["State/Province", "Region"])
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

# Calculate profit margin
state_analysis["Profit_Margin"] = (
    state_analysis["Total_Profit"]
    / state_analysis["Total_Sales"]
    * 100
)

# KPI calculations
top_sales_state = state_analysis.loc[
    state_analysis["Total_Sales"].idxmax(),
    "State/Province"
]

top_profit_state = state_analysis.loc[
    state_analysis["Total_Profit"].idxmax(),
    "State/Province"
]

fastest_state = state_analysis.loc[
    state_analysis["Avg_Lead_Time"].idxmin(),
    "State/Province"
]

# KPI cards
st1, st2, st3 = st.columns(3)

st1.metric(
    "🏆 Top Sales State",
    top_sales_state
)

st2.metric(
    "💰 Top Profit State",
    top_profit_state
)

st3.metric(
    "⚡ Fastest State",
    fastest_state
)

st.write("")

# Ranking selector
state_rank_view = st.selectbox(
    "📊 Rank States By",
    [
        "Orders",
        "Total Sales",
        "Total Profit",
        "Profit Margin",
        "Avg Lead Time"
    ],
    key="state_rank"
)

state_column_map = {
    "Orders": "Orders",
    "Total Sales": "Total_Sales",
    "Total Profit": "Total_Profit",
    "Profit Margin": "Profit_Margin",
    "Avg Lead Time": "Avg_Lead_Time"
}

state_sort_column = state_column_map[state_rank_view]

# Ranked states
ranked_states = (
    state_analysis
    .sort_values(
        state_sort_column,
        ascending=False
    )
)

# Top 10 states
top_states = ranked_states.head(10)

st.subheader("🏅 Top 10 States / Provinces")

st.dataframe(
    top_states,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# STATE / PROVINCE PERFORMANCE CHART
# ============================================================

st.subheader("🗺️ State / Province Performance")

st.caption(
    "Compare the selected states and provinces based on the chosen performance metric."
)

# Prepare chart data
chart_states = (
    top_states
    .sort_values(
        state_sort_column,
        ascending=True
    )
)

# Interactive horizontal chart
fig_state = px.bar(
    chart_states,
    x=state_sort_column,
    y="State/Province",
    orientation="h",
    text=state_sort_column,
    color=state_sort_column,
    color_continuous_scale="Viridis",
    hover_data={
        "State/Province": True,
        "Orders": ":,",
        "Total_Sales": ":,.2f",
        "Total_Profit": ":,.2f",
        "Avg_Lead_Time": ":,.1f"
    },
    labels={
        state_sort_column: state_rank_view,
        "State/Province": "State / Province",
        "Orders": "Orders",
        "Total_Sales": "Total Sales",
        "Total_Profit": "Total Profit",
        "Avg_Lead_Time": "Avg Lead Time"
    },
    title=f"Top 10 States / Provinces by {state_rank_view}",
    template="plotly_dark",
    height=600
)

# Display values at the end of each bar
fig_state.update_traces(
    texttemplate="%{text:,.1f}",
    textposition="outside",
    hovertemplate=(
        "<b>%{y}</b><br>"
        f"{state_rank_view}: %{{x:,.2f}}<br>"
        "Orders: %{customdata[0]:,}<br>"
        "Total Sales: $%{customdata[1]:,.2f}<br>"
        "Total Profit: $%{customdata[2]:,.2f}<br>"
        "Avg Lead Time: %{customdata[3]:,.1f} days"
        "<extra></extra>"
    )
)

fig_state.update_layout(
    title=dict(
        text=f"Top 10 States / Provinces by {state_rank_view}",
        font=dict(
            size=22,
            color="white"
        )
    ),
    xaxis=dict(
        title=dict(
            text=state_rank_view,
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    yaxis=dict(
        title=dict(
            text="State / Province",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        )
    ),
    coloraxis_colorbar=dict(
        title=dict(
            text=state_rank_view,
            font=dict(color="white")
        )
    ),
    margin=dict(
        l=40,
        r=80,
        t=90,
        b=70
    )
)

# Show interactive chart
st.plotly_chart(
    fig_state,
    use_container_width=True
)

# ============================================================
# PROFITABILITY ANALYSIS
# ============================================================

st.divider()
st.markdown(
    '<div id="profitability-analysis"></div>',
    unsafe_allow_html=True
)


st.header("💰 Profitability Analysis")

st.caption(
    "Explore how products contribute to sales, profit, and overall profitability."
)

# ============================================================
# PROFITABILITY CALCULATIONS
# ============================================================

profit_analysis = (
    filtered_df
    .groupby("Product Name")
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

# Calculate profit margin
profit_analysis["Profit_Margin"] = (
    profit_analysis["Total_Profit"]
    / profit_analysis["Total_Sales"]
    * 100
)

# Round values
profit_analysis["Total_Sales"] = profit_analysis["Total_Sales"].round(2)
profit_analysis["Total_Profit"] = profit_analysis["Total_Profit"].round(2)
profit_analysis["Profit_Margin"] = profit_analysis["Profit_Margin"].round(2)
profit_analysis["Avg_Lead_Time"] = profit_analysis["Avg_Lead_Time"].round(1)

# ============================================================
# PROFITABILITY KPIs
# ============================================================

profit_col1, profit_col2, profit_col3 = st.columns(3)

overall_sales = profit_analysis["Total_Sales"].sum()
overall_profit = profit_analysis["Total_Profit"].sum()

overall_margin = (
    overall_profit / overall_sales * 100
    if overall_sales != 0
    else 0
)

best_product = (
    profit_analysis
    .sort_values("Total_Profit", ascending=False)
    .iloc[0]
)

profit_col1.metric(
    "💰 Total Profit",
    f"${overall_profit:,.2f}"
)

profit_col2.metric(
    "📊 Overall Profit Margin",
    f"{overall_margin:.2f}%"
)

profit_col3.metric(
    "🏆 Most Profitable Product",
    best_product["Product Name"]
)

st.divider()

# ============================================================
# PROFITABILITY BUBBLE CHART
# ============================================================

st.subheader("🫧 Product Profitability Map")

st.caption(
    "Bubble size represents total profit. Color represents profit margin. "
    "Hover over a product for detailed performance information."
)

fig_profit = px.scatter(
    profit_analysis,
    x="Total_Sales",
    y="Total_Profit",
    size="Total_Profit",
    color="Profit_Margin",
    hover_name="Product Name",
    hover_data={
        "Orders": ":,",
        "Total_Sales": ":,.2f",
        "Total_Profit": ":,.2f",
        "Profit_Margin": ":.2f",
        "Avg_Lead_Time": ":.1f"
    },
    color_continuous_scale="Viridis",
    size_max=55,
    labels={
        "Total_Sales": "Total Sales ($)",
        "Total_Profit": "Total Profit ($)",
        "Profit_Margin": "Profit Margin (%)",
        "Orders": "Orders",
        "Avg_Lead_Time": "Avg Lead Time (Days)"
    },
    title="Product Profitability Map",
    template="plotly_dark",
    height=650
)

fig_profit.update_traces(
    marker=dict(
        opacity=0.85,
        line=dict(width=1)
    )
)

fig_profit.update_layout(
    title=dict(
        text="Product Profitability Map",
        font=dict(
            size=22,
            color="white"
        )
    ),
    xaxis=dict(
        title=dict(
            text="Total Sales ($)",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    yaxis=dict(
        title=dict(
            text="Total Profit ($)",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    coloraxis_colorbar=dict(
        title=dict(
            text="Profit Margin (%)",
            font=dict(color="white")
        )
    ),
    margin=dict(
        l=70,
        r=80,
        t=90,
        b=70
    )
)

st.plotly_chart(
    fig_profit,
    use_container_width=True
)

# ============================================================
# TOP PROFITABLE PRODUCTS
# ============================================================

st.subheader("🏆 Top 10 Most Profitable Products")

top_profit_products = (
    profit_analysis
    .sort_values("Total_Profit", ascending=False)
    .head(10)
)

st.dataframe(
    top_profit_products[
        [
            "Product Name",
            "Orders",
            "Total_Sales",
            "Total_Profit",
            "Profit_Margin",
            "Avg_Lead_Time"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# ============================================================
# CUSTOMER - PRODUCT DISTRIBUTION ANALYSIS
# ============================================================

st.divider()
st.markdown(
    '<div id="customer-product-analysis"></div>',
    unsafe_allow_html=True
)

st.header("🔗 Customer–Product Distribution")

st.caption(
    "Explore which products are most frequently purchased by customers "
    "and identify strong customer-product relationships."
)

# ============================================================
# CUSTOMER-PRODUCT SUMMARY
# ============================================================

customer_product = (
    filtered_df
    .groupby(["Customer ID", "Product Name"])
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

# ============================================================
# DISTRIBUTION KPIs
# ============================================================

cp_col1, cp_col2, cp_col3 = st.columns(3)

cp_col1.metric(
    "👥 Active Customers",
    f"{filtered_df['Customer ID'].nunique():,}"
)

cp_col2.metric(
    "🍬 Products",
    f"{filtered_df['Product Name'].nunique():,}"
)

cp_col3.metric(
    "🔗 Customer–Product Links",
    f"{len(customer_product):,}"
)

st.divider()

# ============================================================
# PRODUCT SELECTION
# ============================================================

st.subheader("🍫 Product Distribution Explorer")

available_products = sorted(
    filtered_df["Product Name"]
    .dropna()
    .unique()
)

selected_product = st.selectbox(
    "🍬 Choose a Product",
    options=available_products,
    key="customer_product_selector"
)

product_customers = (
    customer_product[
        customer_product["Product Name"] == selected_product
    ]
    .sort_values("Orders", ascending=False)
    .head(15)
)

# ============================================================
# CUSTOMER DISTRIBUTION CHART
# ============================================================

st.subheader("👥 Customer Distribution")

fig_customer_product = px.scatter(
    product_customers,
    x="Orders",
    y="Total_Sales",
    size="Total_Profit",
    color="Total_Profit",
    hover_name="Customer ID",
    hover_data={
        "Orders": ":,",
        "Total_Sales": ":,.2f",
        "Total_Profit": ":,.2f"
    },
    color_continuous_scale="Viridis",
    size_max=50,
    labels={
        "Orders": "Number of Orders",
        "Total_Sales": "Total Sales ($)",
        "Total_Profit": "Total Profit ($)"
    },
    title=f"Customer Distribution — {selected_product}",
    template="plotly_dark",
    height=600
)

fig_customer_product.update_traces(
    marker=dict(
        opacity=0.85,
        line=dict(width=1)
    )
)

fig_customer_product.update_layout(
    title=dict(
        text=f"Customer Distribution — {selected_product}",
        font=dict(
            size=22,
            color="white"
        )
    ),
    xaxis=dict(
        title=dict(
            text="Number of Orders",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    yaxis=dict(
        title=dict(
            text="Total Sales ($)",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    coloraxis_colorbar=dict(
        title=dict(
            text="Total Profit ($)",
            font=dict(color="white")
        )
    ),
    margin=dict(
        l=70,
        r=80,
        t=90,
        b=70
    )
)

st.plotly_chart(
    fig_customer_product,
    use_container_width=True
)

# ============================================================
# CUSTOMER-PRODUCT DETAILS
# ============================================================

st.subheader("📋 Customer–Product Details")

st.dataframe(
    product_customers[
        [
            "Customer ID",
            "Product Name",
            "Orders",
            "Total_Sales",
            "Total_Profit"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# ============================================================
# TIME-BASED DISTRIBUTION ANALYSIS
# ============================================================

st.divider()
st.markdown(
    '<div id="time-analysis"></div>',
    unsafe_allow_html=True
)

st.header("📅 Time-Based Distribution Analysis")

st.caption(
    "Analyze how orders, sales, profit, and shipping performance "
    "change over time."
)

# ============================================================
# MONTHLY DATA
# ============================================================

monthly_analysis = (
    filtered_df
    .dropna(subset=["Order Date"])
    .assign(
        Month=lambda x: x["Order Date"].dt.to_period("M").astype(str)
    )
    .groupby("Month")
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

# Round values
monthly_analysis["Total_Sales"] = (
    monthly_analysis["Total_Sales"].round(2)
)

monthly_analysis["Total_Profit"] = (
    monthly_analysis["Total_Profit"].round(2)
)

monthly_analysis["Avg_Lead_Time"] = (
    monthly_analysis["Avg_Lead_Time"].round(1)
)

# ============================================================
# TIME ANALYSIS KPIs
# ============================================================

time_col1, time_col2, time_col3, time_col4 = st.columns(4)

peak_sales_month = (
    monthly_analysis
    .loc[monthly_analysis["Total_Sales"].idxmax(), "Month"]
)

peak_profit_month = (
    monthly_analysis
    .loc[monthly_analysis["Total_Profit"].idxmax(), "Month"]
)

peak_orders_month = (
    monthly_analysis
    .loc[monthly_analysis["Orders"].idxmax(), "Month"]
)

time_col1.metric(
    "📆 Months Analyzed",
    f"{len(monthly_analysis):,}"
)

time_col2.metric(
    "💰 Peak Sales Month",
    peak_sales_month
)

time_col3.metric(
    "💵 Peak Profit Month",
    peak_profit_month
)

time_col4.metric(
    "📦 Peak Orders Month",
    peak_orders_month
)

st.divider()

# ============================================================
# METRIC SELECTOR
# ============================================================

st.subheader("📈 Distribution Trend")

trend_metric = st.selectbox(
    "📊 Choose a Metric to Analyze",
    options=[
        "Orders",
        "Total_Sales",
        "Total_Profit",
        "Avg_Lead_Time"
    ],
    format_func=lambda x: {
        "Orders": "📦 Orders",
        "Total_Sales": "💰 Total Sales",
        "Total_Profit": "💵 Total Profit",
        "Avg_Lead_Time": "🚚 Average Shipping Lead Time"
    }[x],
    key="time_trend_metric"
)

# ============================================================
# TREND CHART
# ============================================================

metric_labels = {
    "Orders": "Number of Orders",
    "Total_Sales": "Total Sales ($)",
    "Total_Profit": "Total Profit ($)",
    "Avg_Lead_Time": "Average Lead Time (Days)"
}

fig_time = px.line(
    monthly_analysis,
    x="Month",
    y=trend_metric,
    markers=True,
    hover_data={
        "Orders": ":,",
        "Total_Sales": ":,.2f",
        "Total_Profit": ":,.2f",
        "Avg_Lead_Time": ":,.1f"
    },
    labels={
        "Month": "Month",
        trend_metric: metric_labels[trend_metric]
    },
    title=f"Monthly {metric_labels[trend_metric]}",
    template="plotly_dark",
    height=600
)

fig_time.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)

fig_time.update_layout(
    title=dict(
        text=f"Monthly {metric_labels[trend_metric]}",
        font=dict(
            size=22,
            color="white"
        )
    ),
    xaxis=dict(
        title=dict(
            text="Month",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)",
        tickangle=-45
    ),
    yaxis=dict(
        title=dict(
            text=metric_labels[trend_metric],
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    hovermode="x unified",
    margin=dict(
        l=70,
        r=40,
        t=90,
        b=100
    )
)

st.plotly_chart(
    fig_time,
    use_container_width=True
)

# ============================================================
# MONTHLY PERFORMANCE TABLE
# ============================================================

st.subheader("📋 Monthly Performance Details")

st.dataframe(
    monthly_analysis,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# ORDER DISTRIBUTION ANALYSIS
# ============================================================

st.divider()
st.markdown(
    '<div id="order-analysis"></div>',
    unsafe_allow_html=True
)

st.header("📦 Order Distribution Analysis")

st.caption(
    "Understand order size, sales distribution, and unusual order values "
    "across the selected data."
)

# ============================================================
# ORDER-LEVEL DATA
# ============================================================

order_analysis = (
    filtered_df
    .groupby("Order ID")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Shipping_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

order_analysis["Profit_Margin"] = (
    order_analysis["Profit"]
    / order_analysis["Sales"]
    * 100
)

order_analysis["Profit_Margin"] = (
    order_analysis["Profit_Margin"]
    .replace([float("inf"), -float("inf")], 0)
    .fillna(0)
)

# ============================================================
# ORDER DISTRIBUTION KPIs
# ============================================================

order_col1, order_col2, order_col3, order_col4 = st.columns(4)

order_col1.metric(
    "📦 Orders Analyzed",
    f"{len(order_analysis):,}"
)

order_col2.metric(
    "💰 Avg Order Value",
    f"${order_analysis['Sales'].mean():,.2f}"
)

order_col3.metric(
    "💵 Avg Order Profit",
    f"${order_analysis['Profit'].mean():,.2f}"
)

order_col4.metric(
    "🚚 Avg Order Lead Time",
    f"{order_analysis['Shipping_Lead_Time'].mean():,.1f} days"
)

st.divider()

# ============================================================
# SALES DISTRIBUTION
# ============================================================

st.subheader("📊 Order Sales Distribution")

fig_sales_dist = px.histogram(
    order_analysis,
    x="Sales",
    nbins=30,
    marginal="box",
    hover_data={
        "Sales": ":,.2f",
        "Profit": ":,.2f",
        "Shipping_Lead_Time": ":,.1f"
    },
    labels={
        "Sales": "Order Sales ($)"
    },
    title="Distribution of Order Sales",
    template="plotly_dark",
    height=600
)

fig_sales_dist.update_traces(
    marker_line_width=1,
    opacity=0.85
)

fig_sales_dist.update_layout(
    title=dict(
        text="Distribution of Order Sales",
        font=dict(
            size=22,
            color="white"
        )
    ),
    xaxis=dict(
        title=dict(
            text="Order Sales ($)",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    yaxis=dict(
        title=dict(
            text="Number of Orders",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    margin=dict(
        l=70,
        r=40,
        t=90,
        b=70
    )
)

st.plotly_chart(
    fig_sales_dist,
    use_container_width=True
)

# ============================================================
# PROFIT DISTRIBUTION
# ============================================================

st.subheader("💵 Order Profit Distribution")

fig_profit_dist = px.box(
    order_analysis,
    y="Profit",
    points="all",
    hover_data={
        "Sales": ":,.2f",
        "Profit": ":,.2f",
        "Profit_Margin": ":.2f",
        "Shipping_Lead_Time": ":,.1f"
    },
    labels={
        "Profit": "Order Profit ($)"
    },
    title="Order Profit Distribution",
    template="plotly_dark",
    height=550
)

fig_profit_dist.update_traces(
    marker=dict(
        opacity=0.65,
        size=6
    )
)

fig_profit_dist.update_layout(
    title=dict(
        text="Order Profit Distribution",
        font=dict(
            size=22,
            color="white"
        )
    ),
    yaxis=dict(
        title=dict(
            text="Order Profit ($)",
            font=dict(
                size=14,
                color="white"
            )
        ),
        tickfont=dict(
            size=12,
            color="white"
        ),
        gridcolor="rgba(255,255,255,0.12)"
    ),
    margin=dict(
        l=70,
        r=40,
        t=90,
        b=70
    )
)

st.plotly_chart(
    fig_profit_dist,
    use_container_width=True
)


# ------------------------------------------------------------
# SHIPPING INSIGHTS
# ------------------------------------------------------------

st.divider()
st.markdown(
    '<div id="shipping-insights"></div>',
    unsafe_allow_html=True
)

st.header("📦 Shipping Insights")

st.caption(
    "Explore shipping volume, delivery time, and financial performance "
    "across different shipping modes."
)

# ------------------------------------------------------------
# Prepare shipping-mode summary
# ------------------------------------------------------------

shipping_summary = (
    filtered_df.groupby("Ship Mode")
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

shipping_summary["Avg_Lead_Time"] = shipping_summary["Avg_Lead_Time"].round(1)
shipping_summary["Total_Sales"] = shipping_summary["Total_Sales"].round(2)
shipping_summary["Total_Profit"] = shipping_summary["Total_Profit"].round(2)

# ------------------------------------------------------------
# Interactive metric selector
# ------------------------------------------------------------

insight_metric = st.selectbox(
    "📊 Select Shipping Metric",
    [
        "Orders",
        "Average Lead Time",
        "Total Sales",
        "Total Profit"
    ],
    key="shipping_insight_metric"
)

metric_columns = {
    "Orders": "Orders",
    "Average Lead Time": "Avg_Lead_Time",
    "Total Sales": "Total_Sales",
    "Total Profit": "Total_Profit"
}

selected_column = metric_columns[insight_metric]

shipping_chart = shipping_summary.sort_values(
    selected_column,
    ascending=True
)

# ------------------------------------------------------------
# Interactive Plotly chart
# ------------------------------------------------------------

fig_shipping_insights = px.bar(
    shipping_chart,
    x=selected_column,
    y="Ship Mode",
    orientation="h",
    text=selected_column,
    title=f"{insight_metric} by Shipping Mode",
    template="plotly_dark",
    height=500
)

# Format values displayed on chart
if insight_metric in ["Total Sales", "Total Profit"]:
    fig_shipping_insights.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            f"{insight_metric}: $%{{x:,.2f}}"
            "<extra></extra>"
        )
    )

elif insight_metric == "Average Lead Time":
    fig_shipping_insights.update_traces(
        texttemplate="%{text:.1f} days",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Average Lead Time: %{x:.1f} days"
            "<extra></extra>"
        )
    )

else:
    fig_shipping_insights.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Orders: %{x:,}"
            "<extra></extra>"
        )
    )

fig_shipping_insights.update_layout(
    title=dict(
        text=f"{insight_metric} by Shipping Mode",
        font=dict(size=22, color="white")
    ),
    xaxis=dict(
        title=insight_metric,
        color="white",
        gridcolor="#292e3a"
    ),
    yaxis=dict(
        title="Shipping Mode",
        color="white"
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=80, t=70, b=40)
)

st.plotly_chart(
    fig_shipping_insights,
    use_container_width=True
)

# ------------------------------------------------------------
# Shipping Mode Summary
# ------------------------------------------------------------

st.subheader("📌 Shipping Mode Summary")

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

best_orders_mode = shipping_summary.loc[
    shipping_summary["Orders"].idxmax(),
    "Ship Mode"
]

best_sales_mode = shipping_summary.loc[
    shipping_summary["Total_Sales"].idxmax(),
    "Ship Mode"
]

best_profit_mode = shipping_summary.loc[
    shipping_summary["Total_Profit"].idxmax(),
    "Ship Mode"
]

fastest_shipping_mode = shipping_summary.loc[
    shipping_summary["Avg_Lead_Time"].idxmin(),
    "Ship Mode"
]

with summary_col1:
    st.metric(
        "📦 Most Orders",
        best_orders_mode
    )

with summary_col2:
    st.metric(
        "💰 Highest Sales",
        best_sales_mode
    )

with summary_col3:
    st.metric(
        "💵 Highest Profit",
        best_profit_mode
    )

with summary_col4:
    st.metric(
        "⚡ Fastest Shipping",
        fastest_shipping_mode
    )


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.divider()
st.markdown(
    '<div id="executive-summary"></div>',
    unsafe_allow_html=True
)

st.header("💡 Executive Summary")
st.info(
    "💡 Use the interactive filters and analysis sections above to "
    "identify shipping patterns, high-risk areas, route performance, "
    "and operational bottlenecks."
)

st.caption(
    "Key operational insights generated from the currently selected "
    "dashboard filters."
)

# ------------------------------------------------------------
# Overall filtered-data metrics
# ------------------------------------------------------------

summary_orders = len(filtered_df)

summary_sales = filtered_df["Sales"].sum()

summary_profit = filtered_df["Gross Profit"].sum()

summary_avg_lead = filtered_df["Shipping Lead Time"].mean()


# ------------------------------------------------------------
# Shipping Mode Analysis
# ------------------------------------------------------------

mode_summary = (
    filtered_df.groupby("Ship Mode")
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

fastest_mode = mode_summary.loc[
    mode_summary["Avg_Lead_Time"].idxmin(),
    "Ship Mode"
]

slowest_mode = mode_summary.loc[
    mode_summary["Avg_Lead_Time"].idxmax(),
    "Ship Mode"
]


# ------------------------------------------------------------
# State / Province Analysis
# ------------------------------------------------------------

state_summary = (
    filtered_df.groupby("State/Province")
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

fastest_state = state_summary.loc[
    state_summary["Avg_Lead_Time"].idxmin(),
    "State/Province"
]

slowest_state = state_summary.loc[
    state_summary["Avg_Lead_Time"].idxmax(),
    "State/Province"
]


# ------------------------------------------------------------
# Executive Insight Cards
# ------------------------------------------------------------

ecol1, ecol2 = st.columns(2)

with ecol1:
    st.success(
        f"⚡ **Fastest Shipping Mode: {fastest_mode}**\n\n"
        f"This mode records the lowest average shipping lead time "
        f"among the currently selected data."
    )

with ecol2:
    st.warning(
        f"🐌 **Slowest Shipping Mode: {slowest_mode}**\n\n"
        f"This mode records the highest average shipping lead time "
        f"and may require operational attention."
    )

st.write("")

ecol3, ecol4 = st.columns(2)

with ecol3:
    st.info(
        f"🚚 **Fastest State / Province: {fastest_state}**\n\n"
        f"This location records the lowest average shipping lead time "
        f"among the selected locations."
    )

with ecol4:
    st.error(
        f"⚠️ **Slowest State / Province: {slowest_state}**\n\n"
        f"This location records the highest average shipping lead time "
        f"and should be investigated for potential delivery bottlenecks."
    )


# ------------------------------------------------------------
# Executive KPI Snapshot
# ------------------------------------------------------------

st.subheader("📊 Executive KPI Snapshot")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Orders Analyzed",
        f"{summary_orders:,}"
    )

with kpi2:
    st.metric(
        "Total Sales",
        f"${summary_sales:,.0f}"
    )

with kpi3:
    st.metric(
        "Total Profit",
        f"${summary_profit:,.0f}"
    )

with kpi4:
    st.metric(
        "Avg Lead Time",
        f"{summary_avg_lead:.1f} days"
    )


# ------------------------------------------------------------
# Business Summary
# ------------------------------------------------------------

st.subheader("📋 Business Summary")

st.write(
    f"""
    Based on the currently selected filters, the dataset contains
    **{summary_orders:,} orders**, generating **${summary_sales:,.2f}**
    in sales and **${summary_profit:,.2f}** in gross profit.

    The average shipping lead time is approximately
    **{summary_avg_lead:.1f} days**.

    From an operational perspective, **{fastest_mode}** is the fastest
    shipping mode, while **{slowest_mode}** has the highest average
    shipping lead time.

    At the geographic level, **{fastest_state}** records the lowest
    average lead time, whereas **{slowest_state}** records the highest.
    These locations can be used to identify opportunities for route
    optimization and delivery-performance improvement.
    """
)


# ------------------------------------------------------------
# Shipping Mode Performance Table
# ------------------------------------------------------------

st.subheader("🚚 Shipping Mode Performance")

shipping_display = shipping_summary.copy()

shipping_display["Avg Lead Time"] = (
    shipping_display["Avg_Lead_Time"].map(lambda x: f"{x:.1f} days")
)

shipping_display["Sales"] = (
    shipping_display["Total_Sales"].map(lambda x: f"${x:,.2f}")
)

shipping_display["Profit"] = (
    shipping_display["Total_Profit"].map(lambda x: f"${x:,.2f}")
)

shipping_display = shipping_display[
    [
        "Ship Mode",
        "Orders",
        "Avg Lead Time",
        "Sales",
        "Profit"
    ]
]

st.dataframe(
    shipping_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# GEOGRAPHIC DISTRIBUTION ANALYSIS
# ============================================================

st.divider()
st.markdown(
    '<div id="geographic-analysis"></div>',
    unsafe_allow_html=True
)

st.header("🗺️ Geographic Distribution Analysis")

st.caption(
    "Explore shipping performance across states and provinces using "
    "interactive geographic and operational views."
)

# ------------------------------------------------------------
# Prepare geographic summary
# ------------------------------------------------------------

geo_analysis = (
    filtered_df.groupby("State/Province")
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Delayed_Orders=("Shipping Lead Time", lambda x: (x >= 5).sum())
    )
    .reset_index()
)

geo_analysis["Delay_Rate"] = (
    geo_analysis["Delayed_Orders"]
    / geo_analysis["Orders"]
    * 100
)

geo_analysis["Avg_Lead_Time"] = geo_analysis["Avg_Lead_Time"].round(1)
geo_analysis["Delay_Rate"] = geo_analysis["Delay_Rate"].round(1)
geo_analysis["Total_Sales"] = geo_analysis["Total_Sales"].round(2)
geo_analysis["Total_Profit"] = geo_analysis["Total_Profit"].round(2)

# ------------------------------------------------------------
# Geographic metric selector
# ------------------------------------------------------------

geo_metric = st.selectbox(
    "🌎 Select Geographic Metric",
    [
        "Orders",
        "Average Lead Time",
        "Total Sales",
        "Total Profit",
        "Delay Rate"
    ],
    key="geographic_metric"
)

geo_metric_columns = {
    "Orders": "Orders",
    "Average Lead Time": "Avg_Lead_Time",
    "Total Sales": "Total_Sales",
    "Total Profit": "Total_Profit",
    "Delay Rate": "Delay_Rate"
}

geo_selected_column = geo_metric_columns[geo_metric]

# ------------------------------------------------------------
# State name → abbreviation mapping
# ------------------------------------------------------------

state_abbreviations = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC"
}

geo_analysis["State_Code"] = (
    geo_analysis["State/Province"]
    .map(state_abbreviations)
    .fillna(geo_analysis["State/Province"])
)

# ------------------------------------------------------------
# Interactive geographic heatmap
# ------------------------------------------------------------

us_geo = geo_analysis[
    geo_analysis["State_Code"].isin(state_abbreviations.values())
].copy()

if len(us_geo) > 0:

    fig_geo = px.choropleth(
        us_geo,
        locations="State_Code",
        locationmode="USA-states",
        color=geo_selected_column,
        scope="usa",
        hover_name="State/Province",
        hover_data={
            "State_Code": False,
            "Orders": ":,",
            "Avg_Lead_Time": ":.1f",
            "Total_Sales": ":,.2f",
            "Total_Profit": ":,.2f",
            "Delay_Rate": ":.1f"
        },
        title=f"{geo_metric} by State",
        template="plotly_dark",
        height=600
    )

    fig_geo.update_layout(
        title=dict(
            text=f"{geo_metric} by State",
            font=dict(size=22, color="white")
        ),
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            lakecolor="#0e1117",
            landcolor="#161a23",
            subunitcolor="#292e3a"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=70, b=0)
    )

    st.plotly_chart(
        fig_geo,
        use_container_width=True
    )

else:

    st.info(
        "The current filtered data does not contain recognizable "
        "US state values for the geographic map."
    )


# ------------------------------------------------------------
# Geographic KPI cards
# ------------------------------------------------------------

st.subheader("📍 Geographic Performance Snapshot")

geo_col1, geo_col2, geo_col3, geo_col4 = st.columns(4)

highest_volume_state = geo_analysis.loc[
    geo_analysis["Orders"].idxmax(),
    "State/Province"
]

highest_sales_state = geo_analysis.loc[
    geo_analysis["Total_Sales"].idxmax(),
    "State/Province"
]

fastest_geo_state = geo_analysis.loc[
    geo_analysis["Avg_Lead_Time"].idxmin(),
    "State/Province"
]

highest_delay_state = geo_analysis.loc[
    geo_analysis["Delay_Rate"].idxmax(),
    "State/Province"
]

with geo_col1:
    st.metric(
        "📦 Highest Order Volume",
        highest_volume_state
    )

with geo_col2:
    st.metric(
        "💰 Highest Sales",
        highest_sales_state
    )

with geo_col3:
    st.metric(
        "⚡ Fastest Location",
        fastest_geo_state
    )

with geo_col4:
    st.metric(
        "⚠️ Highest Delay Rate",
        highest_delay_state
    )


# ------------------------------------------------------------
# Geographic performance table
# ------------------------------------------------------------

st.subheader("📋 State / Province Performance")

geo_display = geo_analysis.sort_values(
    geo_selected_column,
    ascending=False
).copy()

geo_display["Avg Lead Time"] = (
    geo_display["Avg_Lead_Time"]
    .map(lambda x: f"{x:.1f} days")
)

geo_display["Delay Rate"] = (
    geo_display["Delay_Rate"]
    .map(lambda x: f"{x:.1f}%")
)

geo_display["Sales"] = (
    geo_display["Total_Sales"]
    .map(lambda x: f"${x:,.2f}")
)

geo_display["Profit"] = (
    geo_display["Total_Profit"]
    .map(lambda x: f"${x:,.2f}")
)

geo_display = geo_display[
    [
        "State/Province",
        "Orders",
        "Avg Lead Time",
        "Delay Rate",
        "Sales",
        "Profit"
    ]
]

st.dataframe(
    geo_display,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# BOTTLENECK DETECTION & LOGISTICS RECOMMENDATIONS
# ============================================================

st.divider()
st.markdown(
    '<div id="bottleneck-analysis"></div>',
    unsafe_allow_html=True
)

st.header("🚦 Bottleneck Detection & Logistics Recommendations")

st.caption(
    "Identify high-risk shipping locations and generate data-driven "
    "recommendations for improving delivery efficiency."
)

# ------------------------------------------------------------
# Prepare bottleneck analysis
# ------------------------------------------------------------

bottleneck_analysis = (
    filtered_df.groupby(["State/Province", "Region"])
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Delayed_Orders=(
            "Shipping Lead Time",
            lambda x: (x >= 5).sum()
        )
    )
    .reset_index()
)

bottleneck_analysis["Delay_Rate"] = (
    bottleneck_analysis["Delayed_Orders"]
    / bottleneck_analysis["Orders"]
    * 100
)

# ------------------------------------------------------------
# Bottleneck score
# ------------------------------------------------------------

# Higher lead time and delay rate indicate greater operational risk.
# Order volume is included to identify high-volume bottlenecks.

bottleneck_analysis["Bottleneck_Score"] = (
    bottleneck_analysis["Avg_Lead_Time"].rank(pct=True) * 40
    + bottleneck_analysis["Delay_Rate"].rank(pct=True) * 40
    + bottleneck_analysis["Orders"].rank(pct=True) * 20
)

bottleneck_analysis["Bottleneck_Score"] = (
    bottleneck_analysis["Bottleneck_Score"].round(1)
)

# ------------------------------------------------------------
# Risk classification
# ------------------------------------------------------------

def classify_risk(score):
    if score >= 75:
        return "🔴 Critical"
    elif score >= 50:
        return "🟠 High"
    elif score >= 25:
        return "🟡 Moderate"
    else:
        return "🟢 Low"


bottleneck_analysis["Risk Level"] = (
    bottleneck_analysis["Bottleneck_Score"]
    .apply(classify_risk)
)

# ------------------------------------------------------------
# Top bottlenecks
# ------------------------------------------------------------

top_bottlenecks = bottleneck_analysis.sort_values(
    "Bottleneck_Score",
    ascending=False
).head(10)

# ------------------------------------------------------------
# Bottleneck KPI cards
# ------------------------------------------------------------

critical_count = (
    bottleneck_analysis["Risk Level"]
    .eq("🔴 Critical")
    .sum()
)

high_risk_count = (
    bottleneck_analysis["Risk Level"]
    .eq("🟠 High")
    .sum()
)

highest_risk_location = bottleneck_analysis.loc[
    bottleneck_analysis["Bottleneck_Score"].idxmax(),
    "State/Province"
]

highest_delay_location = bottleneck_analysis.loc[
    bottleneck_analysis["Delay_Rate"].idxmax(),
    "State/Province"
]

bcol1, bcol2, bcol3, bcol4 = st.columns(4)

with bcol1:
    st.metric(
        "🔴 Critical Locations",
        f"{critical_count:,}"
    )

with bcol2:
    st.metric(
        "🟠 High-Risk Locations",
        f"{high_risk_count:,}"
    )

with bcol3:
    st.metric(
        "🚨 Highest-Risk Location",
        highest_risk_location
    )

with bcol4:
    st.metric(
        "⚠️ Highest Delay Rate",
        highest_delay_location
    )

# ------------------------------------------------------------
# Bottleneck chart
# ------------------------------------------------------------

st.subheader("🚨 Top Shipping Bottlenecks")

fig_bottleneck = px.scatter(
    top_bottlenecks,
    x="Avg_Lead_Time",
    y="Delay_Rate",
    size="Orders",
    color="Bottleneck_Score",
    hover_name="State/Province",
    hover_data={
        "Region": True,
        "Orders": ":,",
        "Avg_Lead_Time": ":.1f",
        "Delay_Rate": ":.1f",
        "Total_Sales": ":,.2f",
        "Total_Profit": ":,.2f",
        "Bottleneck_Score": ":.1f"
    },
    title="Shipping Bottleneck Risk Matrix",
    labels={
        "Avg_Lead_Time": "Average Lead Time (Days)",
        "Delay_Rate": "Delay Rate (%)",
        "Bottleneck_Score": "Bottleneck Score"
    },
    template="plotly_dark",
    height=600
)

fig_bottleneck.update_layout(
    title=dict(
        text="Shipping Bottleneck Risk Matrix",
        font=dict(size=22, color="white")
    ),
    xaxis=dict(
        title="Average Lead Time (Days)",
        color="white",
        gridcolor="#292e3a"
    ),
    yaxis=dict(
        title="Delay Rate (%)",
        color="white",
        gridcolor="#292e3a"
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=40, t=70, b=40)
)

st.plotly_chart(
    fig_bottleneck,
    use_container_width=True
)

# ------------------------------------------------------------
# Bottleneck details table
# ------------------------------------------------------------

st.subheader("📋 Highest-Risk Shipping Locations")

bottleneck_display = top_bottlenecks.copy()

bottleneck_display["Avg Lead Time"] = (
    bottleneck_display["Avg_Lead_Time"]
    .map(lambda x: f"{x:.1f} days")
)

bottleneck_display["Delay Rate"] = (
    bottleneck_display["Delay_Rate"]
    .map(lambda x: f"{x:.1f}%")
)

bottleneck_display["Sales"] = (
    bottleneck_display["Total_Sales"]
    .map(lambda x: f"${x:,.2f}")
)

bottleneck_display["Profit"] = (
    bottleneck_display["Total_Profit"]
    .map(lambda x: f"${x:,.2f}")
)

bottleneck_display = bottleneck_display[
    [
        "State/Province",
        "Region",
        "Orders",
        "Avg Lead Time",
        "Delay Rate",
        "Sales",
        "Profit",
        "Bottleneck_Score",
        "Risk Level"
    ]
]

bottleneck_display = bottleneck_display.rename(
    columns={
        "Bottleneck_Score": "Risk Score"
    }
)

st.dataframe(
    bottleneck_display,
    use_container_width=True,
    hide_index=True
)

# ------------------------------------------------------------
# Automated logistics recommendations
# ------------------------------------------------------------

st.subheader("💡 Logistics Recommendations")

overall_delay_rate = (
    (filtered_df["Shipping Lead Time"] >= 5).sum()
    / len(filtered_df)
    * 100
)

overall_avg_lead = filtered_df["Shipping Lead Time"].mean()

recommendation_col1, recommendation_col2 = st.columns(2)

with recommendation_col1:

    if overall_delay_rate >= 30:
        st.error(
            f"🔴 **Priority Action — Delivery Delays**\n\n"
            f"The current filtered data shows a delay rate of "
            f"**{overall_delay_rate:.1f}%**. Focus on high-delay "
            f"locations and review route planning and carrier allocation."
        )

    elif overall_delay_rate >= 15:
        st.warning(
            f"🟠 **Monitor Delivery Delays**\n\n"
            f"The current delay rate is **{overall_delay_rate:.1f}%**. "
            f"Prioritize the highest-risk locations for operational review."
        )

    else:
        st.success(
            f"🟢 **Delivery Performance is Stable**\n\n"
            f"The current delay rate is **{overall_delay_rate:.1f}%**. "
            f"Continue monitoring locations with rising lead times."
        )

with recommendation_col2:

    if overall_avg_lead >= 7:
        st.error(
            f"🚨 **Lead-Time Optimization Required**\n\n"
            f"Average shipping lead time is **{overall_avg_lead:.1f} days**. "
            f"Review slow routes and consider alternative shipping modes."
        )

    elif overall_avg_lead >= 5:
        st.warning(
            f"⚠️ **Lead-Time Improvement Opportunity**\n\n"
            f"Average shipping lead time is **{overall_avg_lead:.1f} days**. "
            f"Focus improvement efforts on the slowest routes."
        )

    else:
        st.success(
            f"⚡ **Efficient Delivery Performance**\n\n"
            f"Average shipping lead time is **{overall_avg_lead:.1f} days**. "
            f"Maintain current routing and shipping practices."
        )

# ------------------------------------------------------------
# Key recommended actions
# ------------------------------------------------------------

st.markdown("### 🎯 Recommended Actions")

actions_col1, actions_col2, actions_col3 = st.columns(3)

with actions_col1:
    st.info(
        "**1. Optimize High-Risk Routes**\n\n"
        "Investigate locations with high delay rates and long average "
        "lead times. Review carrier allocation and route planning."
    )

with actions_col2:
    st.info(
        "**2. Review Shipping Modes**\n\n"
        "Compare shipping modes based on delivery speed, order volume, "
        "sales, and profitability before reallocating shipments."
    )

with actions_col3:
    st.info(
        "**3. Monitor Bottlenecks Regularly**\n\n"
        "Track lead time and delay-rate trends to detect emerging "
        "logistics bottlenecks before they affect service reliability."
    )
    
    
    # ============================================================
# ROUTE EFFICIENCY TREND ANALYSIS
# ============================================================

st.divider()
st.markdown(
    '<div id="route-trend"></div>',
    unsafe_allow_html=True
)

st.header("📈 Route Efficiency Trend")

st.caption(
    "Track how shipping efficiency changes over time using monthly "
    "order volume, sales, profit, and delivery lead time."
)

# ------------------------------------------------------------
# Prepare monthly analysis
# ------------------------------------------------------------

trend_df = filtered_df.copy()

trend_df["Order Month"] = (
    trend_df["Order Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_trend = (
    trend_df.groupby("Order Month")
    .agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

monthly_trend["Avg_Lead_Time"] = (
    monthly_trend["Avg_Lead_Time"].round(2)
)

monthly_trend["Total_Sales"] = (
    monthly_trend["Total_Sales"].round(2)
)

monthly_trend["Total_Profit"] = (
    monthly_trend["Total_Profit"].round(2)
)

# Convert month to datetime for proper ordering
monthly_trend["Month"] = pd.to_datetime(
    monthly_trend["Order Month"]
)

monthly_trend = monthly_trend.sort_values("Month")

# ------------------------------------------------------------
# Metric selector
# ------------------------------------------------------------

trend_metric = st.selectbox(
    "📊 Select Trend Metric",
    [
        "Orders",
        "Average Lead Time",
        "Total Sales",
        "Total Profit"
    ],
    key="route_trend_metric"
)

trend_metric_columns = {
    "Orders": "Orders",
    "Average Lead Time": "Avg_Lead_Time",
    "Total Sales": "Total_Sales",
    "Total Profit": "Total_Profit"
}

trend_column = trend_metric_columns[trend_metric]

# ------------------------------------------------------------
# Interactive trend chart
# ------------------------------------------------------------

fig_trend = px.line(
    monthly_trend,
    x="Month",
    y=trend_column,
    markers=True,
    title=f"Monthly {trend_metric} Trend",
    template="plotly_dark",
    hover_data={
        "Orders": ":,",
        "Avg_Lead_Time": ":.2f",
        "Total_Sales": ":,.2f",
        "Total_Profit": ":,.2f"
    },
    labels={
        "Month": "Order Month",
        trend_column: trend_metric
    },
    height=550
)

fig_trend.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)

fig_trend.update_layout(
    title=dict(
        text=f"Monthly {trend_metric} Trend",
        font=dict(size=22, color="white")
    ),
    xaxis=dict(
        title="Order Month",
        color="white",
        gridcolor="#292e3a"
    ),
    yaxis=dict(
        title=trend_metric,
        color="white",
        gridcolor="#292e3a"
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    hovermode="x unified",
    margin=dict(l=20, r=30, t=70, b=40)
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

# ------------------------------------------------------------
# Trend KPIs
# ------------------------------------------------------------

st.subheader("📌 Monthly Trend Snapshot")

peak_orders_month = monthly_trend.loc[
    monthly_trend["Orders"].idxmax(),
    "Order Month"
]

peak_sales_month = monthly_trend.loc[
    monthly_trend["Total_Sales"].idxmax(),
    "Order Month"
]

fastest_month = monthly_trend.loc[
    monthly_trend["Avg_Lead_Time"].idxmin(),
    "Order Month"
]

slowest_month = monthly_trend.loc[
    monthly_trend["Avg_Lead_Time"].idxmax(),
    "Order Month"
]

trend_col1, trend_col2, trend_col3, trend_col4 = st.columns(4)

with trend_col1:
    st.metric(
        "📦 Peak Order Month",
        peak_orders_month
    )

with trend_col2:
    st.metric(
        "💰 Peak Sales Month",
        peak_sales_month
    )

with trend_col3:
    st.metric(
        "⚡ Fastest Month",
        fastest_month
    )

with trend_col4:
    st.metric(
        "🐌 Slowest Month",
        slowest_month
    )

# ------------------------------------------------------------
# Monthly performance table
# ------------------------------------------------------------

st.subheader("📋 Monthly Shipping Performance")

trend_display = monthly_trend.copy()

trend_display["Average Lead Time"] = (
    trend_display["Avg_Lead_Time"]
    .map(lambda x: f"{x:.1f} days")
)

trend_display["Sales"] = (
    trend_display["Total_Sales"]
    .map(lambda x: f"${x:,.2f}")
)

trend_display["Profit"] = (
    trend_display["Total_Profit"]
    .map(lambda x: f"${x:,.2f}")
)

trend_display = trend_display[
    [
        "Order Month",
        "Orders",
        "Average Lead Time",
        "Sales",
        "Profit"
    ]
]

st.dataframe(
    trend_display,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# FINAL DASHBOARD FOOTER
# ============================================================

st.divider()

st.markdown("### 🍬 Nassau Candy Distributor")

st.caption(
    "Factory-to-Customer Shipping Route Efficiency Analysis"
)

st.markdown(
    "📦 Route Efficiency   •   🚚 Shipping Performance   •   "
    "🗺️ Geographic Analysis   •   🚦 Bottleneck Detection"
)

st.caption(
    "📊 Source: Nassau Candy Distributor shipping dataset"
)

st.caption("Data Analytics Project")

# ============================================================
# ABOUT THE DASHBOARD
# ============================================================

st.markdown("### 📘 About This Dashboard")

st.info(
    "This dashboard analyzes Nassau Candy Distributor's shipping "
    "performance to identify route efficiency, delivery patterns, "
    "geographic performance, shipping risks, and operational bottlenecks."
)