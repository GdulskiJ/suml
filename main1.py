from meteostat import Point, daily, stations
from datetime import datetime
import pandas as pd
import time
import os

# ---------------------------------------------
# Lista stolic europejskich
# ---------------------------------------------
locations = {
    "Warszawa": (52.23, 21.01),
    "Berlin": (52.52, 13.40),
    "Praga": (50.08, 14.42),
    "Budapeszt": (47.50, 19.04),
    "Madryt": (40.42, -3.70),
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
    "Belgrad": (44.82, 20.46),
    "Sofia": (42.70, 23.32),
    "Tallinn": (59.44, 24.75),
    "Ryga": (56.95, 24.11),
    "Wilno": (54.69, 25.28),
    "Luxemburg": (49.61, 6.13),
    "Vaduz": (47.14, 9.52),
    "Monako": (43.73, 7.42),
    "San Marino": (43.94, 12.45),
    "Kiszyniów": (47.01, 28.86),
    "Sarajewo": (43.85, 18.35),
    "Podgorica": (42.44, 19.26),
    "Skopje": (41.99, 21.43),
    "Mińsk": (53.90, 27.57),
    "Ljubljana": (46.05, 14.51),
    "Zagrzeb": (45.81, 15.98),
    "Kijów": (50.45, 30.52),
    "Moskwa": (55.75, 37.62),
    "Reykjavik": (64.14, -21.94)
}


def get_historical_data(lat, lon, start_year=2020):
    start = datetime(start_year, 1, 1)
    end = datetime.now()
    point = Point(lat, lon)

    nearest_station = stations.nearby(point).head(1)
    if nearest_station.empty:
        print(f"⚠️ Brak stacji w pobliżu {lat}, {lon}")
        return None

    station_id = nearest_station.index[0]

    df = daily(station_id, start, end).fetch()
    if df is None or df.empty:
        print(f"⚠️ Brak danych dla stacji {station_id}")
        return None

    cols = [c for c in ['temp', 'tmin', 'tmax', 'prcp', 'wspd', 'pres'] if c in df.columns]
    df = df[cols]
    df.index = pd.to_datetime(df.index)
    df = df.ffill()
    return df


# --- Tworzenie datasetu ---
all_data = []

for city, (lat, lon) in locations.items():
    print(f"Pobieram dane dla {city}...")
    df = get_historical_data(lat, lon)
    if df is None:
        print(f"Pomijam {city} z powodu braku danych")
        continue

    # Sprawdzenie kompletności danych
    start = datetime(2020, 1, 1)
    end = datetime.now()
    expected_days = (end - start).days + 1
    actual_days = len(df)



    df['city'] = city
    df['lat'] = lat
    df['lon'] = lon
    all_data.append(df.reset_index())
    time.sleep(0.5)

# --- Scalanie i zapis ---
if all_data:
    big_df = pd.concat(all_data, ignore_index=True)
    big_df = big_df.rename(columns={'index': 'date'})

    csv_file = os.path.join(os.getcwd(), "european_capitals_history_full2.csv")
    big_df.to_csv(csv_file, index=False)
    print(f"\n✅ Duży kompletny dataset zapisany: {csv_file}")
    print(f"Łącznie rekordów: {len(big_df)}")
else:
    print("❌ Nie pobrano żadnych danych.")