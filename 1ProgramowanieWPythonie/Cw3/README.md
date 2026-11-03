Ćwiczenie III –transformacja plików

•Przejrzyjmy się pobieranym przez nas plikom –są to pliki CSV, zawierające 8 kolumn z liczbami. Kolumna o indeksie 0 oznacza numer porządkowy.

•Niektóre wartości nie są wypełnione, zamiast nich są wpisane myślniki.

•Napisz klasę która symuluje prosty proces ETL korzystając z generatorów:

    •Wczytuje pobrany plik linijka po linijce

    •Dla każdej linijki liczy sumę, średnią oraz zapsujeindeksy brakujących wartości (użyj list comprehension)

    •Zapisuje dwa pliki CSV:

        •values.csv z kolumnami: numer porządkowy, suma, średnia.

        •missing_values.csv z kolumnami: numer porządkowy oraz indeksami kolumn ze myślnikami zamiast wartości.