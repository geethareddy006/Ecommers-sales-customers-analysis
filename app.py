import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv(
    "data/cleaned_online_retail.csv.gz",
    parse_dates=["InvoiceDate"]
)


st.sidebar.header("🔎 Filters")

countries = sorted(df["Country"].dropna().unique())

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All Countries"] + countries
)

if selected_country != "All Countries":
    df = df[df["Country"] == selected_country]


months = sorted(df["Month_Year"].dropna().unique())

selected_month = st.sidebar.selectbox(
    "Select Month",
    ["All Months"] + months
)

if selected_month != "All Months":
    df = df[df["Month_Year"] == selected_month]


customers = sorted(df["CustomerID"].dropna().unique())

selected_customer = st.sidebar.selectbox(
    "Select Customer",
    ["All Customers"] + [str(int(c)) for c in customers]
)

if selected_customer != "All Customers":
    df = df[df["CustomerID"] == float(selected_customer)]

st.sidebar.subheader("📥 Download Data")

csv_data = df.to_csv(index=False)

st.sidebar.download_button(
    label="Download Filtered Data",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

  
st.title("📊 E-Commerce Sales & Customer Behavior Dashboard")

st.markdown(
    "Interactive analysis of sales performance, products, "
    "customers, orders, and geographic trends."
)

# KPI Calculations

total_revenue = df["Revenue"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
total_products = df["StockCode"].nunique()
average_order_value = total_revenue / total_orders

# KPI Cards

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Total Revenue", f"£{total_revenue:,.0f}")
col2.metric("🛒 Total Orders", f"{total_orders:,}")
col3.metric("👥 Total Customers", f"{total_customers:,}")
col4.metric("📦 Total Products", f"{total_products:,}")
col5.metric("📈 Avg Order Value", f"£{average_order_value:,.2f}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Revenue Trend")

    monthly_revenue = (
        df.groupby("Month_Year")["Revenue"]
        .sum()
    )

    st.line_chart(monthly_revenue)


with col2:
    st.subheader("👥 Top 10 Customers by Revenue")

    top_customers = (
        df.groupby("CustomerID")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    st.bar_chart(top_customers)


col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Products by Revenue")

    top_products = (
        df.groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    st.bar_chart(top_products)


with col2:
    st.subheader("🌍 Top 10 Countries by Revenue")

    top_countries = (
        df.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    st.bar_chart(top_countries)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Revenue by Year")

    yearly_revenue = (
        df.groupby("Year")["Revenue"]
        .sum()
    )

    st.bar_chart(yearly_revenue)


with col2:
    st.subheader("📅 Revenue by Month")

    monthly_revenue = (
        df.groupby("Month")["Revenue"]
        .sum()
    )

    st.bar_chart(monthly_revenue)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🛒 Monthly Order Volume")

    monthly_orders = (
        df.groupby("Month_Year")["InvoiceNo"]
        .nunique()
    )

    st.bar_chart(monthly_orders)


with col2:
    st.subheader("👥 Monthly Active Customers")

    monthly_active_customers = (
        df.groupby("Month_Year")["CustomerID"]
        .nunique()
    )

    st.line_chart(monthly_active_customers)
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Customer Purchase Frequency")

    customer_orders = (
        df.groupby("CustomerID")["InvoiceNo"]
        .nunique()
    )

    st.bar_chart(
        customer_orders.value_counts().sort_index()
    )


with col2:
    st.subheader("📊 Customer Revenue vs Purchase Frequency")

    customer_analysis = (
        df.groupby("CustomerID")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("InvoiceNo", "nunique")
        )
    )

    st.scatter_chart(
        customer_analysis,
        x="Orders",
        y="Revenue"
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔄 Repeat Customer Rate")

    customer_orders = (
        df.groupby("CustomerID")["InvoiceNo"]
        .nunique()
    )

    repeat_customers = (customer_orders > 1).sum()
    total_customers = customer_orders.count()

    repeat_customer_rate = (
        repeat_customers / total_customers
    ) * 100

    st.metric(
        "Repeat Customer Rate",
        f"{repeat_customer_rate:.2f}%"
    )


with col2:
    st.subheader("💰 Average Revenue per Customer")

    average_revenue_per_customer = (
        df["Revenue"].sum() / df["CustomerID"].nunique()
    )

    st.metric(
        "Average Revenue per Customer",
        f"£{average_revenue_per_customer:,.2f}"
    )


col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Top 10 Products by Quantity Sold")

    top_quantity_products = (
        df.groupby("Description")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    st.bar_chart(top_quantity_products)


with col2:
    st.subheader("📊 Product Revenue vs Quantity Sold")

    product_analysis = (
        df.groupby("Description")
        .agg(
            Revenue=("Revenue", "sum"),
            Quantity=("Quantity", "sum")
        )
    )

    st.scatter_chart(
        product_analysis,
        x="Quantity",
        y="Revenue"
    )
st.subheader("📅 Revenue by Day of Week")

df["Day_Name"] = df["InvoiceDate"].dt.day_name()

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

daily_revenue = (
    df.groupby("Day_Name")["Revenue"]
    .sum()
    .reindex(day_order)
)

st.bar_chart(daily_revenue)
st.subheader("🛒 Orders by Day of Week")

daily_orders = (
    df.groupby("Day_Name")["InvoiceNo"]
    .nunique()
    .reindex(day_order)
)

st.bar_chart(daily_orders)

st.subheader("🛒 Average Orders per Customer")

average_orders_per_customer = (
    df.groupby("CustomerID")["InvoiceNo"]
    .nunique()
    .mean()
)

st.metric(
    "Average Orders per Customer",
    f"{average_orders_per_customer:.2f}"
)
st.subheader("💰 Customer Revenue Distribution")

customer_revenue = (
    df.groupby("CustomerID")["Revenue"]
    .sum()
)

st.bar_chart(
    customer_revenue.sort_values(ascending=False).head(20)
)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Customers by Country")

    country_customers = (
        df.groupby("Country")["CustomerID"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    st.bar_chart(country_customers)


with col2:
    st.subheader("🌍 Average Order Value by Country")

    country_aov = (
        df.groupby("Country")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("InvoiceNo", "nunique")
        )
    )

    country_aov["AOV"] = (
        country_aov["Revenue"] / country_aov["Orders"]
    )

    country_aov = (
        country_aov["AOV"]
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    st.bar_chart(country_aov)
st.subheader("📌 Key Business Insights")

st.markdown("""
- 💰 The dashboard tracks overall revenue, orders, customers, and products.
- 📈 Monthly revenue trends help identify high and low performing periods.
- 🏆 Top products reveal the products generating the highest revenue.
- 🌍 Country analysis shows the major markets contributing to sales.
- 👥 Customer analysis helps identify high-value and repeat customers.
- 🛒 Order-frequency analysis shows customer purchasing behavior.
- 📦 Quantity analysis identifies products with high sales volume.
""")

st.markdown("---")

st.caption(
    "E-Commerce Sales & Customer Behavior Analysis | "
    "Built with Python, Pandas, and Streamlit"
)