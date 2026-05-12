import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Enterprise BI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# DARK ENTERPRISE STYLE
# ----------------------------
st.markdown("""
<style>

.main {
    background-color: #0B0F19;
}

/* KPI CARDS */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #111827, #1f2937);
    border-radius: 14px;
    padding: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

/* SIDEBAR */
.css-1d391kg {
    background-color: #0f172a;
}

/* HEADINGS */
h1, h2, h3 {
    color: #f8fafc;
    font-weight: 600;
}

/* CHART CONTAINERS */
.stPlotlyChart {
    background: #0f172a;
    padding: 10px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    .main {
        background-color: #0B0F19;
        color: #FFFFFF;
    }

    h1, h2, h3 {
        color: #FFFFFF;
    }

    .stMetric {
        background-color: #111827;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# TITLE
# ----------------------------
st.title("📊 Enterprise Superstore Analytics Dashboard")

# ----------------------------
# LOAD DATA (CACHE FOR SPEED)
# ----------------------------
# @st.cache_data
# def load_data():
#     df = pd.read_csv("superstore.csv")
#     df.columns = df.columns.str.strip()
#     return df

# df = load_data()
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(__file__)
    csv_path = os.path.join(BASE_DIR, "superstore.csv")

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    return df

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("🎛 Filters")

region = st.sidebar.multiselect("Region", df["Region"].unique(), df["Region"].unique())
category = st.sidebar.multiselect("Category", df["Category"].unique(), df["Category"].unique())
sub_category = st.sidebar.multiselect("Sub Category", df["Sub.Category"].unique(), df["Sub.Category"].unique())

# ----------------------------
# FILTER DATA
# ----------------------------
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub.Category"].isin(sub_category))
]

# ----------------------------
# KPI CALCULATIONS
# ----------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
orders = len(filtered_df)
avg_profit = filtered_df["Profit"].mean()

# ----------------------------
# KPI CARDS (ENTERPRISE STYLE)
# ----------------------------
# col1, col2, col3, col4 = st.columns(4)
col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.2, 1.2], gap="large")

col1.metric("💰 Sales", f"${total_sales:,.0f}")
col2.metric("📈 Profit", f"${total_profit:,.0f}")
col3.metric("🧾 Orders", f"{orders}")
col4.metric("📊 Avg Profit", f"${avg_profit:,.2f}")

st.markdown("---")

# ----------------------------
# SALES BY CATEGORY
# ----------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("📦 Sales by Category")
    cat_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig1 = px.bar(cat_sales, x="Category", y="Sales", color="Category")
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    st.subheader("🌍 Profit by Region")
    region_profit = filtered_df.groupby("Region")["Profit"].sum().reset_index()
    fig2 = px.pie(region_profit, values="Profit", names="Region")
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# TOP CUSTOMERS
# ----------------------------
st.subheader("🏆 Top Customers (Enterprise Ranking)")

top_customers = (
    filtered_df.groupby("Customer.Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_customers,
    x="Customer.Name",
    y="Sales",
    color="Sales",
    text_auto=True
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# RAW DATA
# ----------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)
