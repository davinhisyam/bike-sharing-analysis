import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
import datetime

# SETUP
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Set style seaborn agar lebih elegan (Background putih bersih)
sns.set_theme(style="whitegrid")

# LOAD DATA 
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "main_data.csv")
df = pd.read_csv(file_path)
df['dteday'] = pd.to_datetime(df['dteday'])

# SIDEBAR
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=200)
    st.markdown("## Filter Data")
    
    # Menyiapkan rentang waktu
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    
    date_range = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Mencegah error jika user baru pilih 1 tanggal
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Filter Data berdasarkan input tanggal di sidebar
main_df = df[(df["dteday"] >= pd.to_datetime(start_date)) & 
             (df["dteday"] <= pd.to_datetime(end_date))]

# MAIN PAGE
st.title('🚲 Bike Sharing Data Dashboard')
st.markdown("Selamat datang di dashboard analisis data penyewaan sepeda! Gunakan menu di sebelah kiri untuk memfilter data berdasarkan tanggal.")

# KARTU METRIK / SUMMARY
st.subheader("📌 Summary Kinerja")
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_df['cnt'].sum()
    st.metric("Total Penyewaan (Unit)", value=f"{total_rentals:,}")

with col2:
    if not main_df.empty:
        avg_rentals = int(main_df['cnt'].mean())
    else:
        avg_rentals = 0
    st.metric("Rata-rata Penyewaan per Jam", value=f"{avg_rentals:,}")

with col3:
    if not main_df.empty:
        peak_day = main_df.groupby(main_df['dteday'].dt.date)['cnt'].sum().idxmax()
        st.metric("Hari Puncak Penyewaan", value=str(peak_day))
    else:
        st.metric("Hari Puncak Penyewaan", value="-")

st.markdown("---")

# MEMBUAT TABS UNTUK VISUALISASI 
tab1, tab2, tab3 = st.tabs(["🌤️ Kondisi Cuaca", "🌸 Tren Musim", "⏰ Pola Jam"])

# TAB 1: CUACA 
with tab1:
    st.subheader('Bagaimana Pengaruh Cuaca Terhadap Penyewaan Sepeda?')
    weather_df = main_df.groupby('weathersit')['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='weathersit', y='cnt', data=weather_df, hue='weathersit', palette='Blues_d', legend=False, ax=ax)
    ax.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    ax.set_title("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca", fontsize=14, pad=15)
    st.pyplot(fig)
    
    st.info("**Insight SMART:** Cuaca Cerah memiliki rata-rata penyewaan tertinggi. Terdapat penurunan drastis pada saat cuaca buruk, sehingga perlu penyesuaian armada lapangan.")

# TAB 2: MUSIM 
with tab2:
    st.subheader('Musim Apa yang Paling Ramai?')
    season_df = main_df.groupby('season')['cnt'].mean().reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(x='season', y='cnt', data=season_df, hue='season', palette='autumn', legend=False, ax=ax2)
    ax2.set_xlabel('Musim', fontsize=12)
    ax2.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    ax2.set_title("Rata-rata Penyewaan Berdasarkan Musim", fontsize=14, pad=15)
    st.pyplot(fig2)

# TAB 3: JAM 
with tab3:
    st.subheader('Kapan Jam Sibuk (Peak Hours) Terjadi?')
    hour_df = main_df.groupby('hr')['cnt'].mean().reset_index()
    
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    sns.lineplot(x='hr', y='cnt', data=hour_df, marker='o', color='#1f77b4', linewidth=2.5, ax=ax3)
    ax3.set_xlabel('Jam (0-23)', fontsize=12)
    ax3.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    ax3.set_title("Pola Penyewaan Sepeda Harian", fontsize=14, pad=15)
    ax3.set_xticks(range(0, 24))
    ax3.grid(axis='x', alpha=0.3)
    st.pyplot(fig3)
    
    st.info("**Insight SMART:** Puncak penyewaan terjadi pada jam berangkat kerja (08:00) dan pulang kerja (17:00). Jadwal pemeliharaan sepeda disarankan pada jam non-sibuk (10:00 - 14:00).")

# --- COPYRIGHT DINAMIS ---
current_year = datetime.date.today().year
st.caption(f'Copyright © Muhammad Davin Al Hisyam {current_year}')
