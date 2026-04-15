import requests


GENDERIZE_URL = "https://api.genderize.io"
AGIFY_URL = "https://api.agify.io"
NATIONALIZE_URL = "https://api.nationalize.io"


class UpstreamAPIError(Exception):
    pass


def fetch_gender(name: str) -> dict:
    try:
        response = requests.get(GENDERIZE_URL, params={"name": name}, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        raise UpstreamAPIError("Genderize returned an invalid response")

    if data.get("gender") is None or data.get("count", 0) == 0:
        raise UpstreamAPIError("Genderize returned an invalid response")

    return data


def fetch_age(name: str) -> dict:
    try:
        response = requests.get(AGIFY_URL, params={"name": name}, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        raise UpstreamAPIError("Agify returned an invalid response")

    if data.get("age") is None:
        raise UpstreamAPIError("Agify returned an invalid response")

    return data


def fetch_nationality(name: str) -> dict:
    try:
        response = requests.get(NATIONALIZE_URL, params={"name": name}, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        raise UpstreamAPIError("Nationalize returned an invalid response")

    if not data.get("country"):
        raise UpstreamAPIError("Nationalize returned an invalid response")

    return data