from datetime import date
import meteostat as ms
import pandas as pd
import time
from meteostat import daily

# -----------------------------
# Lista miast jako Point
# -----------------------------
cities = {
    "Warszawa": ms.Point(52.23, 21.01),
    "Berlin": ms.Point(52.52, 13.40),
    "Praga": ms.Point(50.08, 14.42),
    "Budapeszt": ms.Point(47.50, 19.04),
    "Madryt": ms.Point(40.42, -3.70),
    "Paryż": ms.Point(48.85, 2.35),
    "Londyn": ms.Point(51.51, -0.13),
    "Wiedeń": ms.Point(48.21, 16.37),
    "Bruksela": ms.Point(50.85, 4.35),
    "Amsterdam": ms.Point(52.37, 4.90),
    "Lizbona": ms.Point(38.72, -9.13),
    "Oslo": ms.Point(59.91, 10.75),
    "Sztokholm": ms.Point(59.33, 18.07),
    "Helsinki": ms.Point(60.17, 24.94),
    "Dublin": ms.Point(53.33, -6.25),
    "Ateny": ms.Point(37.98, 23.73),
    "Belgrad": ms.Point(44.82, 20.46),
    "Sofia": ms.Point(42.70, 23.32),
    "Tallinn": ms.Point(59.44, 24.75),
    "Ryga": ms.Point(56.95, 24.11),
    "Wilno": ms.Point(54.69, 25.28),
    "Luxemburg": ms.Point(49.61, 6.13),
    "Vaduz": ms.Point(47.14, 9.52),
    "Monako": ms.Point(43.73, 7.42),
    "San Marino": ms.Point(43.94, 12.45),
    "Kiszyniów": ms.Point(47.01, 28.86),
    "Sarajewo": ms.Point(43.85, 18.35),
    "Podgorica": ms.Point(42.44, 19.26),
    "Skopje": ms.Point(41.99, 21.43),
    "Mińsk": ms.Point(53.90, 27.57),
    "Ljubljana": ms.Point(46.05, 14.51),
    "Zagrzeb": ms.Point(45.81, 15.98),
    "Kijów": ms.Point(50.45, 30.52),
    "Moskwa": ms.Point(55.75, 37.62),
    "Reykjavik": ms.Point(64.14, -21.94)
}

# -----------------------------
# Zakres czasu
# -----------------------------
start = date(2010, 1, 1)
end = date.today()  # nigdy przyszła data

# -----------------------------
# Pobieranie danych
# -----------------------------
all_data = []

for city, point in cities.items():
    print(f"Pobieram dane dla {city}...")

    # Pobranie danych dziennych bez stacji
    ts = ms.daily(point, start, end)
    df = ts.fetch()

    if df is None or df.empty:
        print(f"⚠️ Brak danych dla {city}")
        continue

    # Wyrównanie kalendarza i uzupełnienie braków
    df = df.asfreq("D").ffill()

    df = df.reset_index()
    df["city"] = city

    all_data.append(df)

    time.sleep(0.5)  # grzecznie dla API

# -----------------------------
# Scalanie i zapis
# -----------------------------
if all_data:
    big_df = pd.concat(all_data, ignore_index=True)
    big_df.to_csv("european_capitals_weather_full.csv", index=False)

    print("\n✅ Zapisano kompletny plik: european_capitals_weather_full.csv")
    print(f"📊 Łącznie rekordów: {len(big_df)}")
else:
    print("❌ Nie udało się pobrać żadnych danych")
