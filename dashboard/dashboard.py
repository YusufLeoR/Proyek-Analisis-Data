import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# Helper functions
def humidity_rentals(day_df):
    day_df["hum_category"] = day_df["hum"].apply(lambda x: "Rendah" if x <= 0.4 else ("Sedang" if x <= 0.7 else "Tinggi"))
    df_grouped = day_df.groupby("hum_category")["cnt"].mean().reset_index()
    return df_grouped

def season_rentals(day_df):
    season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    seasonal_counts = day_df.groupby("season")["registered"].sum().reset_index()
    seasonal_counts["season"] = seasonal_counts["season"].map(season_labels)
    return seasonal_counts

def hourly_usage(hour_df):
    hourly_usage = hour_df.groupby("hr")["cnt"].mean().reset_index()
    return hourly_usage

def hourly_workingday(hour_df):
    return hour_df.groupby(["hr", "workingday"])["cnt"].mean().unstack()

st.title("Dashboard Penyewaan Sepeda")    

st.header("🔵 Scatterplot Kelembaban vs. Jumlah Penyewa")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=day_df["hum"], y=day_df["cnt"], alpha=0.6, color="b", ax=ax)
ax.set_xlabel("Kelembaban")
ax.set_ylabel("Jumlah Penyewa Sepeda")
ax.set_title("Hubungan Kelembaban dengan Jumlah Penyewa Sepeda")
st.pyplot(fig)
st.markdown(
    """
    Pola yang terlihat sangat tidak jelas untuk hubungan kelembaban dengan jumlah penyewaan sepeda sehingga terlihat sangat acak tidak berpola
    """
)


st.header("🌦️ Tren Penyewaan Sepeda oleh Pengguna Terdaftar di Setiap Musim")
season_data = season_rentals(day_df)
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season", y="registered", data=season_data, palette="coolwarm", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan Sepeda oleh Pengguna Terdaftar")
ax.set_title("Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 6))
plt.plot(season_data["season"], season_data["registered"], marker="o", linestyle="-", color="b", linewidth=2, markersize=8)
plt.xlabel("Musim")
plt.ylabel("Total Penyewaan Sepeda (Registered Users)")
plt.title("Tren Penyewaan Sepeda Pengguna Terdaftar Berdasarkan Musim")
plt.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)
st.markdown(
    """
    Penggambaran dengan grafik garis sehingga bisa melihat trennya bagaimana. Terlihat bahwa tren jumlah penyewaan sepeda semakin menaik dari musim semi hingga puncaknya musim gugur lalu menurun di musim dingin
    """
)


st.header("⏰ Pola Penggunaan Sepeda Berdasarkan Waktu dalam Sehari")
hourly_data = hourly_usage(hour_df)
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(x="hr", y="cnt", data=hourly_data, marker="o", linestyle="-", color="b", ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Tren Penggunaan Sepeda per Jam")
st.pyplot(fig)
st.markdown(
    """
    Peak hour adalah jam 8 dan jam 17
    """
)


st.header("🏢 vs. 🏖️ Perbandingan Pola Penggunaan Sepeda pada Hari Kerja vs. Hari Libur")
hourly_workingday_data = hourly_workingday(hour_df)
fig, ax = plt.subplots(figsize=(8, 5))
hourly_workingday_data.plot(kind="bar", ax=ax, colormap="coolwarm")
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Pola Penyewaan Sepeda: Hari Kerja vs. Hari Libur")
st.pyplot(fig)
st.markdown(
    """
    Peak hour tetap dengan menunjukkan ketika hari kerja lebih tinggi
    """
)

st.caption('Copyright @yusuflr 2025')