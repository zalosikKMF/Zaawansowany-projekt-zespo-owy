# ClearAir - Dokumentacja Techniczna

Dokument jest zaawansowaną specyfikacją architektoniczną i techniczną systemu ClearAir. Zawiera szczegóły projektowe bazy danych, specyfikację komunikacji sieciowej (API) oraz wymagania wdrożeniowe. Przeznaczony jest dla deweloperów, inżynierów DevOps oraz administratorów systemu.

## 1. Architektura Oprogramowania i Stos Technologiczny
Architektura ClearAir opiera się na wydzielonym zapleczu (backend API), warstwie persystencji danych oraz kliencie SPA (Single Page Application).

| Technologia / Narzędzie | Wersja | Przeznaczenie i Uzasadnienie (Architektura) |
| :--- | :--- | :--- |
| **Python / FastAPI** | 3.12 / 0.115 | Fundament warstwy logicznej API. FastAPI wybrano z uwagi na natywne wsparcie zapytań asynchronicznych (asyncio), co znacząco zmniejsza czas oczekiwania (I/O bounds) przy pobieraniu dużych paczek z zewnętrznego API. |
| **PostgreSQL + SQLAlchemy** | 16 / 2.0 (asyncpg) | Główny silnik bazy danych (DB Engine) do trwałego przechowywania modeli obiektowo-relacyjnych. Baza jest zoptymalizowana indeksami do zapytań o charakterze szeregów czasowych (Time-Series). |
| **React.js + Vite** | 18 / 6 | Warstwa prezentacyjna. Reaktywność drzewa DOM pozwala na płynne działanie interfejsu (mapy) bez konieczności przeładowywania strony głównej. |
| **Docker Compose** | V2+ | Orkiestrator lokalnych środowisk deweloperskich. Definiuje 3 współpracujące mikrousługi w izolowanych kontenerach sieciowych. |

## 2. Struktura Repozytorium Kodu
Projekt dzieli się na dwie główne aplikacje w architekturze monorepo:

```text
clearair_monorepo/
├── backend/                  # Kontener Backendowy (Python)
│   ├── app/
│   │   ├── main.py           # Inicjalizacja instancji FastAPI i routing
│   │   ├── models.py         # Tabele SQLAlchemy (Klasy ORM)
│   │   ├── schemas.py        # Modele Pydantic (Walidacja Request/Response)
│   │   ├── api/routes.py     # Kontrolery HTTP (Endpointy)
│   │   └── services/         # Logika zewn: aq_sync.py (Pobieranie), aqi.py (Obliczenia)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # Kontener Frontendowy (React)
│   ├── src/
│   │   ├── components/       # MapLayer.jsx, SensorPanel.jsx
│   │   ├── api_client.js     # Moduł axios do odpytywania backendu
│   │   └── main.jsx
│   ├── package.json
│   └── Dockerfile
├── database/                 # Skrypty DB
│   └── init-schema.sql
└── docker-compose.yml        # Konfiguracja środowiska
```

## 3. Specyfikacja Bazy Danych i Indeksowanie

### 3.1 Schemat Tabel (DDL)
Architektura zakłada pełną relacyjność. Główne byty to: `locations` (współrzędne), `sensors` (urządzenia przypisane do miejsca), `measurements` (faktyczne dane liczbowe).

```sql
-- Przykładowa definicja tabeli pomiarowej z relacjami
CREATE TABLE measurements (
    id BIGINT PRIMARY KEY, -- ID pomiaru narzucone przez zewn API
    sensor_id INT NOT NULL,
    measured_at TIMESTAMP WITH TIME ZONE NOT NULL,
    pm10 DOUBLE PRECISION,
    pm25 DOUBLE PRECISION,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
);
```

### 3.2 Strategia Indeksów
* **Wydajność mapy (Latest Data):** Ponieważ mapa potrzebuje tylko *najnowszego* pomiaru dla 1500 czujników w jednej chwili, stworzono kompozytowy B-Tree index: `CREATE INDEX idx_sensor_time ON measurements (sensor_id, measured_at DESC);`
* **Optymalizacja widoku:** Utworzono specjalny `VIEW v_latest_sensor_readings`, który wykonuje zaawansowany podział analityczny (WINDOW FUNCTION) typu `DISTINCT ON (sensor_id)` ułatwiający zrzut dla frontendu.

## 4. Specyfikacja Interfejsu Programistycznego (REST API)
Cała dokumentacja interaktywna (Swagger UI / OpenAPI) serwowana jest automatycznie pod adresem `http://{adres_serwera}:8000/docs`.

| Metoda HTTP | Ścieżka (Endpoint) | Parametry Zapytań (Query/Path) | Zwracane dane (Opis) |
| :--- | :--- | :--- | :--- |
| GET | `/api/health` | Brak | Sprawdzenie pingu do bazy (200 OK). Zwraca flagę statusu db. |
| POST | `/api/sync` | Brak | Uruchamia manualnie skrypt (Job) pobierania JSON z zewnątrz (Sens.Comm). Wynik: ilość zaktualizowanych/dodanych rzędów. |
| GET | `/api/map` | `?pm_only=true` (boolean) | Zwraca masywną listę z geo-lokalizacjami i wyliczonym kolorem hex AQI (do renderowania mapy). |
| GET | `/api/sensors/{id}` | `id` (integer) - w ścieżce | Pobiera pełen model urządzenia oraz listę historycznych pomiarów (array timestampów i wartości float). |

## 5. Skale AQI, Klasyfikacja Logiczna i Algorytmy
Dla jednolitej prezentacji wyników (Frontend/UI) zaimplementowano sztywną klasyfikację po stronie Backendowej, odciążając klienta. Stosowana jest uproszczona kategoria (bazowa podstawa UE) dla stężenia najgroźniejszego pyłu zawieszonego – PM2.5 (mikrogram/metr sześcienny).

| Zakres (Stężenie PM2.5 µg/m³) | Zwracana flaga (Nazwa klucza) | Zwracany kod koloru (HEX) do styli mapy |
| :--- | :--- | :--- |
| <= 10 | bardzo_dobry | `#22c55e` (Green) |
| > 10 AND <= 20 | dobry | `#84cc16` (Lime) |
| > 20 AND <= 25 | umiarkowany | `#eab308` (Yellow) |
| > 25 AND <= 50 | dostateczny | `#f97316` (Orange) |
| > 50 AND <= 75 | zly | `#ef4444` (Red) |
| > 75 | bardzo_zly | `#7f1d1d` (Dark Red) |

## 6. Wdrażanie Systemu i Operacje Administracyjne (DevOps)

### 6.1 Konfiguracja Zmiennych (Env)
Zaleca się umieszczenie pliku `.env` w głównym katalogu uruchomieniowym z kluczowymi hasłami bazodanowymi oraz parametryzacją: `SYNC_COUNTRY=PL` (zabezpieczenie obszaru pobierania), `SYNC_INTERVAL_MINUTES=10`, `DATABASE_URL`, itp.

### 6.2 Proces Budowy Kontenerów
```bash
# Odtworzenie lub nowa budowa obrazów warstwowych bez używania cache:
docker compose build --no-cache

# Demonstracyjne uruchomienie aplikacji z procesami w tle:
docker compose up -d

# Podgląd ciągły logów z kontenera aplikacji backendowej:
docker compose logs -f backend
```
Backend zajmuje nasłuchiwanie na porcie `8000`. Komunikacja między serwisami odbywa się po domenie kontenerowej (np. `http://db:5432` dla bazy i `http://backend:8000` dla komunikatu Proxy Vite z Frontendu).
