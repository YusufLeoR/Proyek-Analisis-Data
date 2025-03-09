import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Helper functions
def humidity_rentals(day_df):
    day_df["hum_category"] = day_df["hum"].apply(lambda x: "Rendah" if x <= 0.4 else ("Sedang" if x <= 0.7 else "Tinggi"))
    df_grouped = day_df.groupby("hum_category")["cnt"].mean().reset_index()
    return df_grouped

def season_rentals(day_df, selected_seasons):
    if not selected_seasons:
        selected_seasons = [1, 2, 3, 4]
    season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    seasonal_counts = day_df[day_df["season"].isin(selected_seasons)].groupby("season")["registered"].sum().reset_index()
    seasonal_counts["season"] = seasonal_counts["season"].map(season_labels)
    return seasonal_counts

def hourly_workingday(hour_df, selected_workingday):
    if not selected_workingday:
        selected_workingday = [0, 1]
    return hour_df[hour_df["workingday"].isin(selected_workingday)].groupby(["hr", "workingday"])["cnt"].mean().unstack()

st.sidebar.header(" Eksplorasi Data Yuk!")
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim:", 
    options=[1, 2, 3, 4], 
    format_func=lambda x: ["Spring", "Summer", "Fall", "Winter"][x-1], 
    default=[]
)
selected_workingday = st.sidebar.multiselect(
    "Pilih Jenis Hari:", 
    options=[0, 1], 
    format_func=lambda x: "Libur" if x == 0 else "Hari Kerja", 
    default=[]
)

st.title("Dashboard Penyewaan Sepeda")

st.header("🔵 Scatterplot Kelembaban vs. Jumlah Penyewa")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=day_df["hum"], y=day_df["cnt"], alpha=0.6, color="b", ax=ax)
ax.set_xlabel("Kelembaban")
ax.set_ylabel("Jumlah Penyewa Sepeda")
ax.set_title("Hubungan Kelembaban dengan Jumlah Penyewa Sepeda")
st.pyplot(fig)

st.header("🌦️ Tren Penyewaan Sepeda oleh Pengguna Terdaftar di Setiap Musim")
season_data = season_rentals(day_df, selected_seasons)
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season", y="registered", data=season_data, palette="coolwarm", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan Sepeda oleh Pengguna Terdaftar")
ax.set_title("Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

st.header("⏰ Pola Penggunaan Sepeda Berdasarkan Waktu")
hourly_data = hour_df.groupby("hr")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(x="hr", y="cnt", data=hourly_data, marker="o", linestyle="-", color="b", ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Tren Penggunaan Sepeda per Jam")
st.pyplot(fig)

st.header("🏢 vs. 🏖️ Pola Penyewaan Sepeda: Hari Kerja vs. Hari Libur")
hourly_workingday_data = hourly_workingday(hour_df, selected_workingday)
fig, ax = plt.subplots(figsize=(8, 5))
hourly_workingday_data.plot(kind="bar", ax=ax, colormap="coolwarm")
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Pola Penyewaan Sepeda: Hari Kerja vs. Hari Libur")
st.pyplot(fig)

st.caption('📌 Copyright @yusuflr 2025')