import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load data
data = pd.read_csv("main_data.csv")

st.title("Bike Sharing Dashboard")
st.markdown("Visualisasi data peminjaman sepeda dari Capital Bikeshare (2011-2012).")

# Sidebar filter
year_map = {0: 2011, 1: 2012}
data['year'] = data['yr'].map(year_map)
year = st.sidebar.selectbox("Pilih Tahun", options=data['year'].unique())
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
data['season_name'] = data['season'].map(season_map)
selected_seasons = st.sidebar.multiselect("Pilih Musim", options=season_map.values(), default=list(season_map.values()))

# Filter data
filtered_data = data[(data['year'] == year) & (data['season_name'].isin(selected_seasons))]

# Visualisasi 1: Rata-rata peminjaman per musim (bar chart)
st.subheader("Rata-rata Peminjaman Sepeda per Musim")
avg_by_season = filtered_data.groupby('season_name')['cnt'].mean().reset_index()
fig1, ax1 = plt.subplots()
sns.barplot(data=avg_by_season, x='season_name', y='cnt', palette='viridis', ax=ax1)
ax1.set_ylabel("Rata-rata Jumlah Peminjaman")
st.pyplot(fig1)

# Visualisasi 2: Tren peminjaman sepanjang tahun (line chart)
st.subheader("Tren Peminjaman Sepanjang Tahun")
monthly_trend = filtered_data.groupby('mnth')['cnt'].mean()
fig2, ax2 = plt.subplots()
monthly_trend.plot(kind='line', marker='o', ax=ax2)
ax2.set_xlabel("Bulan")
ax2.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig2)

# Visualisasi 3: Distribusi peminjaman berdasarkan hari kerja vs libur (boxplot)
st.subheader("Peminjaman: Hari Kerja vs Hari Libur")
fig3, ax3 = plt.subplots()
sns.boxplot(data=filtered_data, x='workingday', y='cnt', ax=ax3)
ax3.set_xticklabels(['Libur', 'Hari Kerja'])
st.pyplot(fig3)

# Visualisasi 4: Pengaruh cuaca terhadap jumlah peminjaman (boxplot)
st.subheader("Pengaruh Cuaca terhadap Jumlah Peminjaman")
fig4, ax4 = plt.subplots()
sns.boxplot(data=filtered_data, x='weathersit', y='cnt', ax=ax4)
ax4.set_xticklabels(['Cerah', 'Berawan/Mist', 'Hujan Ringan', 'Ekstrem'])
st.pyplot(fig4)

# Visualisasi 5: Korelasi suhu dan jumlah peminjaman (scatter plot)
st.subheader("Hubungan Suhu dan Jumlah Peminjaman")
fig5, ax5 = plt.subplots()
sns.scatterplot(data=filtered_data, x='temp', y='cnt', hue='season_name', palette='deep', ax=ax5)
ax5.set_xlabel("Suhu (Ternormalisasi)")
ax5.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig5)
