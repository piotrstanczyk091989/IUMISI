
import requests


def pobierz_plik(url, nazwa_pliku="latest.txt"):
    """
    Pobiera plik z podanego adresu URL i zapisuje go na dysku.

    Parametry:
    url - adres URL pliku do pobrania
    nazwa_pliku - nazwa pliku zapisywanego na dysku
                 (domyślnie latest.txt)
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(nazwa_pliku, "wb") as plik:
            plik.write(response.content)

        print(f"Plik został pobrany i zapisany jako: {nazwa_pliku}")

    except requests.exceptions.RequestException as e:
        print(f"Błąd pobierania pliku: {e}")


# Przykładowe wywołanie funkcji
url = "https://oleksandr-fedoruk.com/sggw/podyplomowe/file"

pobierz_plik(url)
