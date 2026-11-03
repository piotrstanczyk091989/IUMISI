
import requests
import csv
import time
from datetime import datetime


# 1. WYJĄTKI

class DownloadError(Exception):
    pass


class NotFoundError(DownloadError):
    pass


class AccessDeniedError(DownloadError):
    pass


# 2. DEKORATOR LOGUJĄCY CZAS

def log_time(func):
    """
    Dekorator wyświetlający czas rozpoczęcia i zakończenia funkcji.
    """
    def wrapper(*args, **kwargs):

        start_datetime = datetime.now()
        start = time.time()

        print(
            f"Rozpoczęcie funkcji {func.__name__}: "
            f"{start_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        try:
            yield from func(*args, **kwargs)

        finally:
            end = time.time()
            end_datetime = datetime.now()

            print(
                f"Zakończenie funkcji {func.__name__}: "
                f"{end_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
            )

            print(f"Czas wykonania: {end - start:.4f} sekundy")

    return wrapper


# 3. POBIERANIE PLIKU

def download_file(url, filename="latest.csv"):
    """
    Pobiera plik z podanego adresu URL
    i zapisuje go na dysku.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(filename, "wb") as file:
            file.write(response.content)

        print(f"Plik został pobrany: {filename}")

    except requests.exceptions.HTTPError as e:

        if e.response is not None and e.response.status_code == 404:
            raise NotFoundError(
                "Błąd 404: Nie znaleziono pliku."
            ) from e

        elif e.response is not None and e.response.status_code == 403:
            raise AccessDeniedError(
                "Błąd 403: Dostęp zabroniony."
            ) from e

        else:
            print(f"Błąd HTTP: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Błąd pobierania pliku: {e}")


# 4. KLASA ETL

class ETLProcess:

    def __init__(self, filename):
        """
        Konstruktor klasy.
        Zapamiętuje nazwę pliku wejściowego.
        """
        self.filename = filename


    # 4.1. ODCZYT PLIKU GENERATOREM

    def read_file(self):
        """
        Odczytuje plik CSV linijka po linijce.
        """
        with open(self.filename, "r", encoding="utf-8") as file:

            reader = csv.reader(file)

            for row in reader:
                yield row


    # 4.2. TRANSFORMACJA DANYCH

    @log_time
    def process_data(self):
        """
        Przetwarza dane z pliku CSV.
        """
        for row in self.read_file():

            # Pomijamy pusty wiersz
            if not row:
                continue

            # Pierwsza kolumna to numer porządkowy
            number = row[0]

            # Wyszukujemy indeksy brakujących wartości
            missing = [
                index
                for index, value in enumerate(row[1:], start=1)
                if value.strip() == "-"
            ]

            # Zamieniamy wartości na liczby
            # Pomijamy numer porządkowy i myślniki
            numbers = [
                float(value)
                for value in row[1:]
                if value.strip() != "-"
            ]

            # Obliczamy sumę
            total = sum(numbers)

            # Obliczamy średnią
            if numbers:
                average = total / len(numbers)
            else:
                average = 0

            # Generator zwraca wyniki dla jednego wiersza
            yield number, total, average, missing


    # 4.3. ZAPIS WYNIKÓW DO PLIKÓW

    def save_results(self):

        with open("values.csv", "w", newline="", encoding="utf-8") as values_file, \
             open("missing_values.csv", "w", newline="", encoding="utf-8") as missing_file:

            values_writer = csv.writer(values_file)

            missing_writer = csv.writer(
                missing_file,
                quoting=csv.QUOTE_NONNUMERIC
            )

            # Nagłówki kolumn
            values_writer.writerow(["number", "sum", "average"])
            missing_writer.writerow(["number", "missing_column_indexes"])

            # Odczytujemy dane z generatora
            for number, total, average, missing in self.process_data():

                # Zapis sumy i średniej
                values_writer.writerow([
                    number,
                    total,
                    average
                ])

                # Zapis indeksów brakujących wartości
                missing_writer.writerow([
                    number,
                    ",".join(map(str, missing))
                ])

        print("Zapisano plik values.csv")
        print("Zapisano plik missing_values.csv")


# 5. URUCHOMIENIE PROGRAMU

url = "https://oleksandr-fedoruk.com/sggw/podyplomowe/file"

filename = "latest.csv"

try:

    download_file(url, filename)

    etl = ETLProcess(filename)

    etl.save_results()

    print("Proces ETL zakończony!")

except NotFoundError as e:
    print(e)

except AccessDeniedError as e:
    print(e)
