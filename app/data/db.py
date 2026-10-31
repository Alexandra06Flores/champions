"""Capa de acceso a datos: conexion y esquema."""
import os
import psycopg2
from psycopg2.extras import RealDictCursor

SCHEMA = """
CREATE TABLE IF NOT EXISTS matches (
    id INT PRIMARY KEY,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    match_date TIMESTAMP NOT NULL,
    stage TEXT
);
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    match_id INT NOT NULL REFERENCES matches(id),
    winner TEXT NOT NULL CHECK (winner IN ('local', 'visitante', 'empate')),
    home_score INT NOT NULL,
    away_score INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
"""


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor,
    )


def init_db():
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(SCHEMA)
    finally:
        conn.close()
