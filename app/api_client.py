"""Cliente que consume la API (simulada) de partidos."""
import os
import time
import requests


def fetch_matches():
    url = os.getenv("MATCHES_API_URL", "http://mockapi:5001/matches")
    for _ in range(10):
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            time.sleep(2)
    raise RuntimeError("No se pudo consultar la API de partidos")
