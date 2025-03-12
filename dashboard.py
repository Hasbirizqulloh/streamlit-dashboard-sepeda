import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
df = pd.read_csv("all_data.csv")
day_df = pd.read_csv("day.csv")

# Ubah label musim dan cuaca ke dalam bahasa Indonesia
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
weather_mapping = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat"}

df["season"] = df["season"].map(season_mapping)
df["weathersit"] = df["weathersit"].map(weather_mapping)

# Sidebar Filters
st.sidebar.header("Filter Data Jumlah Penyewaan Sepeda")
season_options = ["ALL"] + list(df["season"].unique())
weather_options = ["ALL"] + list(df["weathersit"].unique())
selected_season = st.sidebar.selectbox("Pilih Musim:", season_options)
selected_weather = st.sidebar.selectbox("Pilih Kondisi Cuaca:", weather_options)

# Filter dataset
filtered_df = df.copy()
if selected_season != "ALL":
    filtered_df = filtered_df[filtered_df["season"] == selected_season]
if selected_weather != "ALL":
    filtered_df = filtered_df[filtered_df["weathersit"] == selected_weather]

# Display statistics
st.title("Dashboard Penyewaan Sepeda")
if selected_season == "ALL" and selected_weather == "ALL":
    st.write("### Statistik Penyewaan untuk Semua Musim dan Kondisi Cuaca")
elif selected_season == "ALL":
    st.write(f"### Statistik Penyewaan untuk Semua Musim dengan Cuaca {selected_weather}")
elif selected_weather == "ALL":
    st.write(f"### Statistik Penyewaan pada {selected_season} untuk Semua Kondisi Cuaca")
else:
    st.write(f"### Statistik Penyewaan pada {selected_season} dengan Cuaca {selected_weather}")

# Membuat dua kolom untuk statistik
col1, col2 = st.columns(2)

# Menampilkan metrik di dalam kolom
with col1:
    st.metric("Total Penyewaan", filtered_df["cnt"].sum())

with col2:
    st.metric("Rata-rata Penyewaan", round(filtered_df["cnt"].mean(), 2))

# Agregasi data berdasarkan kondisi cuaca
weathersit_df = day_df.groupby("weathersit").agg({"cnt": "mean"}).reset_index()
weathersit_df["weathersit"] = weathersit_df["weathersit"].map(weather_mapping)

# Menentukan warna: Merah untuk kondisi cuaca dengan penyewaan tertinggi
max_index = weathersit_df["cnt"].idxmax()
colors = ['gray' if i != max_index else 'red' for i in weathersit_df.index]

# Sidebar tambahan untuk interaktivitas grafik cuaca
st.sidebar.header("Pengaturan Visualisasi Cuaca")
chart_type = st.sidebar.radio("Pilih Jenis Grafik Cuaca:", ["Bar Chart", "Line Chart"])
show_values = st.sidebar.checkbox("Tampilkan Nilai di Atas Batang", value=True)

# Plot interaktif pengaruh cuaca
st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")

fig, ax = plt.subplots(figsize=(10, 5))
if chart_type == "Bar Chart":
    plot = sns.barplot(data=weathersit_df, x="weathersit", y="cnt", ax=ax, palette=colors)
    if show_values:
        for p in plot.patches:
            ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')
else:
    sns.lineplot(data=weathersit_df, x="weathersit", y="cnt", marker="o", ax=ax, color="blue")

ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")

st.pyplot(fig)

# Sidebar tambahan untuk interaktivitas penyewaan per jam
st.sidebar.header("Pengaturan Visualisasi Per Jam")
selected_hours = st.sidebar.slider("Pilih Rentang Jam:", 0, 23, (0, 23))

# Visualisasi penyewaan per jam
st.subheader("Tren Penyewaan Sepeda per Jam di Musim Panas dan Musim Dingin")

summer_df = df[df["season"] == "Musim Panas"].groupby("hr")["cnt"].mean().reset_index()
winter_df = df[df["season"] == "Musim Dingin"].groupby("hr")["cnt"].mean().reset_index()

# Filter berdasarkan rentang jam yang dipilih
summer_df = summer_df[(summer_df["hr"] >= selected_hours[0]) & (summer_df["hr"] <= selected_hours[1])]
winter_df = winter_df[(winter_df["hr"] >= selected_hours[0]) & (winter_df["hr"] <= selected_hours[1])]

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=summer_df, x="hr", y="cnt", ax=ax, color="orange", label="Musim Panas")
sns.lineplot(data=winter_df, x="hr", y="cnt", ax=ax, color="blue", label="Musim Dingin")

ax.set_xlabel("Waktu/Jam dalam sehari")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Tren Penyewaan Sepeda per Jam di Musim Panas dan Musim Dingin")
ax.legend()
ax.set_xticks(range(selected_hours[0], selected_hours[1] + 1, max(1, (selected_hours[1] - selected_hours[0]) // 6)))

st.pyplot(fig)
