# Import library yang diperlukan
import pandas as pd  # Digunakan untuk manipulasi data menggunakan DataFrame
import matplotlib.pyplot as plt  # Digunakan untuk visualisasi data dengan plot
import seaborn as sns  # Digunakan untuk plot yang lebih interaktif dan informatif
import streamlit as st  # Digunakan untuk membuat aplikasi web interaktif dengan Python
from babel.numbers import format_currency  # Digunakan untuk memformat nilai mata uang
# Mengatur gaya plot menggunakan tema 'dark' dari seaborn
sns.set(style='dark')
# Mengatur opsi untuk Streamlit agar tidak menampilkan peringatan yang tidak perlu
st.set_option('deprecation.showPyplotGlobalUse', False)


class AnalysisData:
    def __init__(self, df):
        """
        Inisialisasi objek Analisis Data.

        Parameters:
        - df (pandas.DataFrame): DataFrame yang akan dianalisis.
        """
        self.df = df

    def create_daily_orders_df(self):
        """
        Membuat DataFrame harian untuk jumlah pesanan dan pendapatan.

        Returns:
        - pandas.DataFrame: DataFrame harian dengan kolom 'order_count' dan 'revenue'.
        """
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
        """
        Membuat DataFrame untuk jumlah item produk yang terjual.

        Returns:
        - pandas.DataFrame: DataFrame dengan kolom 'product_category_name_english' dan 'product_count'.
        """
        sum_order_items_df = self.df.groupby("product_category_name_english")["product_id"].count().reset_index()
        sum_order_items_df.rename(columns={
            "product_id": "product_count"
        }, inplace=True)
        sum_order_items_df = sum_order_items_df.sort_values(by='product_count', ascending=False)

        return sum_order_items_df

    def review_score_df(self):
        """
        Membuat DataFrame untuk skor ulasan dan skor ulasan yang paling umum.

        Returns:
        - pandas.Series: Jumlah skor ulasan yang diurutkan.
        - int: Skor ulasan yang paling umum.
        """
        review_scores = self.df['review_score'].value_counts().sort_values(ascending=False)
        most_common_score = review_scores.idxmax()

        return review_scores, most_common_score


# Mengimpor library yang diperlukan
import pandas as pd  # Digunakan untuk manipulasi data menggunakan DataFrame
# Mengatur kolom-kolom datetime pada dataset
datetime_cols = ['order_approved_at', 'order_delivered_carrier_date', 
                'order_delivered_customer_date', 'order_estimated_delivery_date', 
                'order_purchase_timestamp', 'shipping_limit_date']
# Membaca dataset dari file CSV
all_df = pd.read_csv("C:\\project\\data-analis-ecommerce\\all_data.csv")
# Mengurutkan DataFrame berdasarkan kolom 'order_approved_at'
all_df.sort_values(by='order_approved_at', inplace=True)
all_df.reset_index(inplace=True)
# Mengonversi kolom-kolom datetime menjadi tipe data datetime
for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])
# Menentukan tanggal minimum dan maksimum dalam DataFrame
min_date = all_df['order_approved_at'].min()
max_date = all_df['order_approved_at'].max()



# Sidebar
with st.sidebar:
    # Title
    st.title("Proyek Analisis Data E-Commerce")
    # Date Range
    start_date, end_date = st.date_input(
        label="Pilih Periode:",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]
# Membuat objek AnalysisData dengan menggunakan DataFrame yang telah difilter
function = AnalysisData(main_df)
# Menggunakan metode-metode dari AnalysisData untuk mendapatkan DataFrames yang diperlukan
daily_orders_df = function.create_daily_orders_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()

# Title
st.header("Dashboard Analisis Data E-Commerce")


# Order Barang
st.subheader("Barang yang Paling Banyak Terjual")

fig, ax = plt.subplots(
    nrows=1, 
    ncols=2, 
    figsize=(24, 12))  

colors = ["#4285F4", "#34A853", "#FBBC05", "#EA4335", "#1F5DC1"]  

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
    fontsize=18)  
ax[0].tick_params(
    axis ='y', 
    labelsize=15)
ax[0].tick_params(
    axis ='x', 
    labelsize=12)

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
    fontsize=18)  
ax[1].tick_params(
    axis='y', 
    labelsize=15)
ax[1].tick_params(
    axis='x', 
    labelsize=12)

st.pyplot(fig)



# Order Harian
st.subheader("Order Harian Konsumen")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#4285F4"  
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
            palette=["#4285F4" if score == common_score else "#D1CFE2" for score in review_score.index] 
            )

plt.title("Rating dari Konsumen untuk Pelayanan", fontsize=20)
plt.xlabel(None)
plt.ylabel(None)
plt.xticks(fontsize=12)
st.pyplot(fig)


