from datetime import date
import meteostat as ms
import meteostat as ms
from meteostat import daily

# Koordynaty Warszawy
warszawa = ms.Point(52.23, 21.01)

stations = ms.stations.nearby(warszawa, limit=1)
print(stations.index[0])


# Zakres czasu
start = date(2010, 1, 1)
end = date(2026, 1, 15)

# Pobranie danych dziennych
ts = ms.daily(stations.index[0], start, end)
df = ts.fetch()

print(df)

# Zapis do CSV
df.to_csv("warszawa_history_full.csv")
print(f"\n✅ Dane dla Warszawy zapisane: warszawa_history_full.csv")
print(f"📊 Łącznie rekordów: {len(df)}")
