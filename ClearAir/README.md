# ClearAir

**System monitorowania jakosci powietrza** - platforma webowa wizualizujaca dane ze stacji czujnikow IoT (Sensor.Community) z mapa i statystykami dla Polski.

## Funkcje

- Mapa interaktywna czujnikow PM na terenie Polski
- Statystyki krajowe (srednia, mediana, rozklad jakosci)
- Synchronizacja z publicznym API [Sensor.Community](https://sensor.community)
- Baza PostgreSQL z historia pomiarow
- Automatyczna synchronizacja co 10 minut

## Stos technologiczny

| Warstwa | Technologia |
|---------|-------------|
| Frontend | React 19.2, TypeScript, Vite, Leaflet, Recharts |
| Backend | Python 3.12, FastAPI, SQLAlchemy, APScheduler |
| Baza | PostgreSQL 17 |
| Infrastruktura | Docker Compose |

## Uruchomienie (Docker)

```bash
cd clearair
docker compose up --build
```

- Aplikacja: http://localhost:5173
- API (Swagger): http://localhost:8000/docs

Po pierwszym uruchomieniu backend automatycznie pobierze dane dla `country=PL`.

## Uruchomienie lokalne (bez Dockera)

### 1. PostgreSQL

Utworzenie bazy i uruchomienie skryptu `database/init-schema.sql` 

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
set DATABASE_URL=postgresql+asyncpg://clearair:clearair@localhost:5432/clearair
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

## Dokumentacja

- [Dokumentacja projektowa](docs/ClearAir_Dokumentacja_Techniczna.md)
- [Dokumentacja techniczna](docs/ClearAir_Dokumentacja_Projektowa.md)

## API (skrot)

| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | `/api/health` | Stan uslugi |
| POST | `/api/sync` | Reczna synchronizacja |
| GET | `/api/map` | Punkty na mape |
| GET | `/api/stats` | Statystyki Polski |
| GET | `/api/sensors/{id}` | Szczegoly czujnika |

## Zrodlo danych

Dane pochodza z sieci [Sensor.Community](https://sensor.community) (dawniej Luftdaten.info), projektu open-source. API: `https://data.sensor.community`

## Licencja

Projekt edukacyjny. Dane Sensor.Community 
