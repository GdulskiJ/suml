import pandas as pd
from meteostat import Point, Daily
from datetime import datetime
import time

# ---------------------------------------------
# Lista stolic europejskich
# ---------------------------------------------
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


# ---------------------------------------------
# Funkcja: pobieranie danych historycznych
# ---------------------------------------------
def get_historical_data(lat, lon, start_year=2010):
    start = datetime(start_year, 1, 1)
    end = datetime.now()
    point = Point(lat, lon)
    df = Daily(point, start, end).fetch()
    df = df[['tavg', 'tmin', 'tmax', 'prcp', 'wspd', 'pres']]
    df.index = pd.to_datetime(df.index)
    df = df.fillna(method='ffill')
    return df

# ---------------------------------------------
# Tworzenie datasetu
# ---------------------------------------------
all_data = []

for city, (lat, lon) in locations.items():
    print(f"Pobieram dane dla {city}...")
    df = get_historical_data(lat, lon)
    df['city'] = city
    df['lat'] = lat
    df['lon'] = lon
    all_data.append(df.reset_index())
    time.sleep(0.5)  # delikatne opóźnienie

# ---------------------------------------------
# Scalanie w jeden DataFrame
# ---------------------------------------------
big_df = pd.concat(all_data, ignore_index=True)
big_df = big_df.rename(columns={'time': 'date'})

# ---------------------------------------------
# Zapis do CSV
# ---------------------------------------------
big_df.to_csv("european_capitals_history_full.csv", index=False)
print("\n✅ Duży historyczny dataset zapisany: european_capitals_history.csv")
print(f"Łącznie rekordów: {len(big_df)}")
