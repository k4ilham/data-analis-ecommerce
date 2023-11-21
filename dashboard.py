import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Function
class AnalysisData:
    def __init__(self, df):
        self.df = df

    def create_daily_orders_df(self):
        daily_orders_df = self.df.resample(rule='D', on='order_approved_at').agg({
            "order_id": "nunique",
            "payment_value": "sum"
        })
        daily_orders_df = daily_orders_df.reset_index()
        daily_orders_df.rename(columns={
            "order_id": "order_count",
            "payment_value": "revenue"
        }, inplace=True)
        
        return daily_orders_df

    def create_sum_order_items_df(self):
        sum_order_items_df = self.df.groupby("product_category_name_english")["product_id"].count().reset_index()
        sum_order_items_df.rename(columns={
            "product_id": "product_count"
        }, inplace=True)
        sum_order_items_df = sum_order_items_df.sort_values(by='product_count', ascending=False)

        return sum_order_items_df

    def review_score_df(self):
        review_scores = self.df['review_score'].value_counts().sort_values(ascending=False)
        most_common_score = review_scores.idxmax()

        return review_scores, most_common_score


# Dataset
datetime_cols = ['order_approved_at', 'order_delivered_carrier_date', 
                'order_delivered_customer_date', 'order_estimated_delivery_date', 
                'order_purchase_timestamp', 'shipping_limit_date']
all_df = pd.read_csv("E:\Project\Dicoding\E-Commerce Public Dataset\All_data.csv")
all_df.sort_values(by='order_approved_at', inplace=True)
all_df.reset_index(inplace=True)

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df['order_approved_at'].min()
max_date = all_df['order_approved_at'].max()

# Sidebar
with st.sidebar:
    # Title
    st.title("Randy Ansari Nur Hidayat")

    # Logo Image
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")


    # Date Range
    start_date, end_date = st.date_input(
        label="Pilih Rentang Tanggal:",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )


# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

function = AnalysisData(main_df)

daily_orders_df = function.create_daily_orders_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()

# Title
st.header("Dashboard E-Commerce")

# Order Barang
st.subheader("Barang yang Paling Banyak Terjual")

fig, ax = plt.subplots(
    nrows=1, 
    ncols=2, 
    figsize=(45, 25))

colors = ["#D4AFB9", "#D1CFE2", "#D1CFE2", "#D1CFE2", "#D1CFE2"]

sns.barplot(
    x="product_count", 
    y="product_category_name_english", 
    data=sum_order_items_df.head(5), 
    palette=colors, 
    ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_title(
    "Produk paling banyak terjual", 
    loc="center", 
    fontsize=60)
ax[0].tick_params(
    axis ='y', 
    labelsize=40)
ax[0].tick_params(
    axis ='x', 
    labelsize=35)

sns.barplot(
    x="product_count", 
    y="product_category_name_english", 
    data=sum_order_items_df.sort_values(
        by="product_count", 
        ascending=True).head(5), 
        palette=colors, 
        ax=ax[1])
ax[1].set_ylabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title(
    "Produk paling sedikit terjual", 
    loc="center", 
    fontsize=60)
ax[1].tick_params(
    axis='y', 
    labelsize=40)
ax[1].tick_params(
    axis='x', 
    labelsize=35)

st.pyplot(fig)


# Order Harian
st.subheader("Order Harian Konsumen")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#D4AFB9"
)
ax.tick_params(
    axis="x", 
    rotation=55,
    labelsize=10)
ax.tick_params(
    axis="y", 
    labelsize=10)
st.pyplot(fig)

# Review Score
st.subheader("Rating Konsumen")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=review_score.index, 
            y=review_score.values, 
            order=review_score.index,
            palette=["#D4AFB9" if score == common_score else "#D1CFE2" for score in review_score.index]
            )

plt.title("Rating dari Konsumen untuk Pelayanan", fontsize=20)
plt.xlabel(None)
plt.ylabel(None)
plt.xticks(fontsize=12)
st.pyplot(fig)

st.caption('Copyright (C) Randy Ansari Nur Hidayat 2023')