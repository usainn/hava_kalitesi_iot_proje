import joblib
import os
import pandas as pd
import streamlit as st
import requests

CSV_PATH = "/home/pi/sensor_log.csv"
API_KEY = os.getenv("OPENWEATHER_API_KEY")

MODEL_PATH = "/home/pi/aq_model.joblib"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)  			 //modeli bir kez yükle tekrar tekrar kullan
    
    
# ---------- Helper functions ----------
def mq_level(value, t1=500, t2=700):           //ham sensör değerleri alır  - insan anlamlı etiket döndürür.
    if value < t1:
        return "Good"
    if value < t2:
        return "Medium"
    return "Bad"

def aqi_label(aqi):      		      api etiketlemesini yapar kullanıcaya sayı değil anlam lazım çünkü
    return {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }.get(aqi, "Unknown")

@st.cache_data(ttl=300)		                              // apiye her saniye  istek atılmaz 5sn de bir atılır				
def fetch_weather(lat, lon):					
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {							//apiye soracağımız parametreler
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }
    r = requests.get(url, params=params, timeout=10)           //http isteği oluşturur
    r.raise_for_status()					//eğer http cevabı gelemzse 200 OK devam etmez
    j = r.json()						//gelen api json cevabını paython objesine çevir
    return {
        "city": j.get("name"),
        "temp": j["main"].get("temp"),
        "hum": j["main"].get("humidity"),			//cevaptan işimize yarayan adımları seçer
        "pressure": j["main"].get("pressure"),
        "wind": j.get("wind", {}).get("speed"),
        "desc": (j.get("weather") or [{}])[0].get("description"),
    }

@st.cache_data(ttl=300)
def fetch_air(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    j = r.json()
    item = (j.get("list") or [{}])[0]
    comps = item.get("components", {})
    return {
        "aqi": item.get("main", {}).get("aqi"),
        "pm2_5": comps.get("pm2_5"),
        "pm10": comps.get("pm10"),
        "no2": comps.get("no2"),
        "o3": comps.get("o3"),
        "so2": comps.get("so2"),
        "co": comps.get("co"),
    }

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
st.title("Raspberry Pi Smart Air Quality Monitoring System")

# Load local sensor data
df = pd.read_csv(CSV_PATH)
df["iso_time"] = pd.to_datetime(df["iso_time"], errors="coerce")
df = df.dropna(subset=["iso_time"]).sort_values("iso_time")
latest = df.iloc[-1]


model = load_model()

X_latest = pd.DataFrame([{
    "temp_c": float(latest["temp_c"]),
    "hum_pct": float(latest["hum_pct"]),
    "mq2": float(latest["mq2"]),
    "mq135": float(latest["mq135"]),
}])

pred = int(model.predict(X_latest)[0])

label_map = {
    0: "Good",
    1: "Moderate",
    2: "Bad"
}

st.subheader("AI Prediction")
st.metric("Predicted Air Quality Class", label_map[pred])



proba = model.predict_proba(X_latest)[0]
st.write(
    f"Probabilities -> Good: {proba[0]:.2f}, "
    f"Moderate: {proba[1]:.2f}, "
    f"Bad: {proba[2]:.2f}"
)


# Top metrics (local sensors)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Indoor Temperature (C)", f"{latest['temp_c']:.1f}")
c2.metric("Indoor Humidity (%)", f"{latest['hum_pct']:.1f}")
c3.metric("MQ-2", f"{latest['mq2']:.0f}", mq_level(latest["mq2"]))
c4.metric("MQ-135", f"{latest['mq135']:.0f}", mq_level(latest["mq135"]))

st.caption(f"Last record time: {latest['iso_time']}")

# Charts
st.subheader("Local Sensors - MQ2 / MQ135")
st.line_chart(df.set_index("iso_time")[["mq2", "mq135"]].tail(600))

st.subheader("Local Temperature / Humidity")
st.line_chart(df.set_index("iso_time")[["temp_c", "hum_pct"]].tail(600))


# OpenWeather section
st.subheader("Outdoor Environment - OpenWeather API")

lat = st.number_input("Latitude", value=36.5850, format="%.6f")
lon = st.number_input("Longitude", value=36.1600, format="%.6f")

if not API_KEY:
    st.error("OPENWEATHER_API_KEY environment variable not found.")
else:
    try:
        weather = fetch_weather(lat, lon)
        air = fetch_air(lat, lon)

        w1, w2, w3, w4, w5 = st.columns(5)
        w1.metric("City", str(weather["city"]))
        w2.metric("Outdoor Temp (C)", str(weather["temp"]))
        w3.metric("Outdoor Hum (%)", str(weather["hum"]))
        w4.metric("Wind Speed (m/s)", str(weather["wind"]))
        w5.metric("Weather", str(weather["desc"]))

        a1, a2, a3, a4, a5 = st.columns(5)
        a1.metric("AQI (1-5)", f"{air['aqi']} - {aqi_label(air['aqi'])}")
        a2.metric("PM2.5 (ug/m3)", str(air["pm2_5"]))
        a3.metric("PM10 (ug/m3)", str(air["pm10"]))
        a4.metric("NO2 (ug/m3)", str(air["no2"]))
        a5.metric("O3 (ug/m3)", str(air["o3"]))

    except Exception as e:
        st.error(f"OpenWeather API error: {e}")
