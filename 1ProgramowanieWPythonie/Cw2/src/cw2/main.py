
import requests

class DownloadError(Exception):
    pass

class NotFoundError(DownloadError):
    pass

class AccessDeniedError(DownloadError):
    pass


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

        if e.response.status_code == 404:
            raise NotFoundError("Błąd 404: Nie znaleziono pliku.") from e

        elif e.response.status_code == 403:
            raise AccessDeniedError("Błąd 403: Dostęp zabroniony.") from e

        else:
            print(f"Błąd HTTP: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Błąd pobierania pliku: {e}")


# Testy
url = "https://oleksandr-fedoruk.com/sggw/podyplomowe/file"
pobierz_plik(url)

url_404 = "http://oleksandr-fedoruk.com/sggw/podyplomowe/404"

try:
    pobierz_plik(url_404)
except NotFoundError as e:
    print(e)

url_403 = "http://oleksandr-fedoruk.com/sggw/podyplomowe/403"

try:
    pobierz_plik(url_403)
except AccessDeniedError as e:
    print(e)
