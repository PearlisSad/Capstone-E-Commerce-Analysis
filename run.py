import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Online Transactions Dashboard", layout="wide")
st.title("Online Transactions Dashboard")
st.markdown("Earliest Record is 2009-12-01 and Latest Record is 2011-12-09")

@st.cache_data
def load_sales():
    df = pd.read_csv("dataset/sales.csv")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

sales = load_sales()
#print(sales.head())

@st.cache_data
def load_returns():
    df = pd.read_csv("dataset/returns.csv")
    return df

returns = load_returns()

### Side bar START
st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Select Country",
    options=sorted(sales["Country"].unique()),
    default=["United Kingdom"]
)

min_date = sales["InvoiceDate"].min().date()
max_date = sales["InvoiceDate"].max().date()

start_date = st.sidebar.date_input(
    "From",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)
end_date = st.sidebar.date_input(
    "To",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

# Ensure proper ordering
if start_date > end_date:
    st.sidebar.warning("'From date' is after 'To date'. Adjust date to chronological order.")
    end_date = start_date

# Convert datetime.date to pd.Timestamp for comparison
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

filtered_sales = sales[sales["Country"].isin(country)]

filtered_sales = filtered_sales[
    (filtered_sales["InvoiceDate"] >= start_date) &
    (filtered_sales["InvoiceDate"] <= end_date)
]


filtered_sales["Revenue"] = (
    filtered_sales["Quantity"] * filtered_sales["Price"]
)

### Side bar END

###

total_revenue = filtered_sales["Revenue"].sum()
total_transactions = filtered_sales["Invoice"].nunique()
total_customers = filtered_sales["Customer ID"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"£{total_revenue:,.2f}")
col2.metric("Total Transactions", f"{total_transactions:,}")
col3.metric("Unique Customers", f"{total_customers:,}")

st.divider()

###

### Tabs Start
tab1, tab2, tab3, tab4, tab5 = st.tabs(["EDA","Revenue Analysis", "Customer Behaviour Analysis", "Purchase Analysis", "Findings"])

with tab1:
    st.subheader("Transactions by Country")

    country_txn = (
        filtered_sales
        .groupby("Country")["Invoice"]
        .nunique()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        country_txn,
        x="Country",
        y="Invoice",
        title="Number of Transactions by Country"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Revenue Over Time")

    revenue_time = (
        filtered_sales
        .groupby(filtered_sales["InvoiceDate"].dt.to_period("M"))["Revenue"]
        .sum()
        .reset_index()
    )

    revenue_time["InvoiceDate"] = revenue_time["InvoiceDate"].astype(str)

    fig = px.line(
        revenue_time,
        x="InvoiceDate",
        y="Revenue",
        title="Monthly Revenue Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    print("wahwah")
    

with tab4:
    st.subheader("Top Products by Revenue")

    product_rev = (
        filtered_sales
        .groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        product_rev,
        x="Revenue",
        y="Description",
        orientation="h",
        title="Top 10 Products by Revenue"
    )
    st.plotly_chart(fig, use_container_width=True)

### Tabs End

### Raw DataFrame Start
with st.expander("Show Sales data"):
    st.dataframe(sales, use_container_width=True)

with st.expander("Show Returns data"):
    st.dataframe(returns, use_container_width=True)

### Raw DataFrame End

