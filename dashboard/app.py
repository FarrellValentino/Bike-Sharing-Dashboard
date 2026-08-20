import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Setup page
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("main_data.csv")
    data['dteday'] = pd.to_datetime(data['dteday'])
    
    # Memastikan kolom time_category ada 
    if 'time_category' not in data.columns:
        def categorize_time(hour):
            if 5 <= hour < 12: return 'Pagi'
            elif 12 <= hour < 17: return 'Siang'
            elif 17 <= hour < 21: return 'Sore'
            else: return 'Malam'
        data['time_category'] = data['hour'].apply(categorize_time)
        
    return data

df = load_data()

# Sidebar
st.sidebar.title("🚲 Bike Sharing Analytics")

min_date = df["dteday"].min()
max_date = df["dteday"].max()

# Filter tanggal
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

main_df = df[(df["dteday"] >= str(start_date)) & 
             (df["dteday"] <= str(end_date))]

# Main Body
st.title("Bike Sharing Data Dashboard 🚲")
st.markdown("Dashboard interaktif ini menyajikan metrik operasional dan analisis faktor lingkungan terhadap tingkat penyewaan sepeda.")

# Total jumlah penyewaan sepeda
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df['total_count'].sum()
    st.metric("Total Penyewaan (Semua Pengguna)", value=f"{total_rentals:,}")
with col2:
    registered_rentals = main_df['registered'].sum()
    st.metric(" Jumlah Penyewaan (Registered) ", value=f"{registered_rentals:,}")
with col3:
    casual_rentals = main_df['casual'].sum()
    st.metric("Jumlah Penyewaan (Casual)", value=f"{casual_rentals:,}")

st.divider()


# Visualisasi dan penjelasan jawaban pertanyaan bisnis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Cuaca")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="weathersit", y="total_count", data=main_df, estimator=sum, errorbar=None, color="steelblue", ax=ax)
    ax.set_ylabel("Total Penyewaan")
    ax.set_xlabel("Kondisi Cuaca")
    plt.xticks(rotation=15)
    st.pyplot(fig)
    
    with st.expander("Penjelasan"):
        st.write(
            """
            Kalo kita perhatikan dari bar chart di atas, cuaca cerah (Clear) adalah golden time buat bisnis ini, 
            total sewaannya tembus paling tinggi. Tapi begitu cuaca mendung atau hujan/salju, angkanya langsung terjun bebas. 
            Untuk mem follow up hal ini , tim marketing bisa mengantisipasi kerugian di hari hujan dengan menembak push notification promo diskon cuaca buruk / Bad Weather Promo ke user.
            """
        )

with col2:
    st.subheader("Pola Rata-rata Sewa per Jam pada Hari Kerja")
    workingday_data = main_df[main_df['workingday'] == 1]
    hourly = workingday_data.groupby('hour')['total_count'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(x="hour", y="total_count", data=hourly, marker="o", color="coral", linewidth=2, ax=ax)
    ax.set_xticks(range(0, 24))
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xlabel("Jam Operasional")
    st.pyplot(fig)
    
    with st.expander("Penjelasan"):
        st.write(
            """
            Pada hari kerja, bisa dilihat ada dua puncak (peak hours) yang tajam, yaitu sekitar **jam 8 pagi** dan **jam 5 sore**. 
            Ini membuktikan bahwa mayoritas penyewa adalah komuter kantoran. 
            Untuk mem follow up hal ini , tim logistik wajib gerak cepat untuk rebalancing armada sepeda di stasiun-stasiun area perkantoran minimal setengah jam sebelum jam sibuk dimulai.
            """
        )

st.divider()


# Visualisasi dan penjelasan heatmap cuaca vs kategori waktu
st.subheader("Hubungan cuaca dengan kategori waktu terhadap rata-rata penyewaan sepeda")

# Memastikan urutan kolom waktu rapi
weather_time_clustering = main_df.groupby(['weathersit', 'time_category'])['total_count'].mean().unstack()
urutan_waktu = ['Pagi', 'Siang', 'Sore', 'Malam']
# Filter hanya kolom yang ada di data saat rentang waktu difilter
kolom_tersedia = [col for col in urutan_waktu if col in weather_time_clustering.columns]
weather_time_clustering = weather_time_clustering[kolom_tersedia]

fig_heat, ax_heat = plt.subplots(figsize=(12, 5))
sns.heatmap(weather_time_clustering, annot=True, fmt=".0f", cmap="YlOrRd", linewidths=.5, ax=ax_heat)
ax_heat.set_xlabel("Kategori Waktu")
ax_heat.set_ylabel("Kondisi Cuaca")
st.pyplot(fig_heat)

with st.expander("Penjelasan"):
    st.write(
        """
        Melalui metrik Heatmap berbasis Binning waktu ini, kita bisa melihat pain points bisnis secara lebih presisi. 
        Saat cuaca buruk memuncak ("Light/Heavy Rain/Snow"), minat sewa di waktu "Pagi" dan "Malam" menjadi titik paling rentan (sangat rendah).
        Sebaliknya, cuaca "Clear" di kategori waktu "Sore" menjadi sweet spot dengan rata-rata penyewaan tertinggi mencapai lebih dari 380 unit per jam. 
        Untuk itu , heatmap ini sangat krusial bagi manajemen untuk merancang strategi dynamic pricing berdasarkan cuaca secara real time.
        """
    )

st.divider()
st.caption("Copyright (c) Farrell Valentino Wempie")