import streamlit as st
import pandas as pd
import snowflake.connector

# Connection
conn = snowflake.connector.connect(
    user=st.secrets["SNOWFLAKE_USER"],
    password=st.secrets["SNOWFLAKE_PASSWORD"],
    account=st.secrets["SNOWFLAKE_ACCOUNT"],
    warehouse="RETAIL_WH",
    database="RETAIL_DB",
    schema="RETAIL_SCHEMA"
)

def run_query(query):
    return pd.read_sql(query, conn)

st.set_page_config(layout="wide")

st.title("🛒 SmartMart Retail Analytics Dashboard")

# Load Data
region_df = run_query("SELECT * FROM REGION_REVENUE")
monthly_df = run_query("SELECT * FROM MONTHLY_SALES")
category_df = run_query("SELECT * FROM CATEGORY_REVENUE")
products_df = run_query("SELECT * FROM TOP_10_PRODUCTS")
channel_df = run_query("SELECT * FROM CHANNEL_PERFORMANCE")

# Sidebar Filters
st.sidebar.header("🔍 Filters")

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(region_df["REGION"].unique())
)

selected_channel = st.sidebar.selectbox(
    "Sales Channel",
    ["All"] + list(channel_df["SALES_CHANNEL"].unique())
)

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + list(category_df["CATEGORY"].unique())
)

# Apply Filters
if selected_region != "All":
    region_df = region_df[region_df["REGION"] == selected_region]

if selected_channel != "All":
    channel_df = channel_df[channel_df["SALES_CHANNEL"] == selected_channel]

if selected_category != "All":
    category_df = category_df[category_df["CATEGORY"] == selected_category]

# KPI
total_revenue = region_df["TOTAL_REVENUE"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Products", len(products_df))
col3.metric("🛍 Channels", channel_df["SALES_CHANNEL"].nunique())

st.divider()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Region")
    st.bar_chart(region_df.set_index("REGION")["TOTAL_REVENUE"])

with col2:
    st.subheader("Online vs Offline Sales")
    st.bar_chart(channel_df.set_index("SALES_CHANNEL")["TOTAL_REVENUE"])

st.subheader("Monthly Sales Trend")
st.line_chart(monthly_df.set_index("SALES_MONTH")["MONTHLY_REVENUE"])

col3, col4 = st.columns(2)

with col3:
    st.subheader("Category Revenue")
    st.bar_chart(category_df.set_index("CATEGORY")["TOTAL_REVENUE"])

with col4:
    st.subheader("Top 10 Products")
    st.bar_chart(products_df.set_index("PRODUCT_NAME")["TOTAL_REVENUE"])
