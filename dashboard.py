import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
df = pd.read_csv("all_data.csv")

# Ubah label musim dan cuaca ke dalam bahasa Indonesia
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
weather_mapping = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat"}

df["season"] = df["season"].map(season_mapping)
df["weathersit"] = df["weathersit"].map(weather_mapping)

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox("Pilih Musim:", df["season"].unique())
selected_weather = st.sidebar.selectbox("Pilih Kondisi Cuaca:", df["weathersit"].unique())

# Filter dataset
filtered_df = df[(df["season"] == selected_season) & (df["weathersit"] == selected_weather)]

# Display statistics
st.title("Dashboard Penyewaan Sepeda")
st.write(f"### Statistik Penyewaan pada {selected_season} dengan Cuaca {selected_weather}")

# Membuat dua kolom untuk statistik
col1, col2 = st.columns(2)

# Menampilkan metrik di dalam kolom
with col1:
    st.metric("Total Penyewaan", filtered_df["cnt"].sum())

with col2:
    st.metric("Rata-rata Penyewaan", round(filtered_df["cnt"].mean(), 2))

# Menentukan batas maksimum y berdasarkan hasil filter
max_rentals = filtered_df[['casual', 'registered', 'cnt']].sum().max()
if pd.isna(max_rentals):  
    max_rentals = 0
else:
    max_rentals = int(max_rentals * 1.1)  

# Bar plot penyewaan sepeda
st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")

weather_avg_df = df.groupby("weathersit")["cnt"].mean().reset_index()
colors = ["red" if w == "Cerah" else "gray" for w in weather_avg_df["weathersit"]]

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=weather_avg_df["weathersit"], y=weather_avg_df["cnt"], palette=colors, ax=ax)
ax.set_title("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")

st.pyplot(fig)

# Visualisasi penyewaan per jam
st.subheader(f"Tren Penyewaan Sepeda per Jam pada {selected_season} dengan Cuaca {selected_weather}")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_df, x="hr", y="cnt", ax=ax, marker='o')
ax.set_xticks([0, 6, 12, 18, 23])
ax.set_xticklabels(["00:00", "06:00", "12:00", "18:00", "23:00"])
ax.set_xlabel("Waktu (Jam)")
ax.set_ylabel("Jumlah Penyewaan")
ax.axvspan(7, 9, color='red', alpha=0.2, label="Jam Sibuk Pagi")
ax.axvspan(17, 19, color='blue', alpha=0.2, label="Jam Sibuk Sore")
ax.legend()

st.pyplot(fig)

peak_hour = filtered_df.loc[filtered_df["cnt"].idxmax(), "hr"]
peak_count = filtered_df["cnt"].max()

st.write(f"📌 Penyewaan sepeda tertinggi terjadi pada pukul {peak_hour}:00 dengan total {peak_count} penyewaan.")

st.write("*Gunakan filter di sidebar untuk melihat data spesifik berdasarkan musim dan cuaca.*")
