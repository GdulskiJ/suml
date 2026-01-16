from datetime import date
import meteostat as ms

# Set time period
start = date(2026, 1, 1)
end = date(2026, 1, 15)

# Get daily data
ts = ms.daily(ms.Station(id='12375'), start, end)
df = ts.fetch()
print(df)

df.to_csv("warszawa_history_full.csv")
print(f"\n✅ Dane dla Warszawy zapisane: warszawa_history_full.csv")
print(f"Łącznie rekordów: {len(df)}")
# Print Da
# point = ms.Point(52.23, 21.01, 100)  # Example: Frankfurt, Germany
# stations = ms.stations.nearby(point, limit=4)
# print(stations)