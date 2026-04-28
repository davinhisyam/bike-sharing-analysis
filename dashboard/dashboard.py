import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set style seaborn
sns.set(style='dark')

# Mendapatkan path direktori script
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "main_data.csv")

# Load data
df = pd.read_csv(file_path)
df['dteday'] = pd.to_datetime(df['dteday'])

# --- SIDEBAR (FITUR INTERAKTIF) ---
with st.sidebar:
    # Menambahkan logo (Gunakan gambar placeholder atau teks jika belum ada file logo)
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png") # Contoh logo dicoding
    
    # Mengambil rentang waktu untuk filter
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe berdasarkan input sidebar
main_df = df[(df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))]

# --- MAIN PAGE ---
st.header('Bike Sharing Dashboard 🚲')

# Pertanyaan 1 (SMART)
st.subheader('Perbedaan Rata-rata Penyewaan Berdasarkan Kondisi Cuaca')

weather_df = main_df.groupby('weathersit')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_df, palette='viridis', ax=ax)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

# Insight SMART untuk Pertanyaan 1
st.write(f"**Insight:** Selama periode yang dipilih, rata-rata penyewaan tertinggi terjadi pada cuaca Cerah. "
         f"Penurunan performa penyewaan sangat terasa ketika cuaca berubah menjadi buruk.")

# Pertanyaan 2
st.subheader('Tren Penyewaan Berdasarkan Musim')
season_df = main_df.groupby('season')['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=season_df, palette='coolwarm', ax=ax2)
st.pyplot(fig2)

st.caption('Copyright © Muhammad Davin Al Hisyam 2024')
