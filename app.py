import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv

# 🔴 IMPORTANT: move weather_service.py to same folder as app.py
from weather_api import fetch_weather_data

# ---------------- LOAD ENV ----------------
load_dotenv()
default_api_key = os.getenv("OPENWEATHER_API_KEY")

# ---------------- UI CONFIG ----------------
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌦️ Weather Visualization Dashboard")
st.markdown("Real-time weather insights using **FREE OpenWeatherMap API**")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Settings")

api_key = st.sidebar.text_input(
    "Enter OpenWeatherMap API Key",
    type="password",
    value=default_api_key if default_api_key else ""
)

city = st.sidebar.text_input("Enter City Name", value="Ahmedabad")

fetch = st.sidebar.button("🔍 Fetch Weather Data")

# ---------------- DEFAULT MESSAGE ----------------
if not fetch:
    st.info("👈 Enter API key and city, then click **Fetch Weather Data**")

# ---------------- MAIN LOGIC ----------------
if fetch:
    if not api_key:
        st.error("❌ API key is required")
    else:
        df = fetch_weather_data(city, api_key)

        if df is None:
            st.error("❌ Invalid city name or API key")
        else:
            st.success(f"✅ Weather data loaded for **{city}**")

            # ----------- METRICS -----------
            col1, col2, col3 = st.columns(3)

            col1.metric("🌡 Avg Temp (°C)", round(df["Temperature (°C)"].mean(), 2))
            col2.metric("💧 Avg Humidity (%)", round(df["Humidity (%)"].mean(), 2))
            col3.metric("💨 Avg Wind (m/s)", round(df["Wind Speed (m/s)"].mean(), 2))

            st.divider()

            # ----------- CHARTS -----------
            st.subheader("📈 Temperature Trend")
            fig1, ax1 = plt.subplots()
            ax1.plot(df["Date"], df["Temperature (°C)"])
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Temperature (°C)")
            st.pyplot(fig1)

            st.subheader("📊 Humidity Levels (Next 10 Records)")
            fig2, ax2 = plt.subplots()
            sns.barplot(x=df["Date"][:10], y=df["Humidity (%)"][:10], ax=ax2)
            ax2.tick_params(axis='x', rotation=45)
            st.pyplot(fig2)

            st.subheader("🌬 Wind Speed Distribution")
            fig3, ax3 = plt.subplots()
            sns.scatterplot(x=df["Date"], y=df["Wind Speed (m/s)"], ax=ax3)
            ax3.set_xlabel("Date")
            ax3.set_ylabel("Wind Speed (m/s)")
            st.pyplot(fig3)

            # ----------- DATA TABLE -----------
            st.subheader("📋 Raw Weather Data")
            st.dataframe(df, use_container_width=True)

            # ----------- DOWNLOAD -----------
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="⬇ Download CSV",
                data=csv_data,
                file_name="weather_data.csv",
                mime="text/csv"
            )
