import streamlit as st
import pandas as pd
import snowflake.connector

# Snowflake connection
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

st.title("🛒 SmartMart Retail Analytics Dashboard")

# Load data
region_df = run_query("SELECT * FROM REGION_REVENUE")
monthly_df = run_query("SELECT * FROM MONTHLY_SALES")
category_df = run_query("SELECT * FROM CATEGORY_REVENUE")
products_df = run_query("SELECT * FROM TOP_10_PRODUCTS")
channel_df = run_query("SELECT * FROM CHANNEL_PERFORMANCE")

st.subheader("Sales by Region")
st.bar_chart(region_df.set_index("REGION")["TOTAL_REVENUE"])

st.subheader("Monthly Sales Trend")
st.line_chart(monthly_df.set_index("SALES_MONTH")["MONTHLY_REVENUE"])

st.subheader("Category Revenue")
st.bar_chart(category_df.set_index("CATEGORY")["TOTAL_REVENUE"])

st.subheader("Top 10 Products")
st.bar_chart(products_df.set_index("PRODUCT_NAME")["TOTAL_REVENUE"])

st.subheader("Online vs Offline Sales")
st.bar_chart(channel_df.set_index("SALES_CHANNEL")["TOTAL_REVENUE"])
