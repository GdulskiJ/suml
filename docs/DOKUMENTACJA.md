# Dokumentacja projektu: Predykcja temperatury dla stolic europejskich

**Przedmiot:** Systemy Uczace sie Maszynowo (SUML)

**Autorzy:**
- Jakub Gdulski (s27753)
- Adam Mielko (s27669)

**Link do aplikacji:** https://przewidywaniepogody.streamlit.app

---

## 1. Opis tematu i uzasadnienie

### Temat
Predykcja temperatury powietrza dla 24 europejskich stolic z wykorzystaniem modeli uczenia maszynowego (LSTM, GRU, Prophet).

### Dlaczego to wazne?

**Aspekt spoleczny:**
- Prognozowanie pogody ma bezposredni wplyw na codzienne zycie ludzi - planowanie podrozy, ubioru, aktywnosci na zewnatrz
- Ekstremalne temperatury (upaly, mrozy) stanowia zagrozenie dla zdrowia, szczegolnie osob starszych
- Wczesne ostrzezenia o anomaliach pogodowych moga ratowac zycie

**Aspekt biznesowy:**
- Rolnictwo - planowanie zasiewow i zbiorow zalezy od prognoz
- Energetyka - zapotrzebowanie na prad/gaz silnie koreluje z temperatura
- Turystyka - branzy hotelarskiej i lotniczej zalezy na dokładnych prognozach
- Logistyka - firmy transportowe planuja trasy w oparciu o warunki pogodowe

**Dlaczego ML a nie tradycyjne metody?**
Klasyczne modele numeryczne (NWP) wymagaja ogromnej mocy obliczeniowej i danych z wielu zrodel. Modele ML moga dawac przyzwoite wyniki bazujac tylko na danych historycznych, co jest tansze i szybsze do wdrozenia.

---

## 2. Opis zbioru danych

### Zrodlo danych
Dane pobrane z **Meteostat API** - otwarte API udostepniajace historyczne dane meteorologiczne ze stacji pogodowych na calym swiecie.

### Zakres danych
- **Okres:** 2010-01-01 do 2026-01-14 (okolo 15 lat danych)
- **Czestotliwosc:** dane dzienne
- **Liczba miast:** 24 stolice europejskie
- **Laczna liczba rekordow:** ~76 000

### Zmienne w datasecie

| Zmienna | Opis | Jednostka |
|---------|------|-----------|
| time | data pomiaru | datetime |
| temp | srednia temperatura dobowa | °C |
| tmin | temperatura minimalna | °C |
| tmax | temperatura maksymalna | °C |
| prcp | opady | mm |
| wspd | predkosc wiatru | km/h |
| pres | cisnienie atmosferyczne | hPa |
| city | nazwa miasta | string |
| lat | szerokosc geograficzna | float |
| lon | dlugosc geograficzna | float |

### Lista miast
Warszawa, Berlin, Praga, Budapeszt, Madryt, Paryz, Londyn, Wieden, Bruksela, Amsterdam, Lizbona, Oslo, Sztokholm, Helsinki, Dublin, Ateny, Kopenhaga, Belgrad, Sofia, Tallinn, Ryga, Wilno, Reykjavik, Rzym

### Ocena wiarygodnosci danych

**Zalety:**
- Meteostat agreguje dane z oficjalnych stacji meteorologicznych (SYNOP, METAR)
- Dane sa standaryzowane i maja jednolity format
- API jest darmowe i dobrze udokumentowane

**Wady/Ograniczenia:**
- Niektore stacje maja luki w danych (np. Lizbona - 314 dni brakujacych)
- Opady (prcp) maja najwiecej brakow (~15% wartosci NaN)
- Dane sa interpolowane gdy brak bezposrednich pomiarow

### EDA (Exploratory Data Analysis)

Analiza eksploracyjna zostala przeprowadzona w notebooku `01_data_analysis.ipynb`.

**Glowne obserwacje:**

1. **Rozklad temperatury:**
   - Srednia: 11.6°C
   - Min: -27.1°C (temperatura minimalna)
   - Max: 43.0°C (temperatura maksymalna)
   - Rozklad zblizony do normalnego z lekka asymetria

2. **Braki danych:**
   - temp, tmax: 0 brakow
   - tmin: 1 brak
   - prcp: ~11800 brakow (15%)
   - wspd, pres: ~1100 brakow (1.5%)

3. **Korelacje:**
   - temp vs tmax: 0.98 (bardzo silna)
   - temp vs tmin: 0.97 (bardzo silna)
   - temp vs pres: -0.15 (slaba ujemna)
   - prcp vs wspd: 0.12 (slaba dodatnia)

4. **Sezonowosc:**
   - Wyrazny cykl roczny temperatur
   - Amplituda wieksza w miastach polnocnych (Helsinki, Sztokholm)
   - Mniejsza zmiennosc w miastach poludniowych (Lizbona, Ateny)

---

## 3. Preprocessing danych

Preprocessing zostal wykonany w notebooku `01_data_analysis.ipynb`.

### Kroki preprocessingu:

**1. Obsluga brakujacych wartosci:**
```
- tmin, wspd, pres: interpolacja czasowa (method='time')
- uzupelnienie brakow na poczatku/koncu serii: forward fill + backward fill
- prcp: pozostawione NaN (opady sa nieregularne, interpolacja nie ma sensu)
```

**2. Obsluga outlierow:**
```
- Clipping wartosci do zakresu [1 percentyl, 99 percentyl]
- Dotyczy: temp, tmin, tmax, prcp, wspd, pres
```

**3. Feature engineering:**
```
- temp_rolling3: srednia kroczaca z 3 dni (wygladzanie szumu)
- temp_diff1: roznica temperatury wzgledem poprzedniego dnia (trend)
```

**4. Normalizacja (przed trenowaniem modeli):**
```
- MinMaxScaler do zakresu [0, 1]
- Osobny scaler dla X (sekwencje) i y (etykiety)
- Fit tylko na danych treningowych (unikniecie data leakage)
```

**5. Tworzenie sekwencji czasowych:**
```
- Window size: 20 dni (dane wejsciowe)
- Forecast horizon: 1 lub 5 dni (prognoza)
- Format: [samples, timesteps, features] dla LSTM/GRU
```

---

## 4. Modelowanie i wyniki

### Model 1: LSTM (Long Short-Term Memory)

**Architektura:**
```
- LSTM(64 units, return_sequences=True)
- Dropout(0.2)
- LSTM(32 units)
- Dense(1) lub Dense(5) dla prognozy 5-dniowej
```

**Hiperparametry:**
- Optimizer: Adam
- Loss: MSE (Mean Squared Error)
- Epochs: 100 (z EarlyStopping, patience=10)
- Batch size: 32
- Window: 20 dni

**Wyniki (Walk-Forward Cross-Validation, 5 folds):**

| Metryka | Wartosc |
|---------|---------|
| R² | 0.8985 |
| MAE | 2.03°C |
| MSE | 6.98 |
| RMSE | 2.56°C |

### Model 2: GRU (Gated Recurrent Unit)

**Architektura:**
```
- GRU(64 units, return_sequences=True)
- Dropout(0.2)
- GRU(32 units)
- Dense(1)
```

**Wyniki (Walk-Forward Cross-Validation, 5 folds):**

| Metryka | Wartosc |
|---------|---------|
| R² | 0.8981 |
| MAE | 1.45°C |
| MSE | 3.51 |
| RMSE | 1.87°C |

### Model 3: Prophet (Facebook)

Prophet zostal uzyty jako model baseline/referencyjny. Jest to model addytywny zaprojektowany do prognozowania szeregow czasowych z sezonowoscia.

**Wyniki:**
| Metryka | Wartosc |
|---------|---------|
| R² | ~0.88 |

### Ensemble (srednia prognoz)

Finalna prognoza to **srednia arytmetyczna** z modeli LSTM i Prophet.

Uzycie ensemble pozwala:
- Zmniejszyc wariancje predykcji
- Skompensowac slabosci poszczegolnych modeli
- Uzyskac bardziej stabilne prognozy

### Porownanie modeli

| Model | R² | MAE | RMSE |
|-------|-----|------|------|
| LSTM | 0.90 | 2.03 | 2.56 |
| GRU | 0.90 | 1.45 | 1.87 |
| Prophet | 0.88 | - | - |
| **Ensemble** | **~0.91** | - | - |

**Wnioski:**
- GRU ma nieco lepsze MAE/RMSE niz LSTM przy podobnym R²
- Oba modele RNN znacznie lepsze od prostej sredniej kroczącej
- Prophet jest dobry jako baseline ale ustepuje sieciom rekurencyjnym
- Ensemble daje najbardziej stabilne wyniki

---

## 5. Wykorzystane narzedzia

### Jezyk programowania
**Python 3.10+**
- Najpopularniejszy jezyk do ML
- Bogaty ekosystem bibliotek
- Latwa integracja z notebookami Jupyter

### Biblioteki ML

**TensorFlow/Keras**
- Framework do deep learningu od Google
- Wysoki poziom abstrakcji (Keras API)
- Dobre wsparcie dla warstw rekurencyjnych (LSTM, GRU)
- Uzyty do: budowy i trenowania modeli LSTM/GRU

**scikit-learn**
- Standardowa biblioteka ML w Pythonie
- Uzyta do: normalizacji (MinMaxScaler), walidacji krzyzowej (TimeSeriesSplit), metryk (MSE, MAE, R²)

**Prophet**
- Biblioteka od Facebooka do prognozowania szeregow czasowych
- Automatyczne wykrywanie sezonowosci
- Uzyty jako model referencyjny

### Biblioteki do danych

**pandas**
- Obsluga danych tabelarycznych
- Operacje na szeregach czasowych
- Wczytywanie/zapis CSV

**numpy**
- Operacje na tablicach wielowymiarowych
- Reshaping danych dla LSTM/GRU

### Wizualizacja

**matplotlib**
- Podstawowe wykresy (liniowe, histogramy)
- Wykresy strat podczas treningu

**seaborn**
- Wykresy statystyczne (heatmapy korelacji, boxploty)
- Histogramy z KDE

**plotly**
- Interaktywne wykresy
- Mapy z lokalizacjami miast

### Dane pogodowe

**Meteostat**
- API do pobierania danych historycznych
- Dane ze stacji SYNOP/METAR

**OpenWeatherMap API**
- Aktualne dane pogodowe
- Uzyte w aplikacji Streamlit

### Aplikacja webowa

**Streamlit**
- Framework do tworzenia aplikacji webowych w Pythonie
- Szybkie prototypowanie dashboardow
- Integracja z pandas/plotly

**pydeck**
- Wizualizacja map
- Warstwa ScatterplotLayer dla miast

### Srodowisko

**Jupyter Notebook**
- Interaktywna analiza danych
- Dokumentowanie eksperymentow

**Git/GitHub**
- Wersjonowanie kodu
- Wspolpraca w zespole

---

## 6. Struktura projektu

```
suml/
├── app/
│   └── streamlit_app.py      # aplikacja webowa
├── data/
│   ├── raw/                  # surowe dane z API
│   └── processed/            # dane po preprocessingu
├── docs/
│   └── DOKUMENTACJA.md       # ten plik
├── forecasts/
│   ├── forecast_avg_5dni.csv           # prognozy ensemble
│   ├── forecasts_5dni_all_cities_lstm.csv
│   └── forecasts_5dni_all_cities_prophet.csv
├── models/                   # zapisane modele .keras
├── notebooks/
│   ├── 01_data_analysis.ipynb    # EDA i preprocessing
│   ├── 02_lstm_model.ipynb       # model LSTM
│   ├── 03_gru_model.ipynb        # model GRU
│   └── 04_forecast_ensemble.ipynb # laczenie prognoz
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 7. Instrukcja uruchomienia

### Wymagania
- Python 3.10+
- pip

### Instalacja
```bash
git clone https://github.com/[UZUPELNIC]/suml.git
cd suml
pip install -r requirements.txt
```

### Uruchomienie aplikacji
```bash
streamlit run app/streamlit_app.py
```

### Uruchomienie notebookow
```bash
jupyter notebook notebooks/
```

---

## 8. Podzial pracy

| Zadanie | Osoba |
|---------|-------|
| Pobranie i przygotowanie danych | Jakub Gdulski |
| EDA i preprocessing | Adam Mielko |
| Model LSTM | Jakub Gdulski |
| Model GRU | Adam Mielko |
| Model Prophet | Jakub Gdulski |
| Aplikacja Streamlit | Adam Mielko |
| Dokumentacja | obaj |

---

## 9. Podsumowanie

Projekt pokazuje ze modele deep learningowe (LSTM, GRU) moga skutecznie prognozowac temperature na podstawie danych historycznych. Osiagniete R² na poziomie ~0.90 oznacza ze model wyjasnia 90% wariancji w danych - to dobry wynik jak na stosunkowo prosta architekture sieci.

**Co mozna poprawic:**
- Dodanie wiecej cech (wilgotnosc, zachmurzenie, dane z sasiadujacych miast)
- Przetestowanie architektury Transformer
- Dluzsza prognoza (7-14 dni)
- Hyperparameter tuning (Optuna, GridSearch)

---

*Dokumentacja wygenerowana: styczen 2026*
