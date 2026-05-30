# ClearAir - Dokumentacja Techniczna

Dokument jest zaawansowaną specyfikacją architektoniczną i techniczną systemu ClearAir. Zawiera szczegóły projektowe bazy danych, specyfikację komunikacji sieciowej (API) oraz wymagania wdrożeniowe. 

## 1. Architektura Oprogramowani
Architektura ClearAir opiera się na wydzielonym zapleczu (backend API), warstwie persystencji danych oraz kliencie SPA (Single Page Application).

| Technologia / Narzędzie | Wersja | Przeznaczenie i Uzasadnienie|
| :--- | :--- | :--- |
| **Python / FastAPI** | 3.12 | Obsługuje logikę aplikacji i komunikację z API. Dzięki pracy asynchronicznej szybciej pobiera dane z zewnętrznych źródeł. |
| **PostgreSQL + SQLAlchemy** | 17.0| Przechowuje dane aplikacji. Dobrze radzi sobie z dużą ilością danych i historią zapisów w czasie. |
| **React.js + Vite** | 19.2 | Odpowiada za wygląd i działanie strony internetowej. Umożliwia płynne aktualizowanie mapy i innych elementów bez odświeżania strony. |
| **Docker Compose** | V2+ | Ułatwia uruchamianie całego projektu. Zarządza trzema współpracującymi usługami działającymi w oddzielnych kontenerach. |

## 2. Specyfikacja Bazy Danych i Indeksowanie

### 2.1 Schemat Tabel (DDL)
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

### 2.2 Strategia Indeksów
* **Wydajność mapy (Latest Data):** Ponieważ mapa potrzebuje tylko *najnowszego* pomiaru dla 1500 czujników w jednej chwili, stworzono kompozytowy B-Tree index: `CREATE INDEX idx_sensor_time ON measurements (sensor_id, measured_at DESC);`
* **Optymalizacja widoku:** Utworzono specjalny `VIEW v_latest_sensor_readings`, który wykonuje zaawansowany podział analityczny (WINDOW FUNCTION) typu `DISTINCT ON (sensor_id)` ułatwiający zrzut dla frontendu.

## 3. Specyfikacja Interfejsu Programistycznego (REST API)
Cała dokumentacja interaktywna (Swagger UI / OpenAPI) serwowana jest automatycznie pod adresem `http://{adres_serwera}:8000/docs`.

| Metoda HTTP | Ścieżka (Endpoint) | Parametry Zapytań (Query/Path) | Zwracane dane (Opis) |
| :--- | :--- | :--- | :--- |
| GET | `/api/health` | Brak | Sprawdzenie pingu do bazy (200 OK). Zwraca flagę statusu db. |
| POST | `/api/sync` | Brak | Uruchamia manualnie skrypt (Job) pobierania JSON z zewnątrz (Sens.Comm). Wynik: ilość zaktualizowanych/dodanych rzędów. |
| GET | `/api/map` | `?pm_only=true` (boolean) | Zwraca masywną listę z geo-lokalizacjami i wyliczonym kolorem hex AQI (do renderowania mapy). |
| GET | `/api/sensors/{id}` | `id` (integer) - w ścieżce | Pobiera pełen model urządzenia oraz listę historycznych pomiarów (array timestampów i wartości float). |

## 4. Skale AQI, Klasyfikacja Logiczna i Algorytmy
Dla jednolitej prezentacji wyników (Frontend/UI) zaimplementowano sztywną klasyfikację po stronie Backendowej, odciążając klienta. Stosowana jest uproszczona kategoria (bazowa podstawa UE) dla stężenia najgroźniejszego pyłu zawieszonego – PM2.5 (mikrogram/metr sześcienny).

| Zakres (Stężenie PM2.5 µg/m³) | Zwracana flaga (Nazwa klucza) | Zwracany kod koloru (HEX) do styli mapy |
| :--- | :--- | :--- |
| <= 10 | bardzo_dobry | `#22c55e` (Green) |
| > 10 AND <= 20 | dobry | `#84cc16` (Lime) |
| > 20 AND <= 25 | umiarkowany | `#eab308` (Yellow) |
| > 25 AND <= 50 | dostateczny | `#f97316` (Orange) |
| > 50 AND <= 75 | zly | `#ef4444` (Red) |
| > 75 | bardzo_zly | `#7f1d1d` (Dark Red) |

## 5. Wdrażanie Systemu i Operacje Administracyjne (DevOps)

### 5.1 Konfiguracja Zmiennych (Env)
Zaleca się umieszczenie pliku `.env` w głównym katalogu uruchomieniowym z kluczowymi hasłami bazodanowymi oraz parametryzacją: `SYNC_COUNTRY=PL` (zabezpieczenie obszaru pobierania), `SYNC_INTERVAL_MINUTES=10`, `DATABASE_URL`, itp.

### 5.2 Proces Budowy Kontenerów
```bash
# Odtworzenie lub nowa budowa obrazów warstwowych bez używania cache:
docker compose build --no-cache

# Demonstracyjne uruchomienie aplikacji z procesami w tle:
docker compose up -d

# Podgląd ciągły logów z kontenera aplikacji backendowej:
docker compose logs -f backend
```
Backend zajmuje nasłuchiwanie na porcie `8000`. Komunikacja między serwisami odbywa się po domenie kontenerowej (np. `http://db:5432` dla bazy i `http://backend:8000` dla komunikatu Proxy Vite z Frontendu).
