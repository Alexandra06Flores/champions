"""API simulada de partidos de la Champions League."""
from flask import Flask, jsonify

app = Flask(__name__)

MATCHES = [
    {"id": 1, "home_team": "Real Madrid", "away_team": "Manchester City", "match_date": "2026-11-04T21:00:00", "stage": "Fase de liga"},
    {"id": 2, "home_team": "FC Barcelona", "away_team": "Bayern Munich", "match_date": "2026-11-04T21:00:00", "stage": "Fase de liga"},
    {"id": 3, "home_team": "Liverpool", "away_team": "Inter de Milan", "match_date": "2026-11-05T21:00:00", "stage": "Fase de liga"},
    {"id": 4, "home_team": "Paris Saint-Germain", "away_team": "Arsenal", "match_date": "2026-11-05T21:00:00", "stage": "Fase de liga"},
    {"id": 5, "home_team": "Juventus", "away_team": "Borussia Dortmund", "match_date": "2026-11-25T21:00:00", "stage": "Fase de liga"},
    {"id": 6, "home_team": "Atletico de Madrid", "away_team": "Benfica", "match_date": "2026-11-25T21:00:00", "stage": "Fase de liga"},
    {"id": 7, "home_team": "Chelsea", "away_team": "Napoli", "match_date": "2026-11-26T21:00:00", "stage": "Fase de liga"},
    {"id": 8, "home_team": "AC Milan", "away_team": "Porto", "match_date": "2026-11-26T21:00:00", "stage": "Fase de liga"},
]


@app.route("/matches")
def matches():
    return jsonify(MATCHES)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
