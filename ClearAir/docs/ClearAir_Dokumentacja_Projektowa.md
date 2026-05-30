# ClearAir - Dokumentacja Projektowa

Niniejszy dokument stanowi kompleksową specyfikację projektową i biznesową dla systemu monitorowania jakości powietrza ClearAir. Zawiera on cele biznesowe, podział ról w zespole, szczegółowy harmonogram prac (sprinty) oraz wymagania funkcjonalne aplikacji.

## 1. Wprowadzenie i Cel Projektu
Celem projektu **ClearAir** jest dostarczenie intuicyjnej i nowoczesnej aplikacji webowej, która agreguje, analizuje i wizualizuje na interaktywnej mapie dane dotyczące jakości powietrza. Aplikacja pobiera dane z rozproszonej sieci czujników IoT (Sensor.Community), dostarczając mieszkańcom rzetelnych informacji na temat poziomu zanieczyszczeń (pyły PM2.5, PM10) w ich okolicy.

## 2. Zespół Projektowy i Podział Ról
Projekt realizowany jest przez zespół studentów WSPA. Poniżej znajduje się struktura zespołu wraz z zakresem odpowiedzialności.

| Rola w projekcie | Imię i Nazwisko | 
| :--- | :--- | 
| **Programista** | Mateusz Wawer | 
| **Projektant UX/UI** | Karol Wądołowski | 
| **Tester QA** | Piotr Saran | |

## 3. Wwymagania Systemu

### 3.1 Wwymagania Funkcjonalne
* System musi dynamicznie pobierać i agregować w czasie rzeczywistym pomiary pyłów PM10 i PM2.5.
* Zapewnienie interaktywnej mapy przestrzennej z naniesionymi punktami (markerami) dla każdego aktywnego czujnika.
* Zastosowanie kodowania kolorystycznego zgodnego z międzynarodowymi normami jakości powietrza (skala wielokolorowa AQI) w wizualizacji punktów na mapie.
* Po kliknięciu w dany czujnik, aplikacja musi wyświetlić panel ze szczegółowymi pomiarami historycznymi (wykres).
*  System musi umożliwiać ręczne uruchomienie synchronizacji na żądanie (np. przez panel admina/API).

### 3.2 Wwymagania Niefunkcjonalne
* **Wydajność:** Czas renderowania mapy przy około 1500-2000 czujnikach nie może przekroczyć 3 sekund w nowoczesnych przeglądarkach.
* **Niezawodność:** W przypadku błędu połączenia z zewnętrznym API, aplikacja ma wykorzystywać najnowsze dane zbuforowane w bazie i informować użytkownika o braku bieżącej synchronizacji.
* **Użyteczność:** Pełna responsywność (poprawne działanie i układ na urządzeniach desktopowych).

## 4. Harmonogram Realizacji (Sprinty)
Projekt realizowany jest w cyklu 4 sprintów (każdy sprint obejmuje 1–2 tygodnie pracy).

| Data | Nazwa Sprintu | Kluczowe Zadania i Produkty (Deliverables) |
| :--- | :--- | :--- |
| **03.04.2026 - 11.04.2026** | Analiza UX i Fundamenty Architektury | **UX:** Badanie potrzeb, tworzenie makiety mapy oraz panelu statystyk.<br>**Programista:** Inicjalizacja repozytorium, projekt schematu bazy PostgreSQL, konfiguracja środowiska FastAPI. |
| **21.04.2026 - 27.04.2026** | Backend i Integracja Danych | **Programista:** Oprogramowanie serwisu integrującego dane z Sensor.Community. Konfiguracja. Endpointy dla frontendu (API REST).<br>**Tester:** Testowanie działania strony  oraz responsywności.  |
| **06.05.2026 - 11.05.2026** | Frontend: Mapa i Wizualizacja | **UX:** Akceptacja palety barw (AQI).<br>**Programista:** Osadzenie biblioteki Leaflet, wyświetlanie kółek w odpowiednich kolorach, budowa paska bocznego na szczegóły. |
| **25.05.2026.-28.05.2026** | Statystyki, Wdrożenie i Stabilizacja | **Programista:** Implementacja wykresów, optymalizacja, finalna konfiguracja.<br>**Tester:** Pełne testy.  Zgłaszanie poprawek. |

## 5. Instrukcja Obsługi Aplikacji (Dla Użytkowników)
Interfejs aplikacji zaprojektowano z myślą o prostocie (zgodnie z wytycznymi UX):
1. **Ekran Główny (Mapa):** Po otwarciu aplikacji, centralną część ekranu zajmuje interaktywna mapa ze znacznikami poszczególnych czujników. Aby przybliżyć rejon, można użyć rolki myszy (scroll) lub gestu na urządzeniu mobilnym. Kolor znaczników intuicyjnie odzwierciedla stan powietrza (od zieleni - bardzo dobre powietrze, do bordowego - bardzo złe).
2. **Detale Pomiaru:** Kliknięcie lewym przyciskiem myszy (lub tapnięcie palcem) w konkretny punkt na mapie powoduje płynne wysunięcie panelu pobocznego. Panel wyświetla adres czujnika, aktualną wilgotność, temperaturę oraz dokładne stężenia PM.
3. **Zakładka Analiz i Statystyk:** W górnym menu nawigacyjnym znajduje się odnośnik do panelu "Statystyki". Kliknięcie otwiera globalne podsumowanie – np. średnie stężenie pyłów w obserwowanym kraju oraz wykresy trendów z ostatnich dni.
