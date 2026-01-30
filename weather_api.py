import requests
import pandas as pd
from datetime import datetime

def fetch_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    dates, temps, humidity, wind = [], [], [], []

    for item in data["list"]:
        dates.append(datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S"))
        temps.append(item["main"]["temp"])
        humidity.append(item["main"]["humidity"])
        wind.append(item["wind"]["speed"])

    df = pd.DataFrame({
        "Date": dates,
        "Temperature (°C)": temps,
        "Humidity (%)": humidity,
        "Wind Speed (m/s)": wind
    })

    return df
