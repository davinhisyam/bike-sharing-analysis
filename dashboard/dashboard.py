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
    
    # Filter Rentang Waktu
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_value,
        value=[min_date, max_date]
    )

# Filter Data
main_df = df[(df["dteday"] >= str(start_date)) & 
             (df["dteday"] <= str(end_date))]

# --- MAIN PAGE ---
st.header('Bike Sharing Dashboard 🚲')

# MEMBUAT TABS (Agar tidak perlu scroll jauh)
tab1, tab2, tab3 = st.tabs(["Kondisi Cuaca", "Tren Musim", "Pola Jam"])

# --- ISI TAB 1: CUACA ---
with tab1:
    st.subheader('Pengaruh Cuaca Terhadap Penyewaan')
    weather_df = main_df.groupby('weathersit')['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='weathersit', y='cnt', data=weather_df, palette='viridis', ax=ax)
    st.pyplot(fig)
    
    st.info("Insight: Cuaca cerah mendominasi total penyewaan harian.")

# --- ISI TAB 2: MUSIM ---
with tab2:
    st.subheader('Rata-rata Penyewaan Berdasarkan Musim')
    season_df = main_df.groupby('season')['cnt'].mean().reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(x='season', y='cnt', data=season_df, palette='magma', ax=ax2)
    st.pyplot(fig2)

# --- ISI TAB 3: JAM ---
with tab3:
    st.subheader('Pola Penyewaan Berdasarkan Jam Puncak')
    hour_df = main_df.groupby('hr')['cnt'].mean().reset_index()
    
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    sns.lineplot(x='hr', y='cnt', data=hour_df, marker='o', ax=ax3)
    ax3.set_xticks(range(0, 24))
    st.pyplot(fig3)

st.caption('Copyright © Muhammad Davin Al Hisyam 2024')
