import json
import psycopg
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "matches.json"

DB_CONFIG = {
    "dbname": "football_db",
    "user": "postgres",
    "host": "localhost",
    "port": 5432,
}

def load_matches():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    matches = data["matches"]

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:

            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS raw;

                CREATE TABLE IF NOT EXISTS raw.matches (
                    match_id BIGINT PRIMARY KEY,
                    match_date TIMESTAMPTZ,
                    status TEXT,
                    matchday INTEGER,
                    home_team TEXT,
                    away_team TEXT,
                    home_score INTEGER,
                    away_score INTEGER,
                    winner TEXT,
                    raw_data JSONB
                );
            """)

            for match in matches:
                cur.execute("""
                    INSERT INTO raw.matches (
                        match_id, match_date, status, matchday,
                        home_team, away_team, home_score, away_score,
                        winner, raw_data
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (match_id) DO UPDATE SET
                        match_date = EXCLUDED.match_date,
                        status = EXCLUDED.status,
                        home_score = EXCLUDED.home_score,
                        away_score = EXCLUDED.away_score,
                        winner = EXCLUDED.winner,
                        raw_data = EXCLUDED.raw_data;
                """, (
                    match["id"],
                    match["utcDate"],
                    match["status"],
                    match["matchday"],
                    match["homeTeam"]["name"],
                    match["awayTeam"]["name"],
                    match["score"]["fullTime"]["home"],
                    match["score"]["fullTime"]["away"],
                    match["score"]["winner"],
                    json.dumps(match),
                ))

        print(f"Successfully loaded {len(matches)} matches into raw.matches")


if __name__ == "__main__":
    load_matches()
