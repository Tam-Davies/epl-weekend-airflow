import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_DIR / ".env")

API_KEY = os.getenv("API_KEY_ACCESS")

URL = "https://api.football-data.org/v4/competitions/PL/matches"


def extract_matches():
    if not API_KEY:
        raise ValueError("API_KEY_ACCESS is missing from .env")

    headers = {
        "X-Auth-Token": API_KEY,
        "Accept": "application/json"
    }

    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()

    output_dir = PROJECT_DIR / "data"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "matches.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Successfully extracted {len(data.get('matches', []))} matches.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    extract_matches()
