"""Capa de acceso a datos: consultas SQL."""
from app.data.db import get_conn


def _run(sql, params=None, fetch=False):
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall() if fetch else None
    finally:
        conn.close()


def save_matches(matches):
    for m in matches:
        _run(
            """INSERT INTO matches (id, home_team, away_team, match_date, stage)
               VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING""",
            (m["id"], m["home_team"], m["away_team"], m["match_date"], m["stage"]),
        )


def get_matches():
    return _run("SELECT * FROM matches ORDER BY match_date, id", fetch=True)


def match_exists(match_id):
    return bool(_run("SELECT 1 FROM matches WHERE id = %s", (match_id,), fetch=True))


def save_prediction(match_id, winner, home_score, away_score):
    _run(
        """INSERT INTO predictions (match_id, winner, home_score, away_score)
           VALUES (%s, %s, %s, %s)""",
        (match_id, winner, home_score, away_score),
    )


def get_predictions():
    return _run(
        """SELECT p.id, p.winner, p.home_score, p.away_score, p.created_at,
                  m.home_team, m.away_team
           FROM predictions p JOIN matches m ON m.id = p.match_id
           ORDER BY p.created_at DESC""",
        fetch=True,
    )
