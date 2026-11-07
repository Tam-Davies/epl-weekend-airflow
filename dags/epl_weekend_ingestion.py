from datetime import timedelta
from pathlib import Path
import logging
import sys
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator, ShortCircuitOperator

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from scripts.extract_matches import extract_matches


def is_weekend_window(**context):
    # Allow manual runs for testing.
    dag_run = context.get("dag_run")

    if dag_run and dag_run.run_type == "manual":
        return True

    run_time = pendulum.instance(
        context["logical_date"]
    ).in_timezone("Africa/Lagos")

    weekday = run_time.weekday()
    hour = run_time.hour

    # Friday from 8 PM, all Saturday and Sunday,
    # and all Monday through 11 PM.
    return (
        (weekday == 4 and hour >= 20)
        or weekday in (5, 6)
        or weekday == 0
    )


def failure_alert(context):
    task_instance = context["task_instance"]
    exception = context.get("exception")

    alert_message = (
        f"ALERT: Task {task_instance.task_id} failed "
        f"in DAG {task_instance.dag_id}. "
        f"Error: {exception}\n"
    )

    logging.error(alert_message)

    alert_dir = PROJECT_DIR / "logs"
    alert_dir.mkdir(exist_ok=True)

    with open(alert_dir / "failure_alerts.log", "a") as file:
        file.write(alert_message)


default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="epl_weekend_ingestion",
    description="Orchestrate Premier League weekend data ingestion",
    default_args=default_args,
    start_date=pendulum.datetime(2026, 11, 5, tz="Africa/Lagos"),
    schedule="0 * * * *",
    catchup=False,
    tags=["premier-league", "api", "weekend"],
) as dag:

    check_weekend = ShortCircuitOperator(
        task_id="check_weekend_window",
        python_callable=is_weekend_window,
    )

    extract = PythonOperator(
        task_id="extract_premier_league_matches",
        python_callable=extract_matches,
        on_failure_callback=failure_alert,
    )

    check_weekend >> extract