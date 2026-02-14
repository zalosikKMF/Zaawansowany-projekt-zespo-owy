# Zaawansowany-projekt-zespo-owy-gr.2
1. Informacje ogólne:

Nazwa projektu: System monitorowania jakości powietrza
Rodzaj systemu: Aplikacja webowa (z możliwością rozszerzenia o aplikację mobilną)
Obszar zastosowania: Monitoring środowiskowy, Smart City, analiza danych IoT
Wersja dokumentu: 0,1 alfa
Data opracowania: 10.02.2026

2. Wprowadzenie

System monitorowania jakości powietrza to platforma umożliwiająca zbieranie, przetwarzanie, analizę i wizualizację danych środowiskowych pochodzących z sieci czujników IoT rozmieszczonych na danym obszarze (np. miasto, region lub kraj). System umożliwia bieżące monitorowanie parametrów jakości powietrza, wspiera procesy decyzyjne jednostek administracyjnych oraz zapewnia dostęp do danych historycznych w celu prowadzenia analiz trendów i oceny zmian środowiskowych w czasie.

2.1 Cel dokumentu
Celem niniejszego dokumentu jest:

- określenie wymagań funkcjonalnych i niefunkcjonalnych systemu,
- zdefiniowanie zakresu działania platformy,
- wskazanie grupy docelowej,
- stworzenie podstawy do dalszego projektowania i implementacji systemu.
2.2 Grupa docelowa:

- Operatorzy i analitycy danych środowiskowych.
- Jednostki administracji publicznej.
- Użytkownicy publiczni (tryb tylko do odczytu).

#3. Wymagania funkcjonalne
   
   3.1.1 Rejestracja użytkownika

System musi:
- umożliwiać rejestrację konta poprzez formularz (e-mail + hasło),
- weryfikować poprawność adresu e-mail (mechanizm potwierdzenia),
- wymuszać minimalną złożoność hasła (min. długość, znaki specjalne),
- blokować możliwość rejestracji z użyciem już istniejącego adresu e-mail.
