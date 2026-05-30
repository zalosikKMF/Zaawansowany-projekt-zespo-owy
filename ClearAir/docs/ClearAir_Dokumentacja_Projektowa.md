# ClearAir - Dokumentacja Projektowa

Niniejszy dokument stanowi kompleksową specyfikację projektową i biznesową dla systemu monitorowania jakości powietrza ClearAir. Zawiera on cele biznesowe, podział ról w zespole, szczegółowy harmonogram prac (sprinty) oraz wymagania funkcjonalne aplikacji.

## 1. Wprowadzenie i Cel Projektu
Celem projektu **ClearAir** jest dostarczenie intuicyjnej i nowoczesnej aplikacji webowej, która agreguje, analizuje i wizualizuje na interaktywnej mapie dane dotyczące jakości powietrza. Aplikacja pobiera dane z rozproszonej sieci czujników IoT (Sensor.Community), dostarczając mieszkańcom i badaczom rzetelnych informacji na temat poziomu zanieczyszczeń (pyły PM2.5, PM10) w ich okolicy.

## 2. Zespół Projektowy i Podział Ról
Projekt realizowany jest przez dedykowany, interdyscyplinarny zespół specjalistów pracujących w metodyce zwinnej. Poniżej znajduje się struktura zespołu wraz z zakresem odpowiedzialności.

| Rola w projekcie | Imię i Nazwisko | Kluczowe Obowiązki |
| :--- | :--- | :--- |
| **Programista** | Mateusz Wawer | - Projektowanie struktury relacyjnej bazy danych PostgreSQL.<br>- Rozwój backendu (FastAPI, Python) oraz asynchronicznych zadań pobierania danych.<br>- Implementacja warstwy widoku w React.js.<br>- Konfiguracja środowiskowa Docker Compose. |
| **Projektant UX/UI** | Karol Wądołowski | - Badanie potrzeb użytkowników i tworzenie makiet Hi-Fi (np. Figma).<br>- Dobór palety kolorystycznej (szczególnie mapowanie kolorów zanieczyszczeń na mapie z dbałością o dostępność/kontrast).<br>- Zaprojektowanie responsywności (RWD) panelu czujnika i statystyk. |
| **Tester QA** | Piotr Saran | - Opracowywanie scenariuszy testowych (Test Cases) i testy manualne.<br>- Wykonywanie testów wydajnościowych API i zapytań SQL.<br>- Weryfikacja poprawności danych na mapie względem źródłowego API Sensor.Community.<br>- Raportowanie i weryfikacja naprawianych błędów (Bug Tracking). |

## 3. Wwymagania Systemu

### 3.1 Wwymagania Funkcjonalne
* **WF1:** System musi dynamicznie pobierać i agregować w czasie rzeczywistym pomiary pyłów PM10 i PM2.5.
* **WF2:** Zapewnienie interaktywnej mapy przestrzennej z naniesionymi punktami (markerami) dla każdego aktywnego czujnika.
* **WF3:** Zastosowanie kodowania kolorystycznego zgodnego z międzynarodowymi normami jakości powietrza (skala wielokolorowa AQI) w wizualizacji punktów na mapie.
* **WF4:** Po kliknięciu w dany czujnik, aplikacja musi wyświetlić panel ze szczegółowymi pomiarami historycznymi (wykres).
* **WF5:** System musi umożliwiać ręczne uruchomienie synchronizacji na żądanie (np. przez panel admina/API).

### 3.2 Wwymagania Niefunkcjonalne
* **WNF1 - Wydajność:** Czas renderowania mapy przy około 1500–2000 czujnikach nie może przekroczyć 3 sekund w nowoczesnych przeglądarkach.
* **WNF2 - Niezawodność:** W przypadku błędu połączenia z zewnętrznym API, aplikacja ma wykorzystywać najnowsze dane zbuforowane w bazie i informować użytkownika o braku bieżącej synchronizacji.
* **WNF3 - Użyteczność:** Pełna responsywność (poprawne działanie i układ na urządzeniach mobilnych, tabletach i desktopach).

## 4. Harmonogram Realizacji (Zwinne Sprinty)
Projekt realizowany jest w cyklu 4 sprintów (każdy sprint obejmuje 1–2 tygodnie pracy).

| Oznaczenie | Nazwa Sprintu | Kluczowe Zadania i Produkty (Deliverables) |
| :--- | :--- | :--- |
| **Sprint 1** | Analiza UX i Fundamenty Architektury | **UX:** Badanie potrzeb, tworzenie makiet Lo-Fi mapy oraz panelu statystyk.<br>**Programista:** Inicjalizacja repozytorium, projekt schematu bazy PostgreSQL, stworzenie Docker Compose, konfiguracja środowiska FastAPI. |
| **Sprint 2** | Backend i Integracja Danych | **Programista:** Oprogramowanie serwisu integrującego dane z Sensor.Community. Konfiguracja zadania cron (APScheduler). Endpointy dla frontendu (API REST).<br>**Tester:** Testowanie logiki mapowania JSON -> DB. Testowanie wydajności bazy za pomocą przykładowych zrzutów danych. |
| **Sprint 3** | Frontend: Mapa i Wizualizacja | **UX:** Dostarczenie makiet Hi-Fi. Akceptacja palety barw (AQI).<br>**Programista:** Kodowanie w React, osadzenie biblioteki Leaflet, wyświetlanie kółek w odpowiednich kolorach, budowa paska bocznego na szczegóły. |
| **Sprint 4** | Statystyki, Wdrożenie i Stabilizacja | **Programista:** Implementacja wykresów (Recharts), optymalizacja zapytań do bazy (indeksy), finalna konfiguracja CI/CD lub obrazów kontenerów.<br>**Tester:** Pełne testy E2E (End-to-End). Symulacja awarii. Zgłaszanie poprawek i retesty UI. |

## 5. Instrukcja Obsługi Aplikacji (Dla Użytkowników)
Interfejs aplikacji zaprojektowano z myślą o prostocie (zgodnie z wytycznymi UX):
1. **Ekran Główny (Mapa):** Po otwarciu aplikacji, centralną część ekranu zajmuje interaktywna mapa ze znacznikami poszczególnych czujników. Aby przybliżyć rejon, można użyć rolki myszy (scroll) lub gestu na urządzeniu mobilnym. Kolor znaczników intuicyjnie odzwierciedla stan powietrza (od zieleni - bardzo dobre powietrze, do bordowego - bardzo złe).
2. **Detale Pomiaru:** Kliknięcie lewym przyciskiem myszy (lub tapnięcie palcem) w konkretny punkt na mapie powoduje płynne wysunięcie panelu pobocznego. Panel wyświetla adres czujnika, aktualną wilgotność, temperaturę oraz dokładne stężenia PM.
3. **Zakładka Analiz i Statystyk:** W górnym menu nawigacyjnym znajduje się odnośnik do panelu "Statystyki". Kliknięcie otwiera globalne podsumowanie – np. średnie stężenie pyłów w obserwowanym kraju oraz wykresy trendów z ostatnich dni.
