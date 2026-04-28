import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set style
sns.set(style='dark')

# --- LOAD DATA ---
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "main_data.csv")
df = pd.read_csv(file_path)
df['dteday'] = pd.to_datetime(df['dteday'])

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Menyiapkan rentang waktu
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    
    # Perbaikan: Tambahkan penanganan agar tidak error saat user memilih tanggal
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date, # Perbaikan Typo dari max_value ke max_date
        value=[min_date, max_date]
    )

# Pastikan date_range memiliki start dan end sebelum filter data
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Filter Data
main_df = df[(df["dteday"] >= pd.to_datetime(start_date)) & 
             (df["dteday"] <= pd.to_datetime(end_date))]

# --- MAIN PAGE ---
st.header('Bike Sharing Dashboard 🚲')

# MEMBUAT TABS
tab1, tab2, tab3 = st.tabs(["Kondisi Cuaca", "Tren Musim", "Pola Jam"])

# --- ISI TAB 1: CUACA ---
with tab1:
    st.subheader('Perbedaan Rata-rata Penyewaan Berdasarkan Cuaca')
    weather_df = main_df.groupby('weathersit')['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    # Perbaikan palette: tambahkan hue=x untuk menghilangkan Warning
    sns.barplot(x='weathersit', y='cnt', data=weather_df, hue='weathersit', palette='viridis', legend=False, ax=ax)
    ax.set_title("Rata-rata Penyewaan per Kondisi Cuaca")
    st.pyplot(fig)
    
    st.info("Insight SMART: Cuaca cerah mendominasi volume penyewaan.")

# --- ISI TAB 2: MUSIM ---
with tab2:
    st.subheader('Rata-rata Penyewaan Berdasarkan Musim')
    season_df = main_df.groupby('season')['cnt'].mean().reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(x='season', y='cnt', data=season_df, hue='season', palette='magma', legend=False, ax=ax2)
    st.pyplot(fig2)

# --- ISI TAB 3: JAM ---
with tab3:
    st.subheader('Pola Penyewaan Berdasarkan Jam Kerja')
    hour_df = main_df.groupby('hr')['cnt'].mean().reset_index()
    
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    sns.lineplot(x='hr', y='cnt', data=hour_df, marker='o', ax=ax3)
    ax3.set_xticks(range(0, 24))
    st.pyplot(fig3)

st.caption('Copyright © Muhammad Davin Al Hisyam 2024')
