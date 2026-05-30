# ClearAir – Dokumentacja techniczna

## 1. Stos technologiczny

| Komponent | Wersja | Uzasadnienie |
|-----------|--------|--------------|
| Python | 3.12 | Ekosystem data/API, czytelnosc |
| FastAPI | 0.115 | Szybkie REST API, OpenAPI |
| SQLAlchemy | 2.0 async | ORM z asyncpg |
| PostgreSQL | 16 | Relacyjna baza, indeksy czasowe |
| React | 18 | Komponentowy UI |
| Vite | 6 | Szybki dev/build |
| Leaflet | 1.9 | Mapy open-source |
| Docker Compose | 3 | Orkiestracja uslug |

## 2. Struktura repozytorium

```
clearair/
├── backend/app/          # Kod API
│   ├── main.py           # FastAPI + scheduler
│   ├── models.py         # Modele ORM
│   ├── api/routes.py     # Endpointy REST
│   └── services/         # Integracja Sensor.Community
├── frontend/src/         # Aplikacja React
├── database/init-schema.sql
├── docs/
└── docker-compose.yml
```

## 3. Baza danych PostgreSQL

### 3.1 Tabele

**locations** – pozycje stacji (PK: id z API)

**sensors** – czujniki (PK: id z API, FK: location_id)

**measurements** – pojedyncze odczyty (PK: id pomiaru z API)

**sync_logs** – historia synchronizacji

### 3.2 Indeksy
- `(sensor_id, measured_at DESC)` – ostatni pomiar per czujnik
- `(measured_at DESC)` – zapytania czasowe

### 3.3 Widok
`v_latest_sensor_readings` – ostatni pomiar kazdego czujnika (opcjonalnie do raportow SQL).

## 4. Integracja Sensor.Community

### 4.1 Endpoint
```
GET {SENSOR_COMMUNITY_URL}/airrohr/v1/filter/country={SYNC_COUNTRY}
Header: User-Agent: ClearAir/1.0 (...)
```

### 4.2 Mapowanie pol API -> baza

| API (sensordatavalues) | Kolumna |
|------------------------|---------|
| P1 | pm10 |
| P2 | pm25 |
| P0 | pm1 |
| temperature | temperature |
| humidity | humidity |
| pressure | pressure |

### 4.3 Strategia zapisu
- `INSERT ... ON CONFLICT DO UPDATE` dla locations i sensors
- `ON CONFLICT DO NOTHING` dla measurements (id unikalne z API)

## 5. API REST ClearAir

Baza URL: `http://localhost:8000`

| Metoda | Sciezka | Opis |
|--------|---------|------|
| GET | /api/health | Stan DB i ostatnia sync |
| POST | /api/sync | Uruchom synchronizacje |
| GET | /api/map?pm_only=true | Punkty mapy z AQI |
| GET | /api/stats | Statystyki krajowe |
| GET | /api/sensors/{id} | Historia czujnika |

Dokumentacja interaktywna: `/docs` (Swagger UI).

## 6. Klasyfikacja jakosci (PM2.5)

Uproszczona skala w `services/aqi.py` (ug/m3):

| PM2.5 | Etykieta | Kolor |
|-------|----------|-------|
| <= 10 | bardzo dobry | #22c55e |
| <= 20 | dobry | #84cc16 |
| <= 25 | umiarkowany | #eab308 |
| <= 50 | dostateczny | #f97316 |
| <= 75 | zly | #ef4444 |
| > 75 | bardzo zly | #7f1d1d |

## 7. Harmonogram synchronizacji

APScheduler – zadanie `scheduled_sync` co `SYNC_INTERVAL_MINUTES` (domyslnie 10). Przy starcie aplikacji wykonywana jest pierwsza synchronizacja.

## 8. Zmienne srodowiskowe

| Zmienna | Domyslnie | Opis |
|---------|-----------|------|
| DATABASE_URL | postgresql+asyncpg://... | Polaczenie async |
| SENSOR_COMMUNITY_URL | https://data.sensor.community | Baza API |
| SYNC_COUNTRY | PL | Kod kraju ISO |
| SYNC_INTERVAL_MINUTES | 10 | Interwal schedulera |
| CORS_ORIGINS | http://localhost:5173 | Dozwolone originy |

## 9. Wdrozenie

```bash
docker compose up --build -d
docker compose logs -f backend
```

Porty: 5173 (frontend), 8000 (API), 5432 (PostgreSQL).

## 10. Rozwoj lokalny

Backend:
```bash
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend && npm install && npm run dev
```

Proxy Vite przekierowuje `/api` na port 8000.

## 11. Testy manualne

1. `GET /api/health` – database: ok
2. `POST /api/sync` – records_saved > 0
3. `GET /api/map` – tablica z pm25
4. Otworz frontend – mapa z punktami w Polsce

## 12. Bezpieczenstwo (zakres edukacyjny)

- Brak uwierzytelniania uzytkownikow (projekt demo)
- Hasla DB tylko w srodowisku dev; w produkcji: sekrety, HTTPS, firewall
- Szanowanie limitow API – User-Agent, interwal 10 min

## 13. Mozliwe rozszerzenia

- Filtr po wojewodztwie (geometria PostGIS)
- Eksport CSV / raporty PDF
- Powiadomienia przy przekroczeniu progu PM2.5
- Pobieranie archiwum dziennego z archive.sensor.community
