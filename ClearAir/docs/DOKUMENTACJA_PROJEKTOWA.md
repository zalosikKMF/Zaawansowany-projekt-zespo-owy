# ClearAir – Dokumentacja projektowa

## 1. Wprowadzenie

### 1.1 Nazwa projektu
**ClearAir** – System monitorowania jakosci powietrza

### 1.2 Cel projektu
Dostarczenie aplikacji webowej umozliwiajacej sledzenie zmian pomiarow jakosci powietrza na terenie Polski na podstawie danych z sieci czujnikow IoT Sensor.Community.

### 1.3 Zakres projektu
- Projektowanie struktury systemu i dobor technologii
- Zaprojektowanie aplikacji webowej (mapa, statystyki, panel czujnika)
- Pobieranie pomiarow z publicznego API Sensor.Community
- Utworzenie relacyjnej bazy danych PostgreSQL
- Dokumentacja projektowa i techniczna

### 1.4 Interesariusze
- Uzytkownicy koncowi – osoby monitorujace jakosc powietrza w swojej okolicy
- Administrator systemu – utrzymanie synchronizacji i bazy
- Zespol projektowy – rozwój i dokumentacja

## 2. Analiza wymagan

### 2.1 Wymagania funkcjonalne
| ID | Wymaganie |
|----|-----------|
| F1 | Wyswietlanie czujnikow na mapie Polski |
| F2 | Kolorowanie punktow wedlug poziomu PM2.5 |
| F3 | Statystyki ogolnopolskie (srednia, mediana, rozklad) |
| F4 | Szczegoly wybranego czujnika z historia |
| F5 | Automatyczna synchronizacja danych z API |
| F6 | Reczna synchronizacja na zadanie |
| F7 | Trwale przechowywanie pomiarow w PostgreSQL |

### 2.2 Wymagania niefunkcjonalne
- Dostepnosc API Sensor.Community z odpowiednim User-Agent
- Czas odpowiedzi mapy < 3 s przy typowej liczbie czujnikow (~1500 PM w PL)
- Skalowalnosc: mozliwosc rozszerzenia o inne kraje (parametr SYNC_COUNTRY)
- Uruchomienie w Docker Compose dla powtarzalnosci srodowiska

## 3. Zrodlo danych

**Sensor.Community** (https://sensor.community) – projekt open-source, siec czujnikow obywatelskich mierzacych m.in. pyl zawieszony PM10 (P1) i PM2.5 (P2).

Endpoint uzywany w ClearAir:
```
GET https://data.sensor.community/airrohr/v1/filter/country=PL
```

Dane obejmuja ostatnie 5 minut pomiarow. Archiwum dzienne dostepne jest osobno na http://archive.sensor.community/.

## 4. Architektura systemu

```
[Czujniki IoT] --> [Sensor.Community API] --> [ClearAir Backend] --> [PostgreSQL]
                                                      |
                                                      v
                                              [ClearAir Frontend]
                                              Mapa + Statystyki
```

### 4.1 Warstwy
1. **Prezentacja** – React, Leaflet, Recharts
2. **Logika biznesowa** – FastAPI, klasyfikacja AQI, synchronizacja
3. **Dane** – PostgreSQL (lokalizacje, czujniki, pomiary, logi sync)

## 5. Model danych (koncepcyjny)

- **Lokalizacja** – wspolrzedne, kraj, typ (indoor/outdoor)
- **Czujnik** – typ (np. SDS011, PMS7003), powiazanie z lokalizacja
- **Pomiar** – timestamp, PM10, PM2.5, temperatura, wilgotnosc
- **Log synchronizacji** – status, liczba rekordow

## 6. Scenariusze uzytkownika

1. Uzytkownik otwiera strone glowna – widzi mape Polski z kolorowymi punktami.
2. Klika punkt – w panelu bocznym pojawiaja sie dane czujnika i wykres historii.
3. Administrator klika „Synchronizuj dane” – system pobiera najnowsze pomiary z API.

## 7. Harmonogram (propozycja)

| Etap | Czas | Deliverable |
|------|------|-------------|
| Analiza i projekt | 1 tydz. | Dokumentacja projektowa |
| Backend + DB | 2 tyg. | API, synchronizacja |
| Frontend | 2 tyg. | Mapa, statystyki |
| Testy i wdrozenie | 1 tydz. | Docker, dokumentacja techniczna |

## 8. Ryzyka

| Ryzyko | Mitygacja |
|--------|-----------|
| Niedostepnosc API | Retry, log bledow, wyswietlanie ostatnich danych z bazy |
| Brak User-Agent | Stały naglowek w kliencie HTTP |
| Duza liczba punktow na mapie | Filtrowanie tylko czujnikow z PM2.5 |

## 9. Podsumowanie

ClearAir spelnia cele projektu edukacyjnego: integruje dane open-source, przechowuje je relacyjnie i prezentuje w przejrzystej formie geograficznej i statystycznej dla uzytkownikow w Polsce.
