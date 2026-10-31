"""Capa de logica de negocio: reglas y validaciones."""
from app import api_client
from app.data import repositories as repo

WINNERS = ("local", "visitante", "empate")


def sync_matches():
    matches = api_client.fetch_matches()
    repo.save_matches(matches)


def list_matches():
    return repo.get_matches()


def list_predictions():
    return repo.get_predictions()


def register_prediction(match_id, winner, home_score, away_score):
    if not repo.match_exists(match_id):
        raise ValueError("El partido no existe")
    if winner not in WINNERS:
        raise ValueError("Resultado no valido")
    if home_score < 0 or away_score < 0:
        raise ValueError("El marcador no puede ser negativo")

    # Regla de negocio: el marcador debe ser coherente con el resultado elegido
    if winner == "local" and home_score <= away_score:
        raise ValueError("Si gana el local, su marcador debe ser mayor")
    if winner == "visitante" and away_score <= home_score:
        raise ValueError("Si gana el visitante, su marcador debe ser mayor")
    if winner == "empate" and home_score != away_score:
        raise ValueError("En un empate los marcadores deben ser iguales")

    repo.save_prediction(match_id, winner, home_score, away_score)
