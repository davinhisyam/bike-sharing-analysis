import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# --- SETUP HALAMAN ---
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# --- LOAD DATA ---
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "main_data.csv")
df = pd.read_csv(file_path)
df['dteday'] = pd.to_datetime(df['dteday'])

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png", width=100)
    st.markdown("## Filter Data")
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=df["dteday"].min(),
        max_value=df["dteday"].max(),
        value=[df["dteday"].min(), df["dteday"].max()]
    )

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = df["dteday"].min(), df["dteday"].max()

main_df = df[(df["dteday"] >= pd.to_datetime(start_date)) & 
             (df["dteday"] <= pd.to_datetime(end_date))]

# --- MAIN PAGE ---
st.title('🚲 Bike Sharing Data Dashboard')

# Summary Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Penyewaan", value=f"{main_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Penyewaan/Jam", value=f"{int(main_df['cnt'].mean()):,}")

tab1, tab2, tab3 = st.tabs(["🌤️ Cuaca", "🌸 Musim", "⏰ Jam"])

# --- TAB 1: CUACA ---
with tab1:
    st.subheader('Rata-rata Penyewaan Berdasarkan Kondisi Cuaca')
    weather_df = main_df.groupby('weathersit')['cnt'].mean().reset_index()
    
    # Perbaikan: Perkecil ukuran (figsize 8x4)
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Perbaikan Warna: Gunakan satu warna, highlight yang tertinggi
    colors = ["#D3D3D3" if (x < max(weather_df['cnt'])) else "#1f77b4" for x in weather_df['cnt']]
    
    sns.barplot(x='weathersit', y='cnt', data=weather_df, palette=colors, ax=ax)
    ax.set_xlabel(None)
    ax.set_ylabel("Rata-rata")
    ax.tick_params(axis='both', labelsize=10)
    st.pyplot(fig)
    st.info("Highlight warna biru menunjukkan kondisi cuaca dengan rata-rata penyewaan tertinggi.")

# --- TAB 2: MUSIM ---
with tab2:
    st.subheader('Rata-rata Penyewaan Berdasarkan Musim')
    season_df = main_df.groupby('season')['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    # Highlight warna untuk musim tertinggi
    colors_season = ["#D3D3D3" if (x < max(season_df['cnt'])) else "#1f77b4" for x in season_df['cnt']]
    
    sns.barplot(x='season', y='cnt', data=season_df, palette=colors_season, ax=ax)
    ax.set_xlabel(None)
    ax.set_ylabel("Rata-rata")
    st.pyplot(fig)

# --- TAB 3: JAM ---
with tab3:
    st.subheader('Tren Penyewaan Berdasarkan Jam')
    hour_df = main_df.groupby('hr')['cnt'].mean().reset_index()
    
    # Gunakan Line Chart karena lebih efektif untuk data waktu (Time Series)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(x='hr', y='cnt', data=hour_df, marker='o', color="#1f77b4", ax=ax)
    ax.set_xticks(range(0, 24))
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata")
    st.pyplot(fig)


st.caption(f'Copyright © Muhammad Davin Al Hisyam 2026')
