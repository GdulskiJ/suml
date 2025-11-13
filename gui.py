import streamlit as st
import pandas as pd
import pydeck as pdk
import random
import plotly.express as px
import requests
from datetime import datetime, timedelta

API_KEY = "efba767b41bf0e2cffddc62cd20c02a6"

# --- Dane lokalizacji ---
locations = {
    "Warszawa": (52.23, 21.01),
    "Berlin": (52.52, 13.40),
    "Praga": (50.08, 14.42),
    "Budapeszt": (47.50, 19.04),
    "Madryt": (40.42, -3.70),
    "Rzym": (41.90, 12.50),
    "Paryż": (48.85, 2.35),
    "Londyn": (51.51, -0.13),
    "Wiedeń": (48.21, 16.37),
    "Bruksela": (50.85, 4.35),
    "Amsterdam": (52.37, 4.90),
    "Lizbona": (38.72, -9.13),
    "Oslo": (59.91, 10.75),
    "Sztokholm": (59.33, 18.07),
    "Helsinki": (60.17, 24.94),
    "Dublin": (53.33, -6.25),
    "Ateny": (37.98, 23.73),
    "Kopenhaga": (55.68, 12.57),
    "Belgrad": (44.82, 20.46),
    "Sofia": (42.70, 23.32),
    "Tallinn": (59.44, 24.75),
    "Ryga": (56.95, 24.11),
    "Wilno": (54.69, 25.28),
    "Valletta": (35.89, 14.51),
    "Luxemburg": (49.61, 6.13),
    "Vaduz": (47.14, 9.52),
    "Monako": (43.73, 7.42),
    "Andora la Vella": (42.51, 1.52),
    "San Marino": (43.94, 12.45),
    "Kiszyniów": (47.01, 28.86),
    "Sarajewo": (43.85, 18.35),
    "Podgorica": (42.44, 19.26),
    "Skopje": (41.99, 21.43),
    "Tirana": (41.33, 19.82),
    "Mińsk": (53.90, 27.57),
    "Ljubljana": (46.05, 14.51),
    "Zagrzeb": (45.81, 15.98),
    "Kijów": (50.45, 30.52),
    "Moskwa": (55.75, 37.62),
    "Reykjavik": (64.14, -21.94)
}

# --- DataFrame ---
df = pd.DataFrame([{"city": city, "lat": coords[0], "lon": coords[1]} for city, coords in locations.items()])

# --- Funkcja pobierająca bieżącą pogodę ---
def get_current_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=pl&appid={API_KEY}"
    try:
        r = requests.get(url)
        data = r.json()
        return {
            "temperatura": round(data["main"]["temp"]),
            "wilgotność": data["main"]["humidity"],
            "wiatr": round(data["wind"]["speed"] * 3.6),  # m/s -> km/h
            "opis": data["weather"][0]["description"].capitalize(),
            "ikona": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }
    except:
        return {"temperatura": None, "wilgotność": None, "wiatr": None, "opis": "Brak danych", "ikona": ""}

# --- Funkcja generująca prognozę 5-dniową demo ---
def fake_forecast_5days():
    days = [datetime.now() + timedelta(days=i) for i in range(1, 6)]
    dni_pl_map = {
        "Monday": "Poniedziałek",
        "Tuesday": "Wtorek",
        "Wednesday": "Środa",
        "Thursday": "Czwartek",
        "Friday": "Piątek",
        "Saturday": "Sobota",
        "Sunday": "Niedziela"
    }
    dni_pl = [dni_pl_map[d.strftime("%A")] for d in days]
    temps = [random.randint(-10, 35) for _ in range(5)]
    icons = ["☀️", "☁️", "🌧️", "❄️", "⛈️", "🌫️"]
    return pd.DataFrame({"Dzień": dni_pl, "Temperatura (°C)": temps, "Ikona": [random.choice(icons) for _ in range(5)]})

# --- Streamlit ---
st.title("🌍 Mapa pogody – Europa")

# --- Mapa PyDeck ---
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[lon, lat]',
    get_radius=40000,
    get_fill_color=[0, 100, 255, 180],
    pickable=True
)
view_state = pdk.ViewState(latitude=54, longitude=15, zoom=3.5, pitch=0)
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{city}"})
st.pydeck_chart(r)

st.markdown("Kliknij w punkt na mapie lub wybierz miasto z listy:")

# --- Wybór miasta ---
city_choice = st.selectbox("Miasto:", df["city"].tolist())

if city_choice:
    lat, lon = locations[city_choice]
    forecast = get_current_weather(lat, lon)

    st.markdown(f"<h3 style='color:blue'>📍 {city_choice}</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌤 Bieżąca pogoda")
        st.image(forecast['ikona'], width=100)
        st.write(
            f"**{forecast['opis']}**  \n"
            f"🌡️ Temperatura: {forecast['temperatura']}°C  \n"
            f"💧 Wilgotność: {forecast['wilgotność']}%  \n"
            f"💨 Wiatr: {forecast['wiatr']} km/h"
        )

    # --- Prognoza 5-dniowa ---
    df_5days = fake_forecast_5days()
    with col2:
        st.subheader("📈 Prognoza na kolejne 5 dni")
        fig = px.line(df_5days, x="Dzień", y="Temperatura (°C)", markers=True, text="Ikona")
        fig.update_traces(textposition="top center")
        # pionowe linie dla czytelności
        for x in df_5days["Dzień"]:
            fig.add_vline(x=x, line_dash="dash", line_color="gray", opacity=0.3)
        st.plotly_chart(fig, width="stretch")
