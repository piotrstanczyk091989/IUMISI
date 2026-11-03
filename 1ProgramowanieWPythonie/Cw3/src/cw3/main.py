
import requests
import csv



# 1. POBIERANIE PLIKU

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

    except requests.exceptions.RequestException as error:
        print(f"Błąd pobierania pliku: {error}")
        raise



# 2. KLASA ETL

class ETLProcess:

    def __init__(self, filename):
        """
        Konstruktor klasy.
        Zapamiętuje nazwę pliku wejściowego.
        """
        self.filename = filename


    # 2.1. ODCZYT PLIKU GENERATOREM

    def read_file(self):
        """
        Odczytuje plik CSV linijka po linijce.
        """
        with open(self.filename, "r", encoding="utf-8") as file:

            reader = csv.reader(file)

            for row in reader:
                yield row


    # 2.2. TRANSFORMACJA DANYCH

    def process_data(self):

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


    # 2.3. ZAPIS WYNIKÓW DO PLIKÓW

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


# 3. URUCHOMIENIE PROGRAMU

url = "https://oleksandr-fedoruk.com/sggw/podyplomowe/file"

filename = "latest.csv"

download_file(url, filename)

etl = ETLProcess(filename)

etl.save_results()

print("Proces ETL zakończony!")