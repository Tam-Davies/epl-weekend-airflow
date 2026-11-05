from datetime import datetime, timedelta
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from scripts.extract_matches import extract_matches


default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="epl_weekend_ingestion",
    description="Extract Premier League match data using football-data.org",
    default_args=default_args,
    start_date=pendulum.datetime(2026, 11, 5, tz="Africa/Lagos"),
    schedule="0 * * * *",
    catchup=False,
    tags=["premier-league", "api", "weekend"],
) as dag:

    extract = PythonOperator(
        task_id="extract_premier_league_matches",
        python_callable=extract_matches,
    )
