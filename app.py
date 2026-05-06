import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Urban Books Dashboard", layout="wide")

st.title("📊 Urban Books Center Dashboard")
st.markdown("Interactive dashboard for monitoring book sales and performance")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sales_data.csv")
    except:
        # Sample data (if no file is uploaded)
        data = {
            "Date": pd.date_range(start="2025-01-01", periods=10),
            "Institution": ["KMTC", "University", "College", "KMTC", "College", "University", "KMTC", "College", "University", "KMTC"],
            "Region": ["Nairobi", "Rift Valley", "Western", "Nairobi", "Coast", "Central", "Western", "Coast", "Central", "Nairobi"],
            "Revenue": [120000, 95000, 70000, 150000, 80000, 110000, 130000, 75000, 90000, 160000]
        }
        df = pd.DataFrame(data)
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

region = st.sidebar.selectbox("Select Region", ["All"] + list(df["Region"].unique()))
institution = st.sidebar.selectbox("Select Institution", ["All"] + list(df["Institution"].unique()))

# Filter data
filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region]

if institution != "All":
    filtered_df = filtered_df[filtered_df["Institution"] == institution]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue (KES)", f"{filtered_df['Revenue'].sum():,}")
col2.metric("Total Transactions", len(filtered_df))
col3.metric("Average Revenue", f"{filtered_df['Revenue'].mean():,.0f}")

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📋 Data Overview")
st.dataframe(filtered_df)

# -----------------------------
# REVENUE TREND
# -----------------------------
st.subheader("📈 Revenue Trend")

fig, ax = plt.subplots()
ax.plot(filtered_df["Date"], filtered_df["Revenue"])
ax.set_xlabel("Date")
ax.set_ylabel("Revenue")
ax.set_title("Revenue Over Time")

st.pyplot(fig)

# -----------------------------
# REVENUE BY REGION
# -----------------------------
st.subheader("🌍 Revenue by Region")

region_data = filtered_df.groupby("Region")["Revenue"].sum()

fig2, ax2 = plt.subplots()
region_data.plot(kind="bar", ax=ax2)
ax2.set_title("Revenue by Region")
ax2.set_ylabel("Revenue")

st.pyplot(fig2)

# -----------------------------
# DOWNLOAD OPTION
# -----------------------------
st.subheader("⬇️ Download Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered data",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Urban Books Center Ltd | Dashboard v1.0")
