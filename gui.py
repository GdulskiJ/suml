import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import requests
from datetime import datetime

API_KEY = "efba767b41bf0e2cffddc62cd20c02a6"

# ===================== DANE LOKALIZACJI =====================
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
    "Reykjavik": (64.14, -21.94)
}

df_locations = pd.DataFrame(
    [{"city": c, "lat": v[0], "lon": v[1]} for c, v in locations.items()]
)

# ===================== WCZYTANIE PROGNOZ =====================
df_forecast = pd.read_csv(
    r"C:\Users\gduls\PycharmProjects\suml\forecasts\forecast_avg_5dni.csv",
    parse_dates=["date"]
)

# ===================== API – BIEŻĄCA POGODA =====================
def get_current_weather(lat, lon):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&units=metric&lang=pl&appid={API_KEY}"
    )
    try:
        r = requests.get(url)
        data = r.json()
        return {
            "temp": round(data["main"]["temp"]),
            "humidity": data["main"]["humidity"],
            "wind": round(data["wind"]["speed"] * 3.6),
            "desc": data["weather"][0]["description"].capitalize(),
            "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }
    except:
        return None

# ===================== STREAMLIT UI =====================
st.title("🌍 Prognoza pogody – Europa")

# ----- MAPA -----
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_locations,
    get_position='[lon, lat]',
    get_radius=40000,
    get_fill_color=[0, 120, 255, 180],
    pickable=True
)

view_state = pdk.ViewState(latitude=54, longitude=15, zoom=3.5)
deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{city}"})
st.pydeck_chart(deck)

# ----- WYBÓR MIASTA -----
city_choice = st.selectbox("Wybierz miasto:", sorted(df_locations["city"].unique()))

if city_choice:
    lat, lon = locations[city_choice]
    weather = get_current_weather(lat, lon)

    st.markdown(f"## 📍 {city_choice}")

    col1, col2 = st.columns(2)

    # ----- BIEŻĄCA POGODA -----
    with col1:
        st.subheader("🌤 Aktualna pogoda")
        if weather:
            st.image(weather["icon"], width=100)
            st.write(
                f"**{weather['desc']}**\n\n"
                f"🌡️ {weather['temp']} °C\n\n"
                f"💧 {weather['humidity']} %\n\n"
                f"💨 {weather['wind']} km/h"
            )
        else:
            st.warning("Brak danych z API")

    # ----- PRAWDZIWA PROGNOZA 5 DNI -----
    with col2:
        st.subheader("📈 Prognoza na 5 dni")

        df_city = (
            df_forecast[df_forecast["city"] == city_choice]
            .sort_values("date")
        )

        if df_city.empty:
            st.warning("Brak prognozy dla tego miasta")
        else:
            fig = px.line(
                df_city,
                x="date",
                y="temp_avg",
                markers=True,
                labels={
                    "date": "Data",
                    "temp_forecast": "Temperatura (°C)"
                }
            )
            fig.update_layout(
                xaxis_tickformat="%d-%m",
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
