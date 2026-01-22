import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="Online Transactions Dashboard", layout="wide")
st.title("Online Transactions Dashboard")

@st.cache_data
def load_sales():
    df = pd.read_csv("dataset/sales.csv")
    return df

sales = load_sales()

@st.cache_data
def load_returns():
    df = pd.read_csv("dataset/returns.csv")
    return df

returns = load_returns

### Side bar START
st.sidebar.header("Filters")

### Side bar END

### Tabs Start
tab1, tab2, tab3, tab4, tab5 = st.tabs(["EDA","Revenue Analysis", "Customer Behaviour Analysis", "Purchase Analysis", "Findings"])


### Tabs End

### Raw DataFrame Start
with st.expander("Show Sales data"):
    st.dataframe(sales, use_container_width=True)

with st.expander("Show Returns data"):
    st.dataframe(sales, use_container_width=True)

### Raw DataFrame End

