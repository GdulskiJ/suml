# Predykcja pogody - SUML

Projekt z przedmiotu **Systemy Uczące się Maszynowo**.

## Demo aplikacji

Przetestuj działającą wersję naszej aplikacji Streamlit:

[Aplikacja do przewidywania pogody](https://przewidywaniepogody.streamlit.app/)  
URL do skopiowania: https://przewidywaniepogody.streamlit.app/

## Autorzy

- Jakub Gdulski (s27753)  
- Adam Mielko (s27669)

Predykcja temperatury dla europejskich stolic z uzyciem modeli LSTM, GRU i Prophet.

Pelna dokumentacja: [docs/DOKUMENTACJA.md](docs/DOKUMENTACJA.md)

## Struktura projektu

```
suml/
├── app/                    
│   └── streamlit_app.py    # aplikacja webowa
├── data/
│   ├── raw/                # surowe dane
│   └── processed/          # dane po preprocessingu
├── docs/
│   └── DOKUMENTACJA.md     # dokumentacja projektu
├── forecasts/              # prognozy CSV
├── models/                 # wytrenowane modele .keras
├── notebooks/
│   ├── 01_data_analysis.ipynb
│   ├── 02_lstm_model.ipynb
│   ├── 03_gru_model.ipynb
│   └── 04_forecast_ensemble.ipynb
├── requirements.txt
└── README.md
```

## Instalacja

```bash
pip install -r requirements.txt
```

## Uruchomienie

Aplikacja Streamlit:
```bash
streamlit run app/streamlit_app.py
```

## Modele

| Model | Opis | R2 |
|-------|------|-----|
| LSTM | 2 warstwy, dropout 0.2 | ~0.92 |
| GRU | 2 warstwy, dropout 0.2 | ~0.90 |
| Prophet | model Facebooka | ~0.88 |

Finalna prognoza to srednia z LSTM i Prophet.

## Dane

- Zrodlo: Meteostat API (dane 2010-2026)
- Aktualna pogoda: OpenWeatherMap API
- 24 stolice europejskie
- Cechy: temp, tmin, tmax, opady, wiatr, cisnienie

## Technologie

- Python 3.10+
- TensorFlow/Keras
- scikit-learn
- Prophet
- Streamlit
- pandas, numpy, matplotlib
