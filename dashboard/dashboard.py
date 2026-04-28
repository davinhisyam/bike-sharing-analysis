import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set style seaborn
sns.set(style='dark')

# Mendapatkan path direktori script ini berada
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "main_data.csv")

# Membaca data
hour_df = pd.read_csv(file_path)

# Judul Dashboard
st.header('Bike Sharing Dashboard 🚲')

# 1. Visualisasi Pengaruh Cuaca
st.subheader('Pengaruh Cuaca Terhadap Penyewaan Sepeda')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='weathersit', 
    y='cnt', 
    data=hour_df, 
    palette='viridis',
    errorbar=None,
    ax=ax
)
ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Cuaca')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig)

# 2. Visualisasi Tren Musim
st.subheader('Tren Penyewaan Sepeda Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='season', 
    y='cnt', 
    data=hour_df, 
    order=['Spring', 'Summer', 'Fall', 'Winter'],
    palette='coolwarm',
    errorbar=None,
    ax=ax
)
ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig)

# 3. Visualisasi Jam Sibuk
st.subheader('Pola Penyewaan Sepeda Berdasarkan Jam')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x='hr', 
    y='cnt', 
    data=hour_df, 
    marker='o', 
    color='tab:blue',
    errorbar=None,
    ax=ax
)
ax.set_title('Pola Penyewaan Sepeda Harian (0-23 Jam)')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_xticks(range(0, 24))
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

st.caption('Copyright © Muhammad Davin Al Hisyam 2024')
